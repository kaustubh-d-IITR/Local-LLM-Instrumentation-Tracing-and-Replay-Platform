from pydantic import BaseModel

class MetricBase(BaseModel):
    block_index: int
    latency: float
    tensor_shape: str
    device: str
    dtype: str

class MetricResponse(MetricBase):
    id: int
    session_id: str

    model_config = {"from_attributes": True}
