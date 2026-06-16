from pydantic import BaseModel
from typing import Any

class TopologyBase(BaseModel):
    blocks: list[Any]

class TopologyResponse(TopologyBase):
    id: int
    session_id: str

    model_config = {"from_attributes": True}
