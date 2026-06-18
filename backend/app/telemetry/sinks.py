import asyncio
from abc import ABC, abstractmethod
from typing import Any
from .events import BaseTelemetryEvent, MemoryEvent, TokenEvent, SessionEvent, MetricEvent, ActivationEvent, AnomalyEvent, TopologyEvent
from app.api.endpoints.ws import manager
from app.core.database import SessionLocal
from app.models.token import Token
from app.models.memory import Memory
from app.models.metric import Metric
from app.models.activation import Activation
from app.models.anomaly import Anomaly
from app.models.topology import Topology
import logging

logger = logging.getLogger(__name__)

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
                    logger.debug(f"Persisting TokenEvent for {event.session_id}: token '{event.token}'")
                    db.add(Token(session_id=event.session_id, idx=event.idx, token=event.token, ms=event.ms))
                elif isinstance(event, MemoryEvent):
                    logger.debug(f"Persisting MemoryEvent for {event.session_id}")
                    db.add(Memory(session_id=event.session_id, t=event.t, gpu=event.gpu, cpu=event.cpu))
                elif isinstance(event, MetricEvent):
                    logger.debug(f"Persisting MetricEvent for {event.session_id}: layer {event.layer}")
                    db.add(Metric(
                        id=event.id, session_id=event.session_id, t=event.t, layer=event.layer,
                        op=event.op, dur_ms=event.dur_ms, shape=event.shape, dtype=event.dtype,
                        device=event.device, level=event.level
                    ))
                elif isinstance(event, ActivationEvent):
                    logger.debug(f"Persisting ActivationEvent for {event.session_id}: layer {event.layer}")
                    db.add(Activation(
                        session_id=event.session_id, layer=event.layer, mean=event.mean,
                        max=event.max, min=event.min, variance=event.variance, sparsity=event.sparsity,
                        nan_count=event.nan_count, inf_count=event.inf_count
                    ))
                elif isinstance(event, AnomalyEvent):
                    logger.debug(f"Persisting AnomalyEvent for {event.session_id}: {event.message}")
                    db.add(Anomaly(
                        id=event.id, session_id=event.session_id, t=event.t,
                        severity=event.severity, layer=event.layer, message=event.message
                    ))
                elif isinstance(event, TopologyEvent):
                    logger.info(f"Persisting TopologyEvent for {event.session_id}")
                    db.add(Topology(
                        session_id=event.session_id, blocks=event.blocks
                    ))
                db.commit()
                
        # Fire and forget database insert, with error logging attached to the task
        task = asyncio.create_task(asyncio.to_thread(_insert))
        def on_done(t):
            try:
                t.result()
            except Exception as e:
                logger.error(f"Database sink error during insert: {e}", exc_info=True)
        task.add_done_callback(on_done)

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
