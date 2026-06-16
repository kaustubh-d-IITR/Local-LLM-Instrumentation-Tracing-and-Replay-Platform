from typing import List
from sqlalchemy.orm import Session
from app.models.attention import Attention
from app.schemas.attention import AttentionBase
from app.repositories.base import BaseRepository

class AttentionRepository(BaseRepository[Attention, AttentionBase]):
    def get_by_session(self, db: Session, session_id: str) -> List[Attention]:
        return db.query(self.model).filter(self.model.session_id == session_id).all()

attention_repo = AttentionRepository(Attention)
