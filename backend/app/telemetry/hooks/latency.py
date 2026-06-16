import time
import torch
from ..hook_result import HookResult
from ..aggregator import TelemetryAggregator
from ..config import telemetry_config

class LatencyHook:
    def __init__(self, session_id: str, layer_idx: int, layer_name: str, layer_type: str, aggregator: TelemetryAggregator):
        self.session_id = session_id
        self.layer_idx = layer_idx
        self.layer_name = layer_name
        self.layer_type = layer_type
        self.aggregator = aggregator
        self.start_times = {}

    def pre_hook(self, module, inputs):
        if not telemetry_config.ENABLE_LATENCY:
            return
        # Store start time per call (using an ID to handle nested/recursive calls just in case, though normally sequence is fine)
        # Using a simple attribute for Phase 2.3
        self.start_times[id(inputs)] = time.time()

    def hook(self, module, inputs, output):
        if not telemetry_config.ENABLE_LATENCY:
            return
            
        start_time = self.start_times.pop(id(inputs), None)
        if start_time is None:
            return

        latency_ms = (time.time() - start_time) * 1000.0

        # Safe extraction of shape/device/dtype
        tensor_ref = output[0] if isinstance(output, tuple) else output
        if isinstance(tensor_ref, torch.Tensor):
            shape_str = str(list(tensor_ref.shape))
            device_str = str(tensor_ref.device)
            dtype_str = str(tensor_ref.dtype)
        else:
            shape_str = "unknown"
            device_str = "cpu"
            dtype_str = "unknown"

        result = HookResult(
            session_id=self.session_id,
            timestamp=time.time(),
            layer_name=self.layer_name,
            layer_type=self.layer_type,
            layer_idx=self.layer_idx,
            tensor_shape=shape_str,
            latency_ms=latency_ms,
            device=device_str,
            dtype=dtype_str
        )
        
        self.aggregator.add_result(result)
