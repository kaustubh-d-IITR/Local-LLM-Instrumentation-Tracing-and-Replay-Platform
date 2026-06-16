from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class TelemetrySnapshot(Base):
    __tablename__ = "telemetry_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    token_idx = Column(Integer, nullable=False)
    layer_index = Column(Integer, nullable=False)
    timestamp = Column(Float, nullable=False)

    session = relationship("Session")
