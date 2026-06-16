import asyncio
import time
import torch
import psutil
from typing import Any
from abc import ABC, abstractmethod
from .context import TelemetryContext
from .events import BaseTelemetryEvent, MemoryEvent
from .bus import EventBus

import uuid
from typing import List
from .hook_result import HookResult
from .events import MetricEvent, ActivationEvent

class MetricCollector:
    """
    Transforms batched HookResults into proper Events and publishes them to the EventBus.
    """
    def __init__(self, bus: EventBus):
        self.bus = bus

    async def process_batch(self, results: List[HookResult]) -> None:
        """
        Receives an asynchronous batch of results from the TelemetryAggregator.
        """
        for res in results:
            if res.latency_ms is not None:
                event = MetricEvent(
                    session_id=res.session_id,
                    id=str(uuid.uuid4()),
                    t=res.timestamp,
                    layer=res.layer_idx,
                    op=res.layer_type,
                    dur_ms=res.latency_ms,
                    shape=res.tensor_shape,
                    dtype=res.dtype,
                    device=res.device,
                    level="info"
                )
                await self.bus.publish(event)
                
            if res.mean_activation is not None or res.nan_count is not None:
                # Can be an Activation or Stability result. We map it to ActivationEvent.
                event = ActivationEvent(
                    session_id=res.session_id,
                    layer=res.layer_idx,
                    mean=res.mean_activation or 0.0,
                    max=res.max_activation or 0.0,
                    min=res.min_activation or 0.0,
                    variance=res.variance or 0.0,
                    sparsity=res.sparsity or 0.0,
                    nan_count=res.nan_count or 0,
                    inf_count=res.inf_count or 0
                )
                await self.bus.publish(event)

class TelemetryCollector(ABC):
    """
    Base class for all collectors.
    A collector formats raw tensor/timing data into a BaseTelemetryEvent 
    and publishes it to the EventBus.
    """
    def __init__(self, bus: EventBus):
        self.bus = bus

    @abstractmethod
    def collect(self, raw_data: Any, context: TelemetryContext) -> None:
        pass

class LatencyCollector(TelemetryCollector):
    def collect(self, raw_data: Any, context: TelemetryContext) -> None:
        pass

class ActivationCollector(TelemetryCollector):
    def collect(self, raw_data: Any, context: TelemetryContext) -> None:
        pass

class MemoryCollector(TelemetryCollector):
    def __init__(self, bus: EventBus, context: TelemetryContext):
        super().__init__(bus)
        self.context = context
        self._running = False
        self._task = None

    def start(self):
        self._running = True
        self._task = asyncio.create_task(self._poll_loop())

    def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()

    async def _poll_loop(self):
        while self._running:
            cpu_gb = psutil.virtual_memory().used / (1024 ** 3)
            
            if torch.cuda.is_available():
                gpu_gb = torch.cuda.memory_allocated() / (1024 ** 3)
            else:
                gpu_gb = 0.0

            event = MemoryEvent(
                session_id=self.context.session_id,
                t=time.time(),
                gpu=gpu_gb,
                cpu=cpu_gb
            )
            
            await self.bus.publish(event)
            await asyncio.sleep(1.0)
            
    def collect(self, raw_data: Any, context: TelemetryContext) -> None:
        pass

