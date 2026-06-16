from typing import Optional
from sqlalchemy.orm import Session
from app.models.token import Token
from app.schemas.token import TokenBase
from app.repositories.base import BaseRepository

class TokenRepository(BaseRepository[Token, TokenBase]):
    def get_by_session(self, db: Session, session_id: str) -> Optional[Token]:
        return db.query(self.model).filter(self.model.session_id == session_id).first()

token_repo = TokenRepository(Token)
