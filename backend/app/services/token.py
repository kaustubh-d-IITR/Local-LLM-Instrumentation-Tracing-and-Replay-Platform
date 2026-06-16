from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.token import token_repo
from app.models.token import Token

class TokenService:
    @staticmethod
    def get_tokens(db: Session, session_id: str) -> Optional[Token]:
        return token_repo.get_by_session(db=db, session_id=session_id)

token_service = TokenService()
