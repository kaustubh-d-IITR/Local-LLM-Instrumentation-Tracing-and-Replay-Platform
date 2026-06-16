from pydantic import BaseModel

class MemoryBase(BaseModel):
    gpu_memory: float
    cpu_memory: float
    vram_utilization: float

class MemoryResponse(MemoryBase):
    id: int
    session_id: str

    model_config = {"from_attributes": True}
