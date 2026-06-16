from .bus import EventBus
from .events import MetricEvent, ActivationEvent, AnomalyEvent
from .config import telemetry_config
import uuid
import time

class AnomalyEngine:
    """
    Subscribes to EventBus streams and evaluates them instantly against thresholds.
    """
    def __init__(self, bus: EventBus):
        self.bus = bus
        self.bus.subscribe(MetricEvent, self)
        self.bus.subscribe(ActivationEvent, self)

    async def push(self, event):
        """
        Acts as a pseudo-sink to receive events from the bus.
        """
        if not telemetry_config.ENABLE_ANOMALIES:
            return

        anomaly = None

        if isinstance(event, MetricEvent):
            if event.dur_ms > telemetry_config.MAX_LATENCY_THRESHOLD_MS:
                anomaly = AnomalyEvent(
                    session_id=event.session_id,
                    id=str(uuid.uuid4()),
                    t=event.t,
                    severity="warn",
                    layer=event.layer,
                    message=f"Latency spike: {event.dur_ms:.2f}ms exceeds threshold ({telemetry_config.MAX_LATENCY_THRESHOLD_MS}ms)"
                )
        
        elif isinstance(event, ActivationEvent):
            if abs(event.max) > telemetry_config.MAX_ACTIVATION_THRESHOLD:
                anomaly = AnomalyEvent(
                    session_id=event.session_id,
                    id=str(uuid.uuid4()),
                    t=time.time(),
                    severity="warn",
                    layer=event.layer,
                    message=f"Activation spike: max={event.max:.2f} exceeds threshold ({telemetry_config.MAX_ACTIVATION_THRESHOLD})"
                )
            
            if event.nan_count > 0:
                anomaly = AnomalyEvent(
                    session_id=event.session_id,
                    id=str(uuid.uuid4()),
                    t=time.time(),
                    severity="error",
                    layer=event.layer,
                    message=f"Numerical instability: {event.nan_count} NaNs detected."
                )
                
            if event.inf_count > 0:
                anomaly = AnomalyEvent(
                    session_id=event.session_id,
                    id=str(uuid.uuid4()),
                    t=time.time(),
                    severity="error",
                    layer=event.layer,
                    message=f"Numerical instability: {event.inf_count} Infs detected."
                )

        if anomaly:
            await self.bus.publish(anomaly)
