from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    block_index = Column(Integer, nullable=False)
    latency = Column(Float, nullable=False)
    tensor_shape = Column(String, nullable=False)
    device = Column(String, nullable=False)
    dtype = Column(String, nullable=False)

    session = relationship("Session")
