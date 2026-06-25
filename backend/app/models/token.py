from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    idx = Column(Integer, nullable=False)
    token = Column(String, nullable=False)
    ms = Column(Float, nullable=False)

    session = relationship("Session")
