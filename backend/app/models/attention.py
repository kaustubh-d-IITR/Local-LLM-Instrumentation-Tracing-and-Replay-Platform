from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.models.base import Base

class Attention(Base):
    __tablename__ = "attentions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    layer_index = Column(Integer, nullable=False)
    matrices = Column(JSONB, nullable=False)

    session = relationship("Session")
