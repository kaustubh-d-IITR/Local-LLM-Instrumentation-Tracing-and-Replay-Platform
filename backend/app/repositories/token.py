from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.token import Token
from app.schemas.token import TokenBase
from app.repositories.base import BaseRepository

import logging

logger = logging.getLogger(__name__)

class TokenRepository(BaseRepository[Token, TokenBase]):
    def get_by_session(self, db: Session, session_id: str) -> List[Token]:
        tokens = (
            db.query(self.model)
            .filter(self.model.session_id == session_id)
            .order_by(self.model.idx)
            .all()
        )
        logger.info(f"Repository type: {type(tokens)}")
        logger.info(f"Repository length: {len(tokens) if isinstance(tokens, list) else 'NOT LIST'}")
        logger.info(f"Retrieved {len(tokens)} token rows")
        return tokens

token_repo = TokenRepository(Token)
