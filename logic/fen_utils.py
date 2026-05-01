# ./DualityAIChess/logic/fen_utils.py
# AI Chess Game allows for user -vs user, ai -vs- ai, user -vs- ai
# Created By: David Kistner(Unconditional Love) at GlyphicMind Solutions LLC



#system imports
import chess



# ===============================
# FEN UTILITIES CLASS
# ===============================
class FENUtils:
    """
    Utility functions for working with FEN strings.
    Provides clean helpers for converting between python-chess
    board objects and FEN notation.
    """
    # ---------------------
    # Initialize
    # ---------------------
    def __init__(self):
        pass

# ===========================================
# Conversion Section
# ===========================================
    # ---------------------
    # Board to Fen
    # ---------------------
    def board_to_fen(self, board: chess.Board) -> str:
        """
        Returns the FEN string for the given board.
        """
        return board.fen()

    # ---------------------
    # Fen to Board
    # ---------------------
    def fen_to_board(self, fen: str) -> chess.Board:
        """
        Creates a new chess.Board object from a FEN string.
        """
        return chess.Board(fen)

# ===========================================
# MetaData Helpers Section
# ===========================================
    # ---------------------
    # Get Turn
    # ---------------------
    def get_turn(self, fen: str) -> str:
        """
        Returns 'w' or 'b' depending on whose turn it is.
        """
        parts = fen.split()
        return parts[1] if len(parts) > 1 else "w"

    # ---------------------
    # Get Castling Rights
    # ---------------------
    def get_castling_rights(self, fen: str) -> str:
        """
        Returns castling rights (e.g., 'KQkq', '-', etc.)
        """
        parts = fen.split()
        return parts[2] if len(parts) > 2 else "-"

    # -----------------------
    # Get en Passant Square
    # -----------------------
    def get_en_passant_square(self, fen: str) -> str:
        """
        Returns the en passant target square or '-'.
        """
        parts = fen.split()
        return parts[3] if len(parts) > 3 else "-"

    # ---------------------
    # Get Halfmove Clock
    # ---------------------
    def get_halfmove_clock(self, fen: str) -> int:
        """
        Returns the halfmove clock (for 50-move rule).
        """
        parts = fen.split()
        return int(parts[4]) if len(parts) > 4 else 0

    # ---------------------
    # Get Fullmove Number
    # ---------------------
    def get_fullmove_number(self, fen: str) -> int:
        """
        Returns the fullmove number.
        """
        parts = fen.split()
        return int(parts[5]) if len(parts) > 5 else 1

# =========================================================
# Debugging / Display Helpers Section
# =========================================================
    # ---------------------
    # Pretty Board
    # ---------------------
    def pretty_board(self, board: chess.Board) -> str:
        """
        Returns a human-readable ASCII board.
        Useful for debugging or logging.
        """
        return str(board)

    # ---------------------
    # Pretty Fen
    # ---------------------
    def pretty_fen(self, fen: str) -> str:
        """
        Returns a formatted breakdown of the FEN fields.
        """
        parts = fen.split()
        if len(parts) < 6:
            return f"Invalid FEN: {fen}"

        return (
            f"Board: {parts[0]}\n"
            f"Turn: {parts[1]}\n"
            f"Castling: {parts[2]}\n"
            f"En Passant: {parts[3]}\n"
            f"Halfmove Clock: {parts[4]}\n"
            f"Fullmove Number: {parts[5]}"
        )

