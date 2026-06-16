import asyncio
import time
import queue
from typing import List
from .hook_result import HookResult

class TelemetryAggregator:
    """
    Sits between synchronous PyTorch hooks and the async EventBus pipeline.
    Batches HookResults and flushes them periodically to avoid flooding.
    """
    def __init__(self, async_collector, main_loop: asyncio.AbstractEventLoop, flush_interval: float = 0.5):
        self.async_collector = async_collector
        self.main_loop = main_loop
        self.flush_interval = flush_interval
        
        self.batch_queue: queue.Queue = queue.Queue()
        self.last_flush_time = time.time()

    def add_result(self, result: HookResult) -> None:
        """
        Called synchronously by PyTorch hooks.
        """
        self.batch_queue.put(result)
        
        current_time = time.time()
        if current_time - self.last_flush_time >= self.flush_interval:
            self.flush()

    def flush(self) -> None:
        """
        Takes all results from the queue and fires an async task on the main loop.
        """
        results: List[HookResult] = []
        while not self.batch_queue.empty():
            try:
                results.append(self.batch_queue.get_nowait())
            except queue.Empty:
                break
                
        if results:
            # Dispatch to async pipeline
            asyncio.run_coroutine_threadsafe(
                self.async_collector.process_batch(results),
                self.main_loop
            )
        
        self.last_flush_time = time.time()
