from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(String, primary_key=True, index=True) # use string ID like ev_1
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    t = Column(Float, nullable=False)
    layer = Column(Integer, nullable=False)
    op = Column(String, nullable=False)
    dur_ms = Column(Float, nullable=False)
    shape = Column(String, nullable=False)
    dtype = Column(String, nullable=False)
    device = Column(String, nullable=False)
    level = Column(String, nullable=False)

    session = relationship("Session")
