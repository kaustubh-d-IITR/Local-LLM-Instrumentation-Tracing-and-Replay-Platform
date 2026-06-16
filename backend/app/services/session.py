import asyncio
from typing import Dict
from sqlalchemy.orm import Session
from app.repositories.session import session_repo
from app.schemas.session import SessionCreate
from app.models.session import Session as SessionModel
from app.telemetry.session import SessionManager

# Global dictionary of active session managers
active_managers: Dict[str, SessionManager] = {}

class SessionService:
    @staticmethod
    def start_session(db: Session, session_in: SessionCreate) -> SessionModel:
        # Create DB record
        db_session = session_repo.create(db=db, obj_in=session_in)
        
        # Instantiate telemetry pipeline
        manager = SessionManager(
            session_id=db_session.id, 
            model_name=session_in.model_name
        )
        active_managers[db_session.id] = manager
        
        # Start async background task for model loading and generation
        asyncio.create_task(manager.start_async(session_in.prompt))
        
        # Set status to starting and return immediately
        db_session.status = "starting"
        db.commit()
        
        return db_session

    @staticmethod
    def get_topology(session_id: str) -> dict:
        if session_id in active_managers and active_managers[session_id].topology_extractor:
            return active_managers[session_id].topology_extractor.extract()
        return {"blocks": []}

session_service = SessionService()

