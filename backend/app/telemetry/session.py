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
from .events import SessionEvent, ModelRuntimeState, TokenEvent, MemoryEvent, MetricEvent, ActivationEvent, AnomalyEvent
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
        for event_type in [TokenEvent, MemoryEvent, SessionEvent, MetricEvent, ActivationEvent, AnomalyEvent]:
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
        try:
            # Broadcast loading
            await self.event_bus.publish(SessionEvent(
                session_id=self.context.session_id, 
                type="model_loading", 
                state=ModelRuntimeState.LOADING
            ))

            # Load model async
            await self.runtime.load_model_async()
            
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
            await self.event_bus.publish(SessionEvent(
                session_id=self.context.session_id, 
                type="generation_started", 
                state=ModelRuntimeState.GENERATING
            ))

            # Stream tokens
            async for token_idx, token_text, elapsed_ms in self.runtime.stream_generate(prompt):
                await self.event_bus.publish(TokenEvent(
                    session_id=self.context.session_id,
                    idx=token_idx,
                    token=token_text,
                    ms=elapsed_ms
                ))
                
            # Final flush of the aggregator
            self.aggregator.flush()

            await self.event_bus.publish(SessionEvent(
                session_id=self.context.session_id, 
                type="generation_finished", 
                state=ModelRuntimeState.READY
            ))
            
            logger.info(f"Generation completed for session {self.context.session_id}")
            self.memory_collector.stop()
            
        except Exception as e:
            logger.error(f"Error during background generation for session {self.context.session_id}: {e}", exc_info=True)
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
