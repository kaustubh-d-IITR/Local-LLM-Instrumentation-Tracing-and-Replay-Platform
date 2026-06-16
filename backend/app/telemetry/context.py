import time
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class TelemetryContext:
    """
    Context propagated through the telemetry pipeline.
    Avoids passing common args to every collector function.
    """
    session_id: str
    model_name: str
    device: str
    start_time: float = field(default_factory=time.time)
    trace_id: Optional[str] = None
