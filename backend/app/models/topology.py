from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Topology(Base):
    __tablename__ = "topologies"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), unique=True, nullable=False)
    embedding_layer = Column(String, nullable=False)
    transformer_blocks = Column(Integer, nullable=False)
    attention_layers = Column(Integer, nullable=False)
    feed_forward_layers = Column(Integer, nullable=False)
    layer_norm_layers = Column(Integer, nullable=False)

    session = relationship("Session")
