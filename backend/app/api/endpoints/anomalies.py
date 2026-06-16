from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.anomaly import AnomalyResponse
from app.services.anomaly import anomaly_service

router = APIRouter()

@router.get("/{session_id}/anomalies", response_model=List[AnomalyResponse])
def get_anomalies(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Returns activation spikes, cpu fallback, memory warnings, latency warnings.
    """
    return anomaly_service.get_anomalies(db=db, session_id=session_id)
