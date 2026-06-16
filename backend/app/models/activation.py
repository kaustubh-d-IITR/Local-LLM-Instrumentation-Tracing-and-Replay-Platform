from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Activation(Base):
    __tablename__ = "activations"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    layer = Column(Integer, nullable=False)
    mean = Column(Float, nullable=False)
    max = Column(Float, nullable=False)
    min = Column(Float, nullable=False)
    variance = Column(Float, nullable=False)
    sparsity = Column(Float, nullable=False)
    nan_count = Column(Integer, nullable=False, default=0)
    inf_count = Column(Integer, nullable=False, default=0)

    session = relationship("Session")
