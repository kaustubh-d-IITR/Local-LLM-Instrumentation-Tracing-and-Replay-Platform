from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.topology import topology_repo
from app.models.topology import Topology

class TopologyService:
    @staticmethod
    def get_topology(db: Session, session_id: str) -> Optional[Topology]:
        return topology_repo.get_by_session(db=db, session_id=session_id)

topology_service = TopologyService()
