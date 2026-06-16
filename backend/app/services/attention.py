from typing import List
from sqlalchemy.orm import Session
from app.repositories.attention import attention_repo
from app.models.attention import Attention

class AttentionService:
    @staticmethod
    def get_attention(db: Session, session_id: str) -> List[Attention]:
        return attention_repo.get_by_session(db=db, session_id=session_id)

attention_service = AttentionService()
