# ./DualityAIChess/engine/chat_selector.py
# LLM-Compatible Chess Engine - Chat Feature
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions LLC.



# system imports
import textwrap
from prompt.prompt_builder import PromptBuilder



# ========================
# CHAT SELECTOR CLASS
# ========================
class ChatSelector:
    """
    Handles chat-based LLM responses (banter, coaching, commentary).
    This LLM NEVER makes moves and NEVER affects turn order.
    """
    # --------------------
    # Initialize
    # --------------------
    def __init__(self, engine):
        self.engine = engine
        self.prompt_builder = PromptBuilder()
        self.mode = "None"   # set by ChessWindow.start_game()


    # ------------
    # Respond 
    # ------------
    def respond(self, user_message: str, board, history):
        """
        Route chat through the correct personality mode.
        """
        model_key = self.engine.chat_model
        if not model_key:
            return None

        # Mode routing
        if self.mode == "Coach":
            prompt = self._coach_prompt(user_message, board, history)

        elif self.mode == "Commentator":
            prompt = self._commentator_prompt(user_message, board, history)

        else:
            prompt = self._neutral_prompt(user_message, board, history)

        return self.engine.generate(model_key, prompt, max_tokens=128)


# ============================================================
# Prompt Section
# ============================================================
    # --------------------
    # Coach Prompt
    # --------------------
    def _coach_prompt(self, user_message, board, history):

        fen = board.fen()

        base_prompt = f"""
        You are a calm, helpful chess coach.
        You NEVER make moves.
        You NEVER output UCI or SAN notation.
        You ONLY give short, clear, constructive guidance.

        Current board (FEN):
        {fen}

        Move history:
        {history}

        The user says:
        "{user_message}"

        Respond with short, helpful coaching.
        """

        template = self.engine.get_template(self.engine.chat_model)
        return self.prompt_builder.wrap_custom_prompt(
            textwrap.dedent(base_prompt).strip(),
            template
        )

    # --------------------
    # Commentator Prompt
    # --------------------
    def _commentator_prompt(self, user_message, board, history):

        fen = board.fen()

        # Trash-talk detection
        trash_words = [
            "trash", "noob", "scrub", "boi", "boy", "scared",
            "punk", "weak", "loser", "clown", "chump"
        ]
        trash = any(w in user_message.lower() for w in trash_words)

        style = (
            "WWE hype + playful trash talk"
            if trash else
            "WWE hype + dramatic commentary"
        )

        base_prompt = f"""
        You are a WWE-style chess commentator.
        You NEVER make moves.
        You NEVER output UCI or SAN notation.
        You ONLY give hype, reactions, and playful banter.

        Style: {style}

        Current board (FEN):
        {fen}

        Move history:
        {history}

        The user says:
        "{user_message}"

        Respond with short, energetic hype or trash talk.
        """

        template = self.engine.get_template(self.engine.chat_model)
        return self.prompt_builder.wrap_custom_prompt(
            textwrap.dedent(base_prompt).strip(),
            template
        )

    # --------------------
    # Neutral Prompt
    # --------------------
    def _neutral_prompt(self, user_message, board, history):

        fen = board.fen()

        base_prompt = f"""
        You are a neutral chess commentator.
        You NEVER make moves.
        You NEVER output UCI or SAN notation.
        You ONLY give short reactions or commentary.

        Current board (FEN):
        {fen}

        Move history:
        {history}

        The user says:
        "{user_message}"

        Respond with short commentary.
        """

        template = self.engine.get_template(self.engine.chat_model)
        return self.prompt_builder.wrap_custom_prompt(
            textwrap.dedent(base_prompt).strip(),
            template
        )

