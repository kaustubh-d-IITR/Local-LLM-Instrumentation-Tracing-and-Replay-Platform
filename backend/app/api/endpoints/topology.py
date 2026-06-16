from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.schemas.topology import TopologyResponse
from app.services.topology import topology_service

router = APIRouter()

@router.get("/{session_id}/topology", response_model=TopologyResponse)
def get_topology(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Returns model topology including embedding layer, transformer blocks,
    attention layers, feed forward layers, and layer norm layers.
    """
    topology = topology_service.get_topology(db=db, session_id=session_id)
    if not topology:
        raise HTTPException(status_code=404, detail="Topology not found for this session")
    return topology
