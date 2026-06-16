from typing import List
from sqlalchemy.orm import Session
from app.repositories.attention_summary import attention_summary_repo
from app.models.attention_summary import AttentionSummary

class AttentionSummaryService:
    @staticmethod
    def get_attention_summary(db: Session, session_id: str) -> List[AttentionSummary]:
        return attention_summary_repo.get_by_session(db=db, session_id=session_id)

attention_summary_service = AttentionSummaryService()
