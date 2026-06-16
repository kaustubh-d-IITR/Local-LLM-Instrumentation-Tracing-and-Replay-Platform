from typing import List
from sqlalchemy.orm import Session
from app.repositories.base import CRUDBase
from app.models.attention_summary import AttentionSummary
from app.schemas.attention_summary import AttentionSummaryResponse, AttentionSummaryBase

class CRUDAttentionSummary(CRUDBase[AttentionSummary, AttentionSummaryBase, AttentionSummaryBase]):
    def get_by_session(self, db: Session, session_id: str) -> List[AttentionSummary]:
        return db.query(AttentionSummary).filter(AttentionSummary.session_id == session_id).all()

attention_summary_repo = CRUDAttentionSummary(AttentionSummary)
