from pydantic import BaseModel
from typing import Any, Dict

class AttentionBase(BaseModel):
    layer_index: int
    matrices: list[Any] | Dict[str, Any]

class AttentionResponse(AttentionBase):
    id: int
    session_id: str

    model_config = {"from_attributes": True}
