from pydantic import BaseModel

class MetricBase(BaseModel):
    id: str
    t: float
    layer: int
    op: str
    dur_ms: float
    shape: str
    dtype: str
    device: str
    level: str

class MetricResponse(MetricBase):
    session_id: str

    model_config = {"from_attributes": True}
