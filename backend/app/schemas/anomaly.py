from pydantic import BaseModel

class AnomalyBase(BaseModel):
    activation_spikes: int
    cpu_fallback: bool
    memory_warnings: int
    latency_warnings: int

class AnomalyResponse(AnomalyBase):
    id: int
    session_id: str

    model_config = {"from_attributes": True}
