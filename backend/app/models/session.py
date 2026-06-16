from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.models.base import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)
    model_name = Column(String, index=True, nullable=False)
    prompt = Column(String, nullable=False)
    status = Column(String, nullable=False, default="started")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
