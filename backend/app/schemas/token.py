from pydantic import BaseModel

class TokenBase(BaseModel):
    idx: int
    token: str
    ms: float

class TokenResponse(TokenBase):
    id: int
    session_id: str

    model_config = {"from_attributes": True, "populate_by_name": True}
