from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    gpu_memory = Column(Float, nullable=False)
    cpu_memory = Column(Float, nullable=False)
    vram_utilization = Column(Float, nullable=False)

    session = relationship("Session")
