from pydantic import BaseModel

class MemoryBase(BaseModel):
    t: float
    gpu: float
    cpu: float

class MemoryResponse(MemoryBase):
    id: int
    session_id: str

    model_config = {"from_attributes": True}
