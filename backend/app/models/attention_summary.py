from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class AttentionSummary(Base):
    __tablename__ = "attention_summaries"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    layer = Column(Integer, nullable=False)
    head = Column(Integer, nullable=False)
    entropy = Column(Float, nullable=False)
    max_weight = Column(Float, nullable=False)

    session = relationship("Session")
