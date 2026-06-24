from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.token import TokenResponse
from app.services.token import token_service

from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/{session_id}/tokens", response_model=List[TokenResponse])
def get_tokens(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Returns token generation timeline.
    """
    try:
        tokens = token_service.get_tokens(db=db, session_id=session_id)
        if tokens is None or len(tokens) == 0:
            logger.info(f"GET /tokens count for {session_id}: 0")
            return []
            
        logger.info(f"TOKEN COUNT: {len(tokens)}")
        # Safe dict conversion for logging avoiding SQLAlchemy state
        if tokens:
            logger.info(f"FIRST TOKEN TYPE: {type(tokens[0])}")
            logger.info(f"FIRST TOKEN ATTRS: {tokens[0].__dict__}")
        
        return tokens
    except Exception:
        logger.exception("TOKENS ENDPOINT FAILURE")
        raise HTTPException(status_code=500, detail="Internal server error")
