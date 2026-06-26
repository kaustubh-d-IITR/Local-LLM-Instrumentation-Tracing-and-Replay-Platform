import asyncio
import time
import os
import traceback
from typing import Dict, Any, Tuple, AsyncGenerator
from threading import Thread
import logging

logger = logging.getLogger(__name__)

# Model Cache to prevent redundant reloads
# Key: model_name, Value: (model, tokenizer)
_MODEL_CACHE: Dict[str, Tuple[Any, Any]] = {}


def _get_memory_mb() -> float:
    """Return current process RSS in MB. Returns 0 if psutil unavailable."""
    try:
        import psutil
        return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
    except Exception:
        return 0.0


class ModelRuntime:
    def __init__(self, model_name: str, device: str = None):
        self.model_name = model_name
        self.device = device
        self.model = None
        self.tokenizer = None

    async def load_model_async(self) -> None:
        """
        Loads the model asynchronously to prevent blocking the FastAPI event loop.
        Uses the internal cache if the model is already loaded.
        """
        logger.info(f"[LOAD] Entering load_model_async for model={self.model_name}")

        if self.model_name in _MODEL_CACHE:
            logger.info(f"[LOAD] Cache HIT for {self.model_name}, skipping download")
            self.model, self.tokenizer = _MODEL_CACHE[self.model_name]
            return

        logger.info(f"[LOAD] Cache MISS for {self.model_name}, will load from HuggingFace")

        def _load():
            # --- Step 1: Import ML dependencies ---
            logger.info("[LOAD STEP 1] Importing torch and transformers...")
            try:
                import torch
                from transformers import AutoModelForCausalLM, AutoTokenizer
                logger.info(f"[LOAD STEP 1] torch={torch.__version__}, transformers imported OK")
            except ImportError as e:
                logger.exception(f"[LOAD STEP 1] FAILED to import ML dependencies")
                raise RuntimeError(f"ML dependencies (torch, transformers) are missing: {e}")

            # --- Step 2: Resolve device ---
            logger.info(f"[LOAD STEP 2] Resolving device (current self.device={self.device})")
            try:
                if self.device is None:
                    self.device = "cuda" if torch.cuda.is_available() else "cpu"
                logger.info(f"[LOAD STEP 2] Resolved device={self.device}, cuda_available={torch.cuda.is_available()}")
            except Exception as e:
                logger.exception(f"[LOAD STEP 2] FAILED resolving device, mem={_get_memory_mb():.1f}MB")
                raise

            # --- Step 3: Resolve HF model id ---
            logger.info(f"[LOAD STEP 3] Resolving HuggingFace model ID for '{self.model_name}'")
            try:
                hf_id = self._get_hf_id(self.model_name)
                logger.info(f"[LOAD STEP 3] Resolved hf_id={hf_id}")
            except Exception as e:
                logger.exception(f"[LOAD STEP 3] FAILED resolving HF ID, mem={_get_memory_mb():.1f}MB")
                raise

            # --- Step 4: Memory before loading ---
            mem_before = _get_memory_mb()
            logger.info(f"[LOAD STEP 4] MEMORY BEFORE LOAD: {mem_before:.1f} MB")

            # --- Step 5: Load tokenizer ---
            logger.info(f"[LOAD STEP 5] Loading tokenizer for {hf_id}...")
            try:
                tokenizer = AutoTokenizer.from_pretrained(hf_id)
                mem_after_tok = _get_memory_mb()
                logger.info(f"[LOAD STEP 5] Tokenizer loaded OK. Memory: {mem_after_tok:.1f} MB (+{mem_after_tok - mem_before:.1f} MB)")
            except Exception as e:
                logger.exception(f"[LOAD STEP 5] FAILED loading tokenizer, mem={_get_memory_mb():.1f}MB, device={self.device}")
                raise

            # --- Step 6: Load model weights (from_pretrained) ---
            logger.info(f"[LOAD STEP 6] Calling AutoModelForCausalLM.from_pretrained('{hf_id}', torch_dtype=bfloat16, low_cpu_mem_usage=True)...")
            try:
                model = AutoModelForCausalLM.from_pretrained(
                    hf_id,
                    torch_dtype=torch.bfloat16,
                    low_cpu_mem_usage=True
                )
                mem_after_load = _get_memory_mb()
                logger.info(f"[LOAD STEP 6] from_pretrained() completed. Memory: {mem_after_load:.1f} MB (+{mem_after_load - mem_before:.1f} MB)")
            except Exception as e:
                logger.exception(f"[LOAD STEP 6] FAILED from_pretrained(), mem={_get_memory_mb():.1f}MB, device={self.device}")
                raise

            # --- Step 7: Move model to device ---
            logger.info(f"[LOAD STEP 7] Moving model to device={self.device}...")
            try:
                model = model.to(self.device)
                mem_after_to = _get_memory_mb()
                logger.info(f"[LOAD STEP 7] model.to({self.device}) completed. Memory: {mem_after_to:.1f} MB")
            except Exception as e:
                logger.exception(f"[LOAD STEP 7] FAILED model.to({self.device}), mem={_get_memory_mb():.1f}MB")
                raise

            # --- Step 8: Set eval mode ---
            logger.info("[LOAD STEP 8] Setting model.eval()...")
            try:
                model.eval()
                logger.info("[LOAD STEP 8] model.eval() completed")
            except Exception as e:
                logger.exception(f"[LOAD STEP 8] FAILED model.eval(), mem={_get_memory_mb():.1f}MB")
                raise

            mem_final = _get_memory_mb()
            logger.info(f"[LOAD COMPLETE] Model {hf_id} loaded successfully. Final memory: {mem_final:.1f} MB (delta: +{mem_final - mem_before:.1f} MB)")
            return model, tokenizer

        logger.info("[LOAD] Dispatching _load() to thread executor via asyncio.to_thread...")
        try:
            self.model, self.tokenizer = await asyncio.to_thread(_load)
        except Exception as e:
            logger.exception(f"[LOAD] asyncio.to_thread(_load) raised exception")
            raise

        # --- Step 9: Cache the model ---
        _MODEL_CACHE[self.model_name] = (self.model, self.tokenizer)
        logger.info(f"[LOAD STEP 9] Model cached under key '{self.model_name}'. Cache size={len(_MODEL_CACHE)}")
        logger.info(f"[LOAD] Returning from load_model_async. mem={_get_memory_mb():.1f}MB")

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

        try:
            from transformers import TextIteratorStreamer
        except ImportError:
            raise RuntimeError("ML dependencies are missing.")

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

        # We must use a thread executor to pull from the streamer
        # so we don't block the main asyncio event loop!
        while True:
            try:
                # next() blocks on a threading.Condition, so we offload it
                new_text = await asyncio.to_thread(next, streamer)
                elapsed_ms = (time.time() - start_time) * 1000.0
                yield idx, new_text, elapsed_ms
                idx += 1
                start_time = time.time()
            except StopIteration:
                break
