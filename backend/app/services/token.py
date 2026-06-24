from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.token import token_repo
from app.models.token import Token

class TokenService:
    @staticmethod
    def get_tokens(db: Session, session_id: str) -> List[Token]:
        tokens = token_repo.get_by_session(db=db, session_id=session_id)
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Service type: {type(tokens)}")
        return tokens

token_service = TokenService()
