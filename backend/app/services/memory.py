from typing import List
from sqlalchemy.orm import Session
from app.repositories.memory import memory_repo
from app.models.memory import Memory

class MemoryService:
    @staticmethod
    def get_memory(db: Session, session_id: str) -> List[Memory]:
        return memory_repo.get_by_session(db=db, session_id=session_id)

memory_service = MemoryService()
