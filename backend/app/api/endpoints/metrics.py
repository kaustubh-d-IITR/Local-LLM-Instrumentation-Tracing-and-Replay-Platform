from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.metric import MetricResponse
from app.services.metric import metric_service

router = APIRouter()

@router.get("/{session_id}/metrics", response_model=List[MetricResponse])
def get_metrics(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Returns runtime metrics like latency, tensor shape, device, dtype
    for every transformer block.
    """
    return metric_service.get_metrics(db=db, session_id=session_id)
