from typing import List
from sqlalchemy.orm import Session
from app.repositories.metric import metric_repo
from app.models.metric import Metric

class MetricService:
    @staticmethod
    def get_metrics(db: Session, session_id: str) -> List[Metric]:
        return metric_repo.get_by_session(db=db, session_id=session_id)

metric_service = MetricService()
