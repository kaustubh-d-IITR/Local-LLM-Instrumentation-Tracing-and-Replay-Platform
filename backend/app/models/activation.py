from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Activation(Base):
    __tablename__ = "activations"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    layer_index = Column(Integer, nullable=False)
    mean = Column(Float, nullable=False)
    max_val = Column(Float, nullable=False)
    min_val = Column(Float, nullable=False)
    variance = Column(Float, nullable=False)
    sparsity = Column(Float, nullable=False)

    session = relationship("Session")
