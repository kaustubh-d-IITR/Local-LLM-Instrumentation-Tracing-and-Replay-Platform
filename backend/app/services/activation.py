from typing import List
from sqlalchemy.orm import Session
from app.repositories.activation import activation_repo
from app.models.activation import Activation

class ActivationService:
    @staticmethod
    def get_activations(db: Session, session_id: str) -> List[Activation]:
        return activation_repo.get_by_session(db=db, session_id=session_id)

activation_service = ActivationService()
