from pydantic import BaseModel

class AnomalyBase(BaseModel):
    id: str
    t: float
    severity: str
    layer: int
    message: str

class AnomalyResponse(AnomalyBase):
    session_id: str

    model_config = {"from_attributes": True}
