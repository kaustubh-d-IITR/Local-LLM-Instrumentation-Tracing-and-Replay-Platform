from pydantic import BaseModel
from typing import Literal
from enum import Enum

class ModelRuntimeState(str, Enum):
    LOADING = "LOADING"
    READY = "READY"
    GENERATING = "GENERATING"
    ERROR = "ERROR"
    UNLOADED = "UNLOADED"

# Base Event
class BaseTelemetryEvent(BaseModel):
    session_id: str

class SessionEvent(BaseTelemetryEvent):
    type: Literal["session_started", "model_loading", "model_ready", "generation_started", "generation_finished", "session_failed"]
    state: ModelRuntimeState
    message: str | None = None


class MetricEvent(BaseTelemetryEvent):
    id: str
    t: float
    layer: int
    op: str
    dur_ms: float
    shape: str
    dtype: str
    device: str
    level: Literal["info", "warn", "error"]

class ActivationEvent(BaseTelemetryEvent):
    layer: int
    mean: float
    max: float
    min: float
    variance: float
    sparsity: float
    nan_count: int = 0
    inf_count: int = 0

class AttentionSummaryEvent(BaseTelemetryEvent):
    layer: int
    head: int
    entropy: float
    max_weight: float

class MemoryEvent(BaseTelemetryEvent):
    t: float
    gpu: float
    cpu: float

class TokenEvent(BaseTelemetryEvent):
    idx: int
    token: str
    ms: float

class AnomalyEvent(BaseTelemetryEvent):
    id: str
    t: float
    severity: Literal["info", "warn", "error"]
    layer: int
    message: str

class TopologyEvent(BaseTelemetryEvent):
    blocks: list
