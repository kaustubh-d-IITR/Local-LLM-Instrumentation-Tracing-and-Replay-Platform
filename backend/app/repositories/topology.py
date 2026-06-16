from typing import Optional
from sqlalchemy.orm import Session
from app.models.topology import Topology
from app.schemas.topology import TopologyBase
from app.repositories.base import BaseRepository

class TopologyRepository(BaseRepository[Topology, TopologyBase]):
    def get_by_session(self, db: Session, session_id: str) -> Optional[Topology]:
        return db.query(self.model).filter(self.model.session_id == session_id).first()

topology_repo = TopologyRepository(Topology)
