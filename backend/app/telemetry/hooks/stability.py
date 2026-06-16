import time
import torch
from ..hook_result import HookResult
from ..aggregator import TelemetryAggregator
from ..config import telemetry_config

class NumericalStabilityHook:
    def __init__(self, session_id: str, layer_idx: int, layer_name: str, layer_type: str, aggregator: TelemetryAggregator):
        self.session_id = session_id
        self.layer_idx = layer_idx
        self.layer_name = layer_name
        self.layer_type = layer_type
        self.aggregator = aggregator

    def hook(self, module, inputs, output):
        if not telemetry_config.ENABLE_ANOMALIES:
            return

        tensor_ref = output[0] if isinstance(output, tuple) else output
        
        if not isinstance(tensor_ref, torch.Tensor):
            return

        with torch.no_grad():
            nan_count = torch.isnan(tensor_ref).sum().item()
            inf_count = torch.isinf(tensor_ref).sum().item()
            
            if nan_count == 0 and inf_count == 0:
                # If everything is perfectly stable, don't flood with empty anomaly checks
                # Only report if there are actually NaNs or Infs
                # Or we can always report. The AnomalyEngine checks > 0.
                pass
            
            # For the sake of the specification "NaN detection / Inf detection", we always report
            # them as HookResults, and AnomalyEngine generates AnomalyEvents.
            max_abs = tensor_ref.abs().max().item() if tensor_ref.numel() > 0 else 0.0

        result = HookResult(
            session_id=self.session_id,
            timestamp=time.time(),
            layer_name=self.layer_name,
            layer_type=self.layer_type,
            layer_idx=self.layer_idx,
            tensor_shape=str(list(tensor_ref.shape)),
            nan_count=nan_count,
            inf_count=inf_count,
            max_abs_value=max_abs,
            device=str(tensor_ref.device),
            dtype=str(tensor_ref.dtype)
        )
        
        self.aggregator.add_result(result)
