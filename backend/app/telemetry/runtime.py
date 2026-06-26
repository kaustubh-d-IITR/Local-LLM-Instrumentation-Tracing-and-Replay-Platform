import asyncio
import time
import os
import gc
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


def _get_available_mb() -> float:
    """Return system available memory in MB."""
    try:
        import psutil
        return psutil.virtual_memory().available / (1024 * 1024)
    except Exception:
        return 0.0


class ModelRuntime:
    def __init__(self, model_name: str, device: str = None):
        self.model_name = model_name
        self.device = device or "cpu"
        self.model = None
        self.tokenizer = None

    async def load_model_async(self) -> None:
        """
        Loads the model asynchronously via asyncio.to_thread.
        Uses low_cpu_mem_usage=True to load weights one-at-a-time,
        keeping peak memory lower than a full state_dict load.
        """
        logger.info(f"[LOAD] Entering load_model_async model={self.model_name}")

        if self.model_name in _MODEL_CACHE:
            logger.info(f"[LOAD] Cache HIT for '{self.model_name}', skipping load")
            self.model, self.tokenizer = _MODEL_CACHE[self.model_name]
            return

        logger.info(f"[LOAD] Cache MISS for '{self.model_name}', loading from HuggingFace")

        def _load():
            # ── Step 1: Import ML dependencies ──────────────────────────
            logger.info("[STEP 1] Importing torch and transformers...")
            try:
                import torch
                from transformers import AutoModelForCausalLM, AutoTokenizer
                logger.info(
                    f"[STEP 1] OK  torch={torch.__version__}  "
                    f"cuda={torch.cuda.is_available()}  "
                    f"mem={_get_memory_mb():.0f}MB"
                )
            except ImportError:
                logger.exception("[STEP 1] FAILED — ML dependencies missing")
                raise

            # ── Step 2: Resolve device ──────────────────────────────────
            logger.info(f"[STEP 2] Resolving device (current={self.device})...")
            try:
                if self.device is None:
                    self.device = "cuda" if torch.cuda.is_available() else "cpu"
                logger.info(f"[STEP 2] OK  device={self.device}")
            except Exception:
                logger.exception(f"[STEP 2] FAILED  mem={_get_memory_mb():.0f}MB")
                raise

            # ── Step 3: Resolve HuggingFace model ID ────────────────────
            logger.info(f"[STEP 3] Resolving HF ID for '{self.model_name}'...")
            try:
                hf_id = self._get_hf_id(self.model_name)
                logger.info(f"[STEP 3] OK  hf_id={hf_id}")
            except Exception:
                logger.exception(f"[STEP 3] FAILED  mem={_get_memory_mb():.0f}MB")
                raise

            # ── Step 4: Pre-load memory snapshot ────────────────────────
            rss = _get_memory_mb()
            avail = _get_available_mb()
            logger.info(
                f"[STEP 4] MEMORY SNAPSHOT  RSS={rss:.0f}MB  "
                f"system_available={avail:.0f}MB"
            )

            # Free any garbage before the heavy allocation
            gc.collect()

            # ── Step 5: Load tokenizer ──────────────────────────────────
            logger.info(f"[STEP 5] Loading tokenizer for '{hf_id}'...")
            try:
                tokenizer = AutoTokenizer.from_pretrained(hf_id)
                logger.info(f"[STEP 5] OK  mem={_get_memory_mb():.0f}MB")
            except Exception:
                logger.exception(f"[STEP 5] FAILED  mem={_get_memory_mb():.0f}MB")
                raise

            # ── Step 6: Load model ──────────────────────────────────────
            #
            # Strategy: load directly onto CPU with low_cpu_mem_usage=True.
            # This creates the model skeleton on meta device, then loads
            # each parameter individually from safetensors → CPU, avoiding
            # the 2x peak memory of a full state_dict load.
            #
            # torch.float32 = native safetensors format → no conversion.
            #
            # We do NOT use device_map="auto" because accelerate's auto
            # device map with max_memory leaves parameters on meta device
            # when CPU budget is too small, causing:
            #   "Tensor.item() cannot be called on meta tensors"
            #
            logger.info(
                f"[STEP 6] AutoModelForCausalLM.from_pretrained('{hf_id}', "
                f"torch_dtype=float32, low_cpu_mem_usage=True)..."
            )
            try:
                model = AutoModelForCausalLM.from_pretrained(
                    hf_id,
                    torch_dtype=torch.float32,
                    low_cpu_mem_usage=True,
                )
                logger.info(f"[STEP 6] from_pretrained() OK  mem={_get_memory_mb():.0f}MB")
            except Exception:
                logger.exception(f"[STEP 6] FAILED  mem={_get_memory_mb():.0f}MB")
                raise

            # ── Step 7: Move to device ──────────────────────────────────
            logger.info(f"[STEP 7] model.to('{self.device}')...")
            try:
                model = model.to(self.device)
                logger.info(f"[STEP 7] OK  mem={_get_memory_mb():.0f}MB")
            except Exception:
                logger.exception(f"[STEP 7] FAILED  mem={_get_memory_mb():.0f}MB")
                raise

            # ── Step 8: Eval mode ───────────────────────────────────────
            logger.info("[STEP 8] model.eval()...")
            try:
                model.eval()
                logger.info(f"[STEP 8] OK  mem={_get_memory_mb():.0f}MB")
            except Exception:
                logger.exception(f"[STEP 8] FAILED  mem={_get_memory_mb():.0f}MB")
                raise

            # ── Step 9: Verify parameters are NOT on meta ───────────────
            first_param = next(model.parameters())
            param_device = str(first_param.device)
            logger.info(f"[STEP 9] First parameter device: {param_device}")
            if param_device == "meta":
                raise RuntimeError(
                    f"Model parameters are on 'meta' device after loading. "
                    f"This means weights were never materialized."
                )

            mem_final = _get_memory_mb()
            logger.info(
                f"[LOAD COMPLETE] {hf_id} ready on {param_device}.  "
                f"Final RSS={mem_final:.0f}MB  delta=+{mem_final - rss:.0f}MB"
            )
            return model, tokenizer

        # Dispatch blocking _load() to a thread so the event loop stays free
        logger.info("[LOAD] Dispatching _load() via asyncio.to_thread...")
        try:
            self.model, self.tokenizer = await asyncio.to_thread(_load)
        except Exception:
            logger.exception("[LOAD] asyncio.to_thread(_load) raised")
            raise

        # ── Step 10: Cache the loaded model ─────────────────────────────
        _MODEL_CACHE[self.model_name] = (self.model, self.tokenizer)
        logger.info(
            f"[STEP 10] Model cached as '{self.model_name}'.  "
            f"cache_size={len(_MODEL_CACHE)}  mem={_get_memory_mb():.0f}MB"
        )

    # ------------------------------------------------------------------ #
    def _get_hf_id(self, name: str) -> str:
        name_lower = name.lower()
        if "gpt2" in name_lower:
            return "gpt2"
        elif "tinyllama" in name_lower:
            return "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        else:
            raise ValueError(
                f"Unsupported model: {name}. "
                "Only GPT-2 and TinyLlama are supported."
            )

    # ------------------------------------------------------------------ #
    async def stream_generate(
        self, prompt: str
    ) -> AsyncGenerator[Tuple[int, str, float], None]:
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
            temperature=0.7,
        )

        # Run model.generate() in a background OS thread
        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        idx = 0
        start_time = time.time()

        # Pull tokens from the streamer via asyncio.to_thread so we don't
        # block the event loop on TextIteratorStreamer's threading.Condition
        while True:
            try:
                new_text = await asyncio.to_thread(next, streamer)
                elapsed_ms = (time.time() - start_time) * 1000.0
                yield idx, new_text, elapsed_ms
                idx += 1
                start_time = time.time()
            except StopIteration:
                break
