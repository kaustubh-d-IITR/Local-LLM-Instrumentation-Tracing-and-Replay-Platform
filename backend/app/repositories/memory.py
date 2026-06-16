from typing import List
from sqlalchemy.orm import Session
from app.models.memory import Memory
from app.schemas.memory import MemoryBase
from app.repositories.base import BaseRepository

class MemoryRepository(BaseRepository[Memory, MemoryBase]):
    def get_by_session(self, db: Session, session_id: str) -> List[Memory]:
        return db.query(self.model).filter(self.model.session_id == session_id).all()

memory_repo = MemoryRepository(Memory)
