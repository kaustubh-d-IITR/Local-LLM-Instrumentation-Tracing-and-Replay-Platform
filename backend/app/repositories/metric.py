from typing import List
from sqlalchemy.orm import Session
from app.models.metric import Metric
from app.schemas.metric import MetricBase
from app.repositories.base import BaseRepository

class MetricRepository(BaseRepository[Metric, MetricBase]):
    def get_by_session(self, db: Session, session_id: str) -> List[Metric]:
        return db.query(self.model).filter(self.model.session_id == session_id).all()

metric_repo = MetricRepository(Metric)
