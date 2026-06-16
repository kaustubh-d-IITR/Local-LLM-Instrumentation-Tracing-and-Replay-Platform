from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Anomaly(Base):
    __tablename__ = "anomalies"

    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    t = Column(Float, nullable=False)
    severity = Column(String, nullable=False)
    layer = Column(Integer, nullable=False)
    message = Column(String, nullable=False)

    session = relationship("Session")
