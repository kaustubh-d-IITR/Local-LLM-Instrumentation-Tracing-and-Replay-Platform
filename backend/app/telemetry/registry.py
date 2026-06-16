from typing import Any, List
from .context import TelemetryContext
from .aggregator import TelemetryAggregator
from .adapters import ModelAdapter
from .hooks.latency import LatencyHook
from .hooks.activation import ActivationHook
from .hooks.stability import NumericalStabilityHook

class HookRegistry:
    """
    Manages the lifecycle of PyTorch forward/backward hooks.
    """
    def __init__(self, context: TelemetryContext, adapter: ModelAdapter, aggregator: TelemetryAggregator):
        self.context = context
        self.adapter = adapter
        self.aggregator = aggregator
        self.active_hooks: List[Any] = []  # Will store torch.utils.hooks.RemovableHandle

    def attach_all(self):
        # 1. Attach Latency Hooks to Transformer Blocks
        for idx, block in enumerate(self.adapter.get_transformer_blocks()):
            h = LatencyHook(self.context.session_id, idx, f"block.{idx}", "transformer_block", self.aggregator)
            self.active_hooks.append(block.register_forward_pre_hook(h.pre_hook))
            self.active_hooks.append(block.register_forward_hook(h.hook))

        # 2. Attach Activation and Stability Hooks to MLPs
        for idx, mlp in enumerate(self.adapter.get_mlp_layers()):
            # Activation Hook
            a_hook = ActivationHook(self.context.session_id, idx, f"mlp.{idx}", "mlp", self.aggregator)
            self.active_hooks.append(mlp.register_forward_hook(a_hook.hook))
            
            # Stability Hook
            s_hook = NumericalStabilityHook(self.context.session_id, idx, f"mlp.{idx}", "mlp", self.aggregator)
            self.active_hooks.append(mlp.register_forward_hook(s_hook.hook))
            
        # Optional: Can attach to norm layers if required by config, but MLPs cover the spec requirement for now.
        for idx, norm in enumerate(self.adapter.get_norm_layers()):
            s_hook = NumericalStabilityHook(self.context.session_id, idx, f"norm.{idx}", "norm", self.aggregator)
            self.active_hooks.append(norm.register_forward_hook(s_hook.hook))

    def remove_all_hooks(self) -> None:
        """
        Removes all registered hooks from the model.
        """
        for hook in self.active_hooks:
            hook.remove()
        self.active_hooks.clear()
