from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.token import TokenResponse
from app.services.token import token_service

router = APIRouter()

@router.get("/{session_id}/tokens", response_model=TokenResponse)
def get_tokens(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Returns token generation timeline.
    """
    tokens = token_service.get_tokens(db=db, session_id=session_id)
    if not tokens:
        raise HTTPException(status_code=404, detail="Tokens timeline not found for this session")
    return tokens
