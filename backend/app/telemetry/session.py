import asyncio
from typing import Any
from .context import TelemetryContext
from .bus import EventBus
from .registry import HookRegistry
from .adapters import ModelAdapter, LlamaAdapter, GPT2Adapter
from .topology import TopologyExtractor
from .runtime import ModelRuntime
from .sinks import DatabaseSink, WebSocketSink
from .collectors import MemoryCollector, MetricCollector
from .aggregator import TelemetryAggregator
from .anomaly_engine import AnomalyEngine
from .events import SessionEvent, ModelRuntimeState, TokenEvent, MemoryEvent, MetricEvent, ActivationEvent, AnomalyEvent, TopologyEvent
import logging

logger = logging.getLogger(__name__)

class SessionManager:
    """
    Orchestrates the entire telemetry pipeline for a single tracing run.
    """
    def __init__(self, session_id: str, model_name: str, device: str = None):
        self.context = TelemetryContext(
            session_id=session_id,
            model_name=model_name,
            device=device or "cpu"
        )
        self.event_bus = EventBus()
        self.runtime = ModelRuntime(model_name, device)
        
        # Sinks
        self.ws_sink = WebSocketSink()
        self.db_sink = DatabaseSink()
        
        # Core Events -> Sinks
        for event_type in [TokenEvent, MemoryEvent, SessionEvent, MetricEvent, ActivationEvent, AnomalyEvent, TopologyEvent]:
            self.event_bus.subscribe(event_type, self.ws_sink)
            if event_type is not SessionEvent:
                self.event_bus.subscribe(event_type, self.db_sink)

        # Collectors / Engines
        self.memory_collector = MemoryCollector(self.event_bus, self.context)
        self.metric_collector = MetricCollector(self.event_bus)
        self.anomaly_engine = AnomalyEngine(self.event_bus)
        
        self.aggregator = None
        self.adapter = None
        self.topology_extractor = None
        self.hook_registry = None

    def _resolve_adapter(self, model_instance: Any) -> ModelAdapter:
        name_lower = self.context.model_name.lower()
        if "gpt2" in name_lower:
            return GPT2Adapter(model_instance)
        elif "tinyllama" in name_lower:
            return LlamaAdapter(model_instance)
        raise ValueError(f"No adapter found for {self.context.model_name}")

    async def start_async(self, prompt: str) -> None:
        """
        Initializes sinks, loads model async, and starts generation.
        """
        logger.info(f"START SESSION: {self.context.session_id}")
        try:
            # Broadcast loading
            await self.event_bus.publish(SessionEvent(
                session_id=self.context.session_id, 
                type="model_loading", 
                state=ModelRuntimeState.LOADING
            ))

            # Load model async
            logger.info("MODEL LOAD START")
            await self.runtime.load_model_async()
            logger.info("MODEL LOAD COMPLETE")
            
            # Initialize the synchronous aggregator bridging to the async MetricCollector
            self.aggregator = TelemetryAggregator(
                async_collector=self.metric_collector,
                main_loop=asyncio.get_running_loop(),
                flush_interval=0.5
            )

            # Instantiate topology and hooks
            self.adapter = self._resolve_adapter(self.runtime.model)
            self.topology_extractor = TopologyExtractor(self.adapter)
            self.hook_registry = HookRegistry(self.context, self.adapter, self.aggregator)
            
            # Attach hooks
            self.hook_registry.attach_all()

            # Broadcast topology
            logger.info(f"Extracting and publishing topology for session {self.context.session_id}")
            topology_data = self.topology_extractor.extract()
            await self.event_bus.publish(TopologyEvent(
                session_id=self.context.session_id,
                blocks=topology_data["blocks"]
            ))
            logger.info("TOPOLOGY SAVED")

            # Broadcast ready
            await self.event_bus.publish(SessionEvent(
                session_id=self.context.session_id, 
                type="model_ready", 
                state=ModelRuntimeState.READY
            ))
            
            # Start Memory polling
            self.memory_collector.start()

            # Start generating
            logger.info(f"Background generation beginning for session {self.context.session_id}")
            logger.info("TOKEN GENERATION START")
            await self.event_bus.publish(SessionEvent(
                session_id=self.context.session_id, 
                type="generation_started", 
                state=ModelRuntimeState.GENERATING
            ))

            # Stream tokens
            first_token_seen = False
            async for token_idx, token_text, elapsed_ms in self.runtime.stream_generate(prompt):
                if not first_token_seen:
                    logger.info("FIRST TOKEN GENERATED")
                    first_token_seen = True
                    
                await self.event_bus.publish(TokenEvent(
                    session_id=self.context.session_id,
                    idx=token_idx,
                    token=token_text,
                    ms=elapsed_ms
                ))
                if token_idx == 0:
                    logger.info("FIRST TOKEN SAVED")
                logger.info("TOKEN SAVED")
                
            # Final flush of the aggregator
            self.aggregator.flush()

            await self.event_bus.publish(SessionEvent(
                session_id=self.context.session_id, 
                type="generation_finished", 
                state=ModelRuntimeState.READY
            ))
            
            logger.info(f"Generation completed for session {self.context.session_id}")
            logger.info("GENERATION COMPLETE")
            self.memory_collector.stop()
            
        except Exception as e:
            logger.exception(f"CRITICAL: Background generation failed for session {self.context.session_id}, model {self.context.model_name}")
            self.memory_collector.stop()

    def stop(self) -> None:
        """
        Removes all hooks and gracefully flushes the EventBus.
        """
        if self.hook_registry:
            self.hook_registry.remove_all_hooks()
        if self.aggregator:
            self.aggregator.flush()
        self.memory_collector.stop()
