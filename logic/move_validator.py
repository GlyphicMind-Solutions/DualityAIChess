# ./DualityAIChess/logic/move_validator.py
# AI Chess Game allows for user -vs user, ai -vs- ai, user -vs- ai
# Created By: David Kistner(Unconditional Love) at GlyphicMind Solutions LLC



#system imports
import chess, random



# ===========================
# MOVE VALIDATOR CLASS
# ===========================
class MoveValidator:
    """
    Validates moves for the Chess LLM engine.
    Ensures moves are legal and provides safe fallbacks.
    """
    # -----------------
    # Initalize 
    # -----------------
    def __init__(self):
        pass


# ==========================
# Logic Section
# ==========================
    # -------------------
    # Is Legal Move
    # -------------------
    def is_legal_move(self, board: chess.Board, move: chess.Move) -> bool:
        """
        Returns True if the move is legal in the current position.
        """
        return move in board.legal_moves

    # --------------------
    # Random Legal Move
    # --------------------
    def random_legal_move(self, board: chess.Board) -> chess.Move:
        """
        Returns a random legal move.
        Used when the LLM outputs an invalid or unparsable move.
        """
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None  # checkmate or stalemate
        return random.choice(legal_moves)


# ===============================
# Parsing Section
# ===============================
    # --------------------
    # Try Parse San
    # --------------------
    def try_parse_san(self, board: chess.Board, san: str):
        """
        Attempts to parse SAN notation safely.
        Returns a move or None.
        """
        try:
            move = board.parse_san(san)
            if self.is_legal_move(board, move):
                return move
        except Exception:
            return None

    # -------------------
    # Try Parse UCI
    # -------------------
    def try_parse_uci(self, board: chess.Board, uci: str):
        """
        Attempts to parse UCI notation safely.
        Returns a move or None.
        """
        try:
            move = chess.Move.from_uci(uci)
            if self.is_legal_move(board, move):
                return move
        except Exception:
            return None

