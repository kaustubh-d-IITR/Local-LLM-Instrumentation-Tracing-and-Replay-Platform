from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.session import SessionCreate, SessionResponse
from app.services.session import session_service

router = APIRouter()

@router.post("/start", response_model=SessionResponse)
def start_session(
    session_in: SessionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Creates an inference tracing session.
    """
    return session_service.start_session(db=db, session_in=session_in, background_tasks=background_tasks)



