from typing import Any, List
from abc import ABC, abstractmethod

class ModelAdapter(ABC):
    """
    Abstract adapter resolving structural differences between models.
    Provides a unified interface to the HookRegistry and TopologyExtractor.
    """
    def __init__(self, model: Any):
        self.model = model

    @abstractmethod
    def get_model_name(self) -> str:
        pass

    @abstractmethod
    def get_embedding_layer(self) -> Any:
        pass

    @abstractmethod
    def get_transformer_blocks(self) -> List[Any]:
        pass

    @abstractmethod
    def get_attention_layers(self) -> List[Any]:
        pass

    @abstractmethod
    def get_mlp_layers(self) -> List[Any]:
        pass

    @abstractmethod
    def get_norm_layers(self) -> List[Any]:
        pass

class LlamaAdapter(ModelAdapter):
    def get_model_name(self) -> str:
        return "Llama"

    def get_embedding_layer(self) -> Any:
        return self.model.model.embed_tokens

    def get_transformer_blocks(self) -> List[Any]:
        return list(self.model.model.layers)

    def get_attention_layers(self) -> List[Any]:
        return [layer.self_attn for layer in self.model.model.layers]

    def get_mlp_layers(self) -> List[Any]:
        return [layer.mlp for layer in self.model.model.layers]

    def get_norm_layers(self) -> List[Any]:
        norms = []
        for layer in self.model.model.layers:
            norms.extend([layer.input_layernorm, layer.post_attention_layernorm])
        norms.append(self.model.model.norm)
        return norms

class MistralAdapter(LlamaAdapter):
    def get_model_name(self) -> str:
        return "Mistral"

class GPT2Adapter(ModelAdapter):
    def get_model_name(self) -> str:
        return "GPT-2"

    def get_embedding_layer(self) -> Any:
        return self.model.transformer.wte

    def get_transformer_blocks(self) -> List[Any]:
        return list(self.model.transformer.h)

    def get_attention_layers(self) -> List[Any]:
        return [block.attn for block in self.model.transformer.h]

    def get_mlp_layers(self) -> List[Any]:
        return [block.mlp for block in self.model.transformer.h]

    def get_norm_layers(self) -> List[Any]:
        norms = []
        for block in self.model.transformer.h:
            norms.extend([block.ln_1, block.ln_2])
        norms.append(self.model.transformer.ln_f)
        return norms
