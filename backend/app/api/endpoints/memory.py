from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.memory import MemoryResponse
from app.services.memory import memory_service

router = APIRouter()

@router.get("/{session_id}/memory", response_model=List[MemoryResponse])
def get_memory(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Returns GPU memory, CPU memory, VRAM utilization.
    """
    return memory_service.get_memory(db=db, session_id=session_id)
