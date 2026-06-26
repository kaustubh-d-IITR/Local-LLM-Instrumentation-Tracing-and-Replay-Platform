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

# Disk offload directory for accelerate device_map
_OFFLOAD_DIR = "/tmp/model_offload"

# Maximum CPU memory (in MiB) accelerate may use for model weights.
# Remaining layers are offloaded to disk and loaded per-forward-pass.
# Render Free Tier has 512 MB total; at load time ~420 MB is already used
# by Python + FastAPI + SQLAlchemy + torch + transformers.
# Keeping this small ensures we never exceed the cgroup limit.
_MAX_CPU_MEMORY = "80MiB"


def _get_memory_mb() -> float:
    """Return current process RSS in MB. Returns 0 if psutil unavailable."""
    try:
        import psutil
        return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
    except Exception:
        return 0.0


def _get_available_mb() -> float:
    """Return system available memory in MB. May not reflect cgroup limits."""
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
        Uses accelerate device_map with disk offloading to stay within
        Render's 512 MB RAM limit.
        """
        logger.info(f"[LOAD] Entering load_model_async model={self.model_name}")

        if self.model_name in _MODEL_CACHE:
            logger.info(f"[LOAD] Cache HIT for '{self.model_name}', skipping download")
            self.model, self.tokenizer = _MODEL_CACHE[self.model_name]
            return

        logger.info(f"[LOAD] Cache MISS for '{self.model_name}', will load from HuggingFace")

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
            if rss > 400:
                logger.warning(
                    f"[STEP 4] RSS is already {rss:.0f}MB. "
                    f"Will use device_map with disk offloading "
                    f"(max_memory={_MAX_CPU_MEMORY}) to stay under 512MB."
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

            # ── Step 6: Prepare offload directory ───────────────────────
            logger.info(f"[STEP 6] Creating offload dir {_OFFLOAD_DIR}...")
            try:
                os.makedirs(_OFFLOAD_DIR, exist_ok=True)
                logger.info(f"[STEP 6] OK")
            except Exception:
                logger.exception("[STEP 6] FAILED creating offload dir")
                raise

            # ── Step 7: Load model with device_map + disk offloading ────
            #
            # WHY device_map="auto" + offload_folder:
            #   GPT-2 float32 = ~497 MB of weights.
            #   Process RSS is already ~425 MB.
            #   Loading the full model into CPU RAM would need ~920 MB → OOM.
            #
            #   device_map="auto" with max_memory tells accelerate to keep
            #   at most 80 MiB of weights on CPU. The remaining layers are
            #   serialized to /tmp/model_offload/ and loaded per-forward-pass.
            #
            # WHY torch.float32:
            #   The safetensors file stores weights in float32.
            #   Using float32 avoids an in-memory dtype conversion that would
            #   temporarily double the memory for each tensor.
            #   bfloat16 saves space but the conversion itself can cause the
            #   OOM spike that kills the Render process.
            #
            logger.info(
                f"[STEP 7] AutoModelForCausalLM.from_pretrained('{hf_id}', "
                f"device_map='auto', max_memory={_MAX_CPU_MEMORY}, "
                f"offload_folder='{_OFFLOAD_DIR}', "
                f"torch_dtype=float32, low_cpu_mem_usage=True)..."
            )
            try:
                model = AutoModelForCausalLM.from_pretrained(
                    hf_id,
                    torch_dtype=torch.float32,
                    low_cpu_mem_usage=True,
                    device_map="auto",
                    offload_folder=_OFFLOAD_DIR,
                    max_memory={"cpu": _MAX_CPU_MEMORY},
                )
                logger.info(f"[STEP 7] from_pretrained() OK  mem={_get_memory_mb():.0f}MB")
            except Exception:
                logger.exception(f"[STEP 7] FAILED  mem={_get_memory_mb():.0f}MB")
                raise

            # ── Step 8: Log device map ──────────────────────────────────
            if hasattr(model, "hf_device_map"):
                dmap = model.hf_device_map
                cpu_layers = [k for k, v in dmap.items() if v != "disk"]
                disk_layers = [k for k, v in dmap.items() if v == "disk"]
                logger.info(
                    f"[STEP 8] Device map: {len(cpu_layers)} layers on CPU, "
                    f"{len(disk_layers)} layers on disk"
                )
                logger.info(f"[STEP 8] CPU layers : {cpu_layers}")
                logger.info(f"[STEP 8] Disk layers: {disk_layers}")
            else:
                logger.info("[STEP 8] No hf_device_map (model fully on CPU)")

            # ── Step 9: Eval mode ───────────────────────────────────────
            logger.info("[STEP 9] model.eval()...")
            try:
                model.eval()
                logger.info(f"[STEP 9] OK  mem={_get_memory_mb():.0f}MB")
            except Exception:
                logger.exception(f"[STEP 9] FAILED  mem={_get_memory_mb():.0f}MB")
                raise

            # NOTE: Do NOT call model.to(device) — accelerate manages
            # device placement via the dispatch hooks set up by device_map.
            # self.device is used only for placing INPUT tensors on CPU.
            self.device = "cpu"

            mem_final = _get_memory_mb()
            logger.info(
                f"[LOAD COMPLETE] {hf_id} ready.  "
                f"Final RSS={mem_final:.0f}MB  "
                f"delta=+{mem_final - rss:.0f}MB"
            )
            return model, tokenizer

        # Dispatch the blocking _load() to a thread so the event loop stays free
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

        # Inputs always go to CPU; accelerate dispatch hooks move data
        # through CPU/disk layers automatically during model.generate().
        inputs = self.tokenizer([prompt], return_tensors="pt").to("cpu")
        streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True)

        generation_kwargs = dict(
            inputs,
            streamer=streamer,
            max_new_tokens=50,
            do_sample=True,
            top_p=0.9,
            temperature=0.7,
        )

        # Run model.generate() in a background OS thread.
        # accelerate's dispatch hooks work in any thread.
        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        idx = 0
        start_time = time.time()

        # Pull tokens from the streamer via asyncio.to_thread so we don't
        # block the main event loop on the threading.Condition inside the
        # streamer's __next__().
        while True:
            try:
                new_text = await asyncio.to_thread(next, streamer)
                elapsed_ms = (time.time() - start_time) * 1000.0
                yield idx, new_text, elapsed_ms
                idx += 1
                start_time = time.time()
            except StopIteration:
                break
