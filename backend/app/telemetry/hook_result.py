from dataclasses import dataclass
from typing import Optional

@dataclass
class HookResult:
    session_id: str
    timestamp: float

    layer_name: str
    layer_type: str
    layer_idx: int

    tensor_shape: str

    latency_ms: Optional[float] = None

    mean_activation: Optional[float] = None
    max_activation: Optional[float] = None
    min_activation: Optional[float] = None
    variance: Optional[float] = None
    sparsity: Optional[float] = None

    nan_count: Optional[int] = None
    inf_count: Optional[int] = None
    max_abs_value: Optional[float] = None

    device: str = "cpu"
    dtype: str = "float32"
