from pydantic import BaseModel
from typing import Any

class TokenBase(BaseModel):
    timeline: list[Any]

class TokenResponse(TokenBase):
    id: int
    session_id: str

    model_config = {"from_attributes": True}
