from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.session import SessionCreate, SessionResponse
from app.services.session import session_service

router = APIRouter()

@router.post("/start", response_model=SessionResponse)
def start_session(
    session_in: SessionCreate,
    db: Session = Depends(get_db)
):
    """
    Creates an inference tracing session.
    """
    return session_service.start_session(db=db, session_in=session_in)

@router.get("/{session_id}/topology")
def get_topology(session_id: str):
    """
    Returns the real-time topology extracted from the loaded model.
    """
    return session_service.get_topology(session_id)

