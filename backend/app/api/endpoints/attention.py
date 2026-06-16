from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.attention import AttentionResponse
from app.services.attention import attention_service

router = APIRouter()

@router.get("/{session_id}/attention", response_model=List[AttentionResponse])
def get_attention(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Returns attention matrices.
    """
    return attention_service.get_attention(db=db, session_id=session_id)
