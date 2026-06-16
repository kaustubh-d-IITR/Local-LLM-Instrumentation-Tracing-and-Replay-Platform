from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Anomaly(Base):
    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    activation_spikes = Column(Integer, nullable=False, default=0)
    cpu_fallback = Column(Boolean, nullable=False, default=False)
    memory_warnings = Column(Integer, nullable=False, default=0)
    latency_warnings = Column(Integer, nullable=False, default=0)

    session = relationship("Session")
