import asyncio
import time
from typing import Dict, Any, Tuple, AsyncGenerator
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread

# Model Cache to prevent redundant reloads
# Key: model_name, Value: (model, tokenizer)
_MODEL_CACHE: Dict[str, Tuple[Any, Any]] = {}

class ModelRuntime:
    def __init__(self, model_name: str, device: str = None):
        self.model_name = model_name
        # Fallback to cpu if cuda is unavailable
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.tokenizer = None

    async def load_model_async(self) -> None:
        """
        Loads the model asynchronously to prevent blocking the FastAPI event loop.
        Uses the internal cache if the model is already loaded.
        """
        if self.model_name in _MODEL_CACHE:
            self.model, self.tokenizer = _MODEL_CACHE[self.model_name]
            return

        def _load():
            hf_id = self._get_hf_id(self.model_name)
            tokenizer = AutoTokenizer.from_pretrained(hf_id)
            model = AutoModelForCausalLM.from_pretrained(hf_id).to(self.device)
            return model, tokenizer

        self.model, self.tokenizer = await asyncio.to_thread(_load)
        _MODEL_CACHE[self.model_name] = (self.model, self.tokenizer)

    def _get_hf_id(self, name: str) -> str:
        name_lower = name.lower()
        if "gpt2" in name_lower:
            return "gpt2"
        elif "tinyllama" in name_lower:
            return "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        else:
            raise ValueError(f"Unsupported model: {name}. Only GPT-2 and TinyLlama are supported in Phase 2.2.")

    async def stream_generate(self, prompt: str) -> AsyncGenerator[Tuple[int, str, float], None]:
        """
        Generates text using TextIteratorStreamer.
        Yields: (token_idx, token_text, elapsed_ms)
        """
        if not self.model or not self.tokenizer:
            raise RuntimeError("Model not loaded.")

        inputs = self.tokenizer([prompt], return_tensors="pt").to(self.device)
        streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True)
        
        generation_kwargs = dict(
            inputs, 
            streamer=streamer, 
            max_new_tokens=50, 
            do_sample=True,
            top_p=0.9,
            temperature=0.7
        )

        # Run generation in a background thread so it doesn't block the async loop
        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        idx = 0
        start_time = time.time()
        for new_text in streamer:
            # Yield control back to event loop, allowing WS messages to flush
            await asyncio.sleep(0) 
            elapsed_ms = (time.time() - start_time) * 1000.0
            yield idx, new_text, elapsed_ms
            idx += 1
            start_time = time.time() # Reset timer for next token
