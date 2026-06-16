from pydantic import BaseModel

class AttentionSummaryBase(BaseModel):
    layer: int
    head: int
    entropy: float
    max_weight: float

class AttentionSummaryResponse(AttentionSummaryBase):
    id: int
    session_id: str

    model_config = {"from_attributes": True}
