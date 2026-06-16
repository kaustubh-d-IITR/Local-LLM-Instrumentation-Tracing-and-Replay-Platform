from pydantic import BaseModel

class TelemetrySnapshotBase(BaseModel):
    token_idx: int
    layer_index: int
    timestamp: float

class TelemetrySnapshotResponse(TelemetrySnapshotBase):
    id: int
    session_id: str

    model_config = {"from_attributes": True}
