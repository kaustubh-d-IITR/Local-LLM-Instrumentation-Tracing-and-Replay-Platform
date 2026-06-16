from pydantic import BaseModel

class TopologyBase(BaseModel):
    embedding_layer: str
    transformer_blocks: int
    attention_layers: int
    feed_forward_layers: int
    layer_norm_layers: int

class TopologyResponse(TopologyBase):
    id: int
    session_id: str

    model_config = {"from_attributes": True}
