import asyncio
from abc import ABC, abstractmethod
from typing import Any
from .events import BaseTelemetryEvent, MemoryEvent, TokenEvent, SessionEvent, MetricEvent, ActivationEvent, AnomalyEvent
from app.api.endpoints.ws import manager
from app.core.database import SessionLocal
from app.models.token import Token
from app.models.memory import Memory
from app.models.metric import Metric
from app.models.activation import Activation
from app.models.anomaly import Anomaly

class BaseSink(ABC):
    """
    Interface for a telemetry sink.
    """
    @abstractmethod
    async def push(self, event: BaseTelemetryEvent) -> None:
        pass

class DatabaseSink(BaseSink):
    """
    Asynchronously batches events and flushes them to the PostgreSQL database.
    """
    async def push(self, event: BaseTelemetryEvent) -> None:
        def _insert():
            with SessionLocal() as db:
                if isinstance(event, TokenEvent):
                    db.add(Token(session_id=event.session_id, idx=event.idx, token=event.token, ms=event.ms))
                elif isinstance(event, MemoryEvent):
                    db.add(Memory(session_id=event.session_id, t=event.t, gpu=event.gpu, cpu=event.cpu))
                elif isinstance(event, MetricEvent):
                    db.add(Metric(
                        id=event.id, session_id=event.session_id, t=event.t, layer=event.layer,
                        op=event.op, dur_ms=event.dur_ms, shape=event.shape, dtype=event.dtype,
                        device=event.device, level=event.level
                    ))
                elif isinstance(event, ActivationEvent):
                    db.add(Activation(
                        session_id=event.session_id, layer=event.layer, mean=event.mean,
                        max=event.max, min=event.min, variance=event.variance, sparsity=event.sparsity,
                        nan_count=event.nan_count, inf_count=event.inf_count
                    ))
                elif isinstance(event, AnomalyEvent):
                    db.add(Anomaly(
                        id=event.id, session_id=event.session_id, t=event.t,
                        severity=event.severity, layer=event.layer, message=event.message
                    ))
                db.commit()
                
        # Fire and forget database insert
        asyncio.create_task(asyncio.to_thread(_insert))

class WebSocketSink(BaseSink):
    """
    Pushes ephemeral events immediately to connected clients via WebSockets.
    """
    async def push(self, event: BaseTelemetryEvent) -> None:
        payload = event.model_dump_json()
        await manager.broadcast_to_session(payload, event.session_id)

class ReplaySink(BaseSink):
    """
    Groups events by token_idx and layer, then flushes a full 
    TelemetrySnapshot frame to the database for historical replay.
    """
    async def push(self, event: BaseTelemetryEvent) -> None:
        pass
