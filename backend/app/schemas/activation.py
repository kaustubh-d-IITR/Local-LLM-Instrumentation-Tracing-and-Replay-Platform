from pydantic import BaseModel

class ActivationBase(BaseModel):
    layer_index: int
    mean: float
    max_val: float
    min_val: float
    variance: float
    sparsity: float

class ActivationResponse(ActivationBase):
    id: int
    session_id: str

    model_config = {"from_attributes": True}
