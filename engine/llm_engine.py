# ./DualityAIChess/engine/llm_engine.py
# AI Chess Game allows for user -vs user, ai -vs- ai, user -vs- ai
# Created By: David Kistner(Unconditional Love) at GlyphicMind Solutions LLC


#system imports
import os, yaml
from pathlib import Path
from llama_cpp import Llama
from engine.chess_engine import ChessEngine



# =========================
# LLM ENGINE CLASS
# =========================
class LLMEngine:
    """
    Multi‑model LLM engine for Chess.
    Loads all models defined in manifest.yaml but initializes them lazily.
    Compatible with Forge-style manifests and prompt templates.
    """
    # --------------
    # Initialize
    # --------------
    def __init__(self):
        # Load manifest.yaml
        manifest_path = (
            Path(__file__).resolve().parents[1] / "models" / "manifest.yaml"
        )
        with open(manifest_path, "r", encoding="utf-8") as f:
            self.manifest = yaml.safe_load(f)

        # Registry of model configs
        self.model_configs = self.manifest.get("models", {})
        # Lazy-loaded model instances
        self.loaded_models = {}

        #chat model
        self.chat_model = None

        # Defaults for Chess
        defaults = self.manifest.get("defaults", {})
        self.mode = defaults.get("mode", "llm_vs_llm")
        self.white_model = defaults.get("white_model", None)
        self.black_model = defaults.get("black_model", None)

        # Chess Engine
        self.chess_engine = ChessEngine(
            engine_path=os.path.join(os.getcwd(), "engine", "core", "stockfish-ubuntu-x86-64-avx2"),
            depth=12
        )

    # -----------------------
    # Load Model
    # -----------------------
    def load_model(self, model_key: str):
        """
        Lazy-load a model only when needed.
        Silences duplicate BOS warnings by disabling llama.cpp's BOS injection.
        """
        if model_key in self.loaded_models:
            return self.loaded_models[model_key]

        if model_key not in self.model_configs:
            raise ValueError(f"Model '{model_key}' not found in manifest.yaml")

        cfg = self.model_configs[model_key]

        model_path = cfg.get("path")
        n_ctx = cfg.get("n_ctx", 4096)

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")

        print(f"[LLMEngine] Loading model: {model_key} ({model_path})")

        # BOS-SAFE MODEL LOADING
        llm = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            verbose=False,
            add_bos_token=False,
        )

        self.loaded_models[model_key] = llm
        return llm

    # -----------------------
    # Generate
    # -----------------------
    def generate(self, model_key: str, prompt: str, max_tokens: int = 128):
        """
        Generate text from a specific model.
        """
        llm = self.load_model(model_key)

        output = llm(
            prompt,
            max_tokens=max_tokens,
            temperature=0.7,
            top_k=40,
            top_p=0.9,
        )

        return output["choices"][0]["text"].strip()


# =========================================================
# CHESS HELPERS
# =========================================================
    # --------------------
    # Get White Model
    # --------------------
    def get_white_model(self):
        return self.white_model

    # --------------------
    # Get Black model
    # --------------------
    def get_black_model(self):
        return self.black_model

    # --------------------
    # Get Mode
    # --------------------
    def get_mode(self):
        return self.mode

    # --------------------
    # Get Template
    # --------------------
    def get_template(self, model_key: str):
        """
        Returns the template type for the model (gpt, mistral, qwen, llama, etc.)
        """
        cfg = self.model_configs.get(model_key, {})
        return cfg.get("template", "gpt")  # default fallback

