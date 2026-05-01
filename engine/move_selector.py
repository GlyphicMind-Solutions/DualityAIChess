# ./DualityAIChess/engine/move_selector.py
# Hybrid LLM + Stockfish Move Selector
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions LLC



#system imports
import chess


#local imports
from logic.move_validator import MoveValidator
from prompt.prompt_builder import PromptBuilder



# =============================
# MOVE SELECTOR CLASS
# =============================
class MoveSelector:
    """
    Hybrid move selector:
    - Uses Stockfish to compute best move
    - Injects Stockfish suggestion into LLM prompt
    - LLM chooses move if valid
    - Falls back to Stockfish if LLM fails
    """

    # -------------------
    # Initialize
    # -------------------
    def __init__(self, llm_engine, chess_engine=None):

        self.llm_engine = llm_engine
        self.chess_engine = chess_engine
        self.validator = MoveValidator()
        self.prompt_builder = PromptBuilder()

    # ----------------------------
    # Select Move
    # ----------------------------
    def select_move(self, board: chess.Board):
        """
        Main hybrid move selection logic.
        Determines which model to use,
        injects Stockfish suggestion,
        validates LLM output,
        falls back to Stockfish if needed.
        """

        mode = self.llm_engine.get_mode()

        # USER VS USER
        if mode == "user_vs_user":
            return None  # GUI handles user input

        # USER VS LLM
        if mode == "user_vs_llm":

            # LLM plays white
            if board.turn == chess.WHITE and self.llm_engine.white_model is not None:
                model_key = self.llm_engine.white_model

            # LLM plays black
            elif board.turn == chess.BLACK and self.llm_engine.black_model is not None:
                model_key = self.llm_engine.black_model
            else:
                return None  # User turn

        else:
            # LLM VS LLM
            model_key = (
                self.llm_engine.get_white_model()
                if board.turn == chess.WHITE
                else self.llm_engine.get_black_model()
            )

        #STOCKFISH SUGGESTION (ENGINE MEMORY)
        engine_move = None

        if self.chess_engine:
            try:
                engine_move = self.chess_engine.suggest_move(board)
            except Exception as e:
                print("[MoveSelector] Stockfish error:", e)

        #HYBRID PROMPT CONSTRUCTION
        fen = board.fen()
        template = self.llm_engine.get_template(model_key)

        engine_suggestion = engine_move.uci() if engine_move else "none"

        prompt = self.prompt_builder.build_prompt(
            fen,
            template,
            engine_suggestion=engine_suggestion
        )

        #LLM MOVE GENERATION
        raw_output = self.llm_engine.generate(
            model_key,
            prompt,
            max_tokens=8
        )

        #PARSE + VALIDATE LLM MOVE
        move = self._parse_and_validate(board, raw_output)

        #FALLBACK TO STOCKFISH IF LLM FAILS
        if move is None and engine_move:
            return engine_move

        return move

    # ---------------------------------
    # Parse and Validate
    # ---------------------------------
    def _parse_and_validate(self, board: chess.Board, raw_output: str):
        """
        Attempts to parse the LLM output into a legal chess move.
        Supports SAN, UCI, and common LLM mistakes.
        """

        if not raw_output:
            return None

        # Try SAN
        try:
            move = board.parse_san(raw_output)
            if self.validator.is_legal_move(board, move):
                return move
        except Exception:
            pass

        # Try UCI
        try:
            move = chess.Move.from_uci(raw_output.strip())
            if self.validator.is_legal_move(board, move):
                return move
        except Exception:
            pass

        # Try extracting UCI
        cleaned = self._extract_uci(raw_output)
        if cleaned:
            try:
                move = chess.Move.from_uci(cleaned)
                if self.validator.is_legal_move(board, move):
                    return move
            except Exception:
                pass

        return None

    # ----------------------------
    # Extract UCI
    # ----------------------------
    def _extract_uci(self, text: str):
        """
        Extracts a UCI move from messy LLM output.
        Example: "I think the best move is e2e4." → "e2e4"
        """
        text = text.lower().strip()

        for token in text.split():
            if len(token) == 4 and token[0] in "abcdefgh":
                return token
            if len(token) == 5 and token[0] in "abcdefgh":  # promotion
                return token

        return None

