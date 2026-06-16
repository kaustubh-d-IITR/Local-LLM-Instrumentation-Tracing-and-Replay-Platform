from typing import List
from sqlalchemy.orm import Session
from app.repositories.anomaly import anomaly_repo
from app.models.anomaly import Anomaly

class AnomalyService:
    @staticmethod
    def get_anomalies(db: Session, session_id: str) -> List[Anomaly]:
        return anomaly_repo.get_by_session(db=db, session_id=session_id)

anomaly_service = AnomalyService()
