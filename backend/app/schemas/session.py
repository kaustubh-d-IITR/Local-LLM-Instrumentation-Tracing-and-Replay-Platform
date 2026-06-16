from pydantic import BaseModel
from datetime import datetime

class SessionBase(BaseModel):
    model_name: str
    prompt: str

class SessionCreate(SessionBase):
    pass

class SessionResponse(SessionBase):
    id: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
