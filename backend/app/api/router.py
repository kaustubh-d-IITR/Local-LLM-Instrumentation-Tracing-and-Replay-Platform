from fastapi import APIRouter
from app.api.endpoints import (
    sessions,
    topology,
    metrics,
    attention,
    activations,
    anomalies,
    memory,
    tokens
)

api_router = APIRouter()

api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
api_router.include_router(topology.router, prefix="/sessions", tags=["topology"])
api_router.include_router(metrics.router, prefix="/sessions", tags=["metrics"])
api_router.include_router(attention.router, prefix="/sessions", tags=["attention"])
api_router.include_router(activations.router, prefix="/sessions", tags=["activations"])
api_router.include_router(anomalies.router, prefix="/sessions", tags=["anomalies"])
api_router.include_router(memory.router, prefix="/sessions", tags=["memory"])
api_router.include_router(tokens.router, prefix="/sessions", tags=["tokens"])
