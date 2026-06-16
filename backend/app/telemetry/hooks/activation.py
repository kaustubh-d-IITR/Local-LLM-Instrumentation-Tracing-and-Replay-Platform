import time
import torch
from ..hook_result import HookResult
from ..aggregator import TelemetryAggregator
from ..config import telemetry_config

class ActivationHook:
    def __init__(self, session_id: str, layer_idx: int, layer_name: str, layer_type: str, aggregator: TelemetryAggregator):
        self.session_id = session_id
        self.layer_idx = layer_idx
        self.layer_name = layer_name
        self.layer_type = layer_type
        self.aggregator = aggregator

    def hook(self, module, inputs, output):
        if not telemetry_config.ENABLE_ACTIVATIONS:
            return

        tensor_ref = output[0] if isinstance(output, tuple) else output
        
        if not isinstance(tensor_ref, torch.Tensor):
            return

        # Explicit float conversion and item() to prevent memory leaks
        with torch.no_grad():
            tensor_float = tensor_ref.float()
            mean_val = tensor_float.mean().item()
            max_val = tensor_float.max().item()
            min_val = tensor_float.min().item()
            var_val = tensor_float.var().item() if tensor_float.numel() > 1 else 0.0
            sparsity_val = (tensor_float == 0).sum().item() / tensor_float.numel()

        result = HookResult(
            session_id=self.session_id,
            timestamp=time.time(),
            layer_name=self.layer_name,
            layer_type=self.layer_type,
            layer_idx=self.layer_idx,
            tensor_shape=str(list(tensor_ref.shape)),
            mean_activation=mean_val,
            max_activation=max_val,
            min_activation=min_val,
            variance=var_val,
            sparsity=sparsity_val,
            device=str(tensor_ref.device),
            dtype=str(tensor_ref.dtype)
        )
        
        self.aggregator.add_result(result)
