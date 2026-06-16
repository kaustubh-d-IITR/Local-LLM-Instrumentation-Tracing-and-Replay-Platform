from typing import Dict, Any, List
from .adapters import ModelAdapter

class TopologyExtractor:
    """
    Traverses the ModelAdapter to generate a UI-friendly topology representation.
    """
    def __init__(self, adapter: ModelAdapter):
        self.adapter = adapter

    def extract(self) -> Dict[str, Any]:
        """
        Returns a dictionary representing the topology, compatible with
        the frontend `TopologyBlock[]` array mapped to JSONB.
        """
        # Validate count dynamically based on the model's actual config
        # Different models have different config attributes (e.g. n_layer for GPT-2, num_hidden_layers for Llama)
        config = self.adapter.model.config
        num_layers = getattr(config, "num_hidden_layers", getattr(config, "n_layer", 0))
        
        topology_blocks: List[Dict[str, Any]] = []
        
        # We loop up to num_layers to dynamically represent the model's structure
        for i in range(num_layers):
            topology_blocks.append({
                "index": i,
                "name": f"block.{i}",
                "components": [
                    {"name": "input_norm", "kind": "norm"},
                    {"name": "self_attn", "kind": "attn"},
                    {"name": "post_norm", "kind": "norm"},
                    {"name": "mlp", "kind": "mlp"}
                ],
                "status": "ok"
            })
            
        return {
            "blocks": topology_blocks
        }
