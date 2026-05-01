# ./DualityAIChess/prompt/prompt_builder.py
# AI Chess Game allows for user -vs user, ai -vs- ai, user -vs- ai
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions LLC



#system imports
import textwrap



# ====================================
# PROMPT BUILDER CLASS
# ====================================
class PromptBuilder:
    """
    Builds prompts for LLM-based chess move generation.
    Template-aware (gpt, mistral, qwen, llama, etc.)
    Now supports hybrid Stockfish + LLM reasoning.
    """

    # --------------
    # Initialize
    # --------------
    def __init__(self):
        pass


# ====================================
# Prompt Construction
# ====================================
    # ------------------------
    # Build Prompt (Hybrid)
    # ------------------------
    def build_prompt(self, fen: str, template: str, engine_suggestion: str = "none"):
        """
        Build a complete prompt for the given model template.
        Includes Stockfish's suggested move for hybrid reasoning.
        """
        base = self._base_prompt(fen, engine_suggestion)

        if template == "gpt":
            return self._wrap_gpt(base)

        if template == "mistral":
            return self._wrap_mistral(base)

        if template == "qwen":
            return self._wrap_qwen(base)

        if template == "llama":
            return self._wrap_llama(base)

        # fallback
        return base


    # ------------------------
    # Base Prompt (Hybrid)
    # ------------------------
    def _base_prompt(self, fen: str, engine_suggestion: str):
        """
        Core chess instruction with Stockfish suggestion included.
        """
        return textwrap.dedent(
            f"""
            -- INSTRUCTIONS --

            - You are an Agent using a chess engine.
            - Your purpose is to use the chess engine with your current knowledge and understanding of the game to win.
            - The current board position is given in FEN format:
              -- {fen}

            - Suggested best move from a strong chess engine:
              -- {engine_suggestion}

            - You may follow this suggestion or choose a different legal move.
            - Respond with ONLY the move in UCI format (example: e2e4, g8f6, a7a8q).
            - Do not explain your reasoning.
            - Do not output anything except the move.
            """
        ).strip()



# =========================================================
# Template Wrappers
# =========================================================
    # ------------------------------
    # Wrap Custom Prompt
    # ------------------------------
    def wrap_custom_prompt(self, content: str, template: str):
        """
        Wraps arbitrary content in the correct template format.
        Used for chat model prompts.
        """
        if template == "gpt":
            return f"<|system|>\n{content}\n<|assistant|>"

        if template == "mistral":
            return f"<s>[INST] {content} [/INST]"

        if template == "qwen":
            return (
                f"<|im_start|>system\n{content}<|im_end|>\n"
                f"<|im_start|>assistant\n"
            )

        if template == "llama":
            return (
                f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n"
                f"{content}\n"
                f"<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
            )

        return content


    # -------------
    # Wrap GPT
    # -------------
    def _wrap_gpt(self, content: str):
        """
        GPT-style chat template.
        """
        return (
            f"<|system|>\nYou are a chess engine.\n"
            f"<|user|>\n{content}\n"
            f"<|assistant|>"
        )


    # -------------
    # Wrap Mistral
    # -------------
    def _wrap_mistral(self, content: str):
        """
        Mistral instruct template.
        """
        return f"[INST] {content} [/INST]"


    # -------------
    # Wrap QWEN
    # -------------
    def _wrap_qwen(self, content: str):
        """
        Qwen chat template.
        """
        return (
            f"<|im_start|>system\nYou are a chess engine.<|im_end|>\n"
            f"<|im_start|>user\n{content}<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )


    # -------------
    # Wrap llama
    # -------------
    def _wrap_llama(self, content: str):
        """
        Llama 3 instruct template.
        """
        return (
            f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n"
            f"{content}\n"
            f"<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
        )

