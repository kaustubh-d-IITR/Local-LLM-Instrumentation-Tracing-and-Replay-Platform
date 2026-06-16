from typing import List
from sqlalchemy.orm import Session
from app.models.activation import Activation
from app.schemas.activation import ActivationBase
from app.repositories.base import BaseRepository

class ActivationRepository(BaseRepository[Activation, ActivationBase]):
    def get_by_session(self, db: Session, session_id: str) -> List[Activation]:
        return db.query(self.model).filter(self.model.session_id == session_id).all()

activation_repo = ActivationRepository(Activation)
