from sqlalchemy.orm import Session
from app.repositories.session import session_repo
from app.schemas.session import SessionCreate
from app.models.session import Session as SessionModel

class SessionService:
    @staticmethod
    def start_session(db: Session, session_in: SessionCreate) -> SessionModel:
        return session_repo.create(db=db, obj_in=session_in)

session_service = SessionService()
