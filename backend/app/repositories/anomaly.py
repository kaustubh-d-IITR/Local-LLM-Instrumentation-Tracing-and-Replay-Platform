from typing import List
from sqlalchemy.orm import Session
from app.models.anomaly import Anomaly
from app.schemas.anomaly import AnomalyBase
from app.repositories.base import BaseRepository

class AnomalyRepository(BaseRepository[Anomaly, AnomalyBase]):
    def get_by_session(self, db: Session, session_id: str) -> List[Anomaly]:
        return db.query(self.model).filter(self.model.session_id == session_id).all()

anomaly_repo = AnomalyRepository(Anomaly)
