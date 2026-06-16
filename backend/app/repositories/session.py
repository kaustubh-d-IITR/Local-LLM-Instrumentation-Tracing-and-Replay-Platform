from typing import Optional
from sqlalchemy.orm import Session
from app.models.session import Session as SessionModel
from app.schemas.session import SessionCreate
from app.repositories.base import BaseRepository
import uuid

class SessionRepository(BaseRepository[SessionModel, SessionCreate]):
    def create(self, db: Session, *, obj_in: SessionCreate) -> SessionModel:
        # Generate custom UUID for session
        db_obj = SessionModel(
            id=str(uuid.uuid4()),
            model_name=obj_in.model_name,
            prompt=obj_in.prompt
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

session_repo = SessionRepository(SessionModel)
