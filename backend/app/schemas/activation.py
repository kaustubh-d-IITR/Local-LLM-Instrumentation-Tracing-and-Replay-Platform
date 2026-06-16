from pydantic import BaseModel

class ActivationBase(BaseModel):
    layer: int
    mean: float
    max: float
    min: float
    variance: float
    sparsity: float

class ActivationResponse(ActivationBase):
    id: int
    session_id: str

    model_config = {"from_attributes": True}
