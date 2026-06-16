from fastapi import APIRouter
from app.api.endpoints import (
    sessions,
    topology,
    metrics,
    activations,
    anomalies,
    memory,
    tokens,
    ws,
    health
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
api_router.include_router(topology.router, prefix="/sessions", tags=["topology"])
api_router.include_router(metrics.router, prefix="/sessions", tags=["metrics"])
api_router.include_router(activations.router, prefix="/sessions", tags=["activations"])
api_router.include_router(anomalies.router, prefix="/sessions", tags=["anomalies"])
api_router.include_router(memory.router, prefix="/sessions", tags=["memory"])
api_router.include_router(tokens.router, prefix="/sessions", tags=["tokens"])
api_router.include_router(ws.router, prefix="/ws", tags=["websocket"])
