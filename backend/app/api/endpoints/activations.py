from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.activation import ActivationResponse
from app.services.activation import activation_service

router = APIRouter()

@router.get("/{session_id}/activations", response_model=List[ActivationResponse])
def get_activations(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Returns mean, max, min, variance, sparsity for each layer.
    """
    return activation_service.get_activations(db=db, session_id=session_id)
