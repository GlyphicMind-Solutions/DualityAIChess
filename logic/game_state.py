# ./DualityAIChess/logic/game_state.py
# AI Chess Game allows for user -vs user, ai -vs- ai, user -vs- ai
# Created By: David Kistner(Unconditional Love) at GlyphicMind Solutions LLC



#system imports
import chess
from logic.fen_utils import FENUtils



# ===================================
# GAME STATE CLASS
# ===================================
class GameState:
    """
    Centralized game state manager for the Chess engine.
    Wraps python-chess Board and provides clean helpers for
    move application, FEN access, resets, and game termination checks.
    """
    # ----------------
    # Initialize
    # ----------------
    def __init__(self):
        self.fen_utils = FENUtils()
        self.board = chess.Board()


# ====================================
# Basic State Access
# ====================================
    # ----------------
    # Get Board
    # ----------------
    def get_board(self) -> chess.Board:
        """
        Returns the internal python-chess Board object.
        """
        return self.board

    # ----------------
    # Get Fen
    # ----------------
    def get_fen(self) -> str:
        """
        Returns the current board position in FEN format.
        """
        return self.board.fen()

    # ----------------
    # Apply Move
    # ----------------
    def apply_move(self, move: chess.Move) -> bool:
        """
        Applies a move to the board if legal.
        Returns True if the move was applied, False otherwise.
        """
        if move in self.board.legal_moves:
            self.board.push(move)
            return True
        return False


# =========================================
# Game Termination Checks
# =========================================
    # ----------------
    # Is Game Over
    # ----------------
    def is_game_over(self) -> bool:
        """
        Returns True if the game has ended (checkmate, stalemate, etc.)
        """
        return self.board.is_game_over()

    # ----------------
    # Result
    # ----------------
    def result(self) -> str:
        """
        Returns the game result in PGN format:
        '1-0', '0-1', or '1/2-1/2'
        """
        return self.board.result()

    # ----------------
    # Outcome
    # ----------------
    def outcome(self):
        """
        Returns a python-chess Outcome object with detailed info.
        """
        return self.board.outcome()


# =========================================
# Turn and Status Helpers
# =========================================
    # ----------------
    # Is White Turn
    # ----------------
    def is_white_turn(self) -> bool:
        return self.board.turn == chess.WHITE

    # ----------------
    # Is Black Turn
    # ----------------
    def is_black_turn(self) -> bool:
        return self.board.turn == chess.BLACK

    # ----------------
    # In Check
    # ----------------
    def in_check(self) -> bool:
        return self.board.is_check()

    # ----------------
    # In Checkmate
    # ----------------
    def in_checkmate(self) -> bool:
        return self.board.is_checkmate()

    # ----------------
    # In Stalemate
    # ----------------
    def in_stalemate(self) -> bool:
        return self.board.is_stalemate()

    # --------------------------
    # In Insufficient Material
    # --------------------------
    def in_insufficient_material(self) -> bool:
        return self.board.is_insufficient_material()

    # ----------------
    # Undo
    # ----------------
    def undo(self):
        """
        Undo the last move if possible.
        """
        if self.board.move_stack:
            self.board.pop()

    # ----------------
    # Move History
    # ----------------
    def move_history(self):
        """
        Returns a list of SAN moves played so far.
        """
        temp_board = chess.Board()
        history = []
        for move in self.board.move_stack:
            history.append(temp_board.san(move))
            temp_board.push(move)
        return history

    # ----------------
    # Reset
    # ----------------
    def reset(self):
        """
        Resets the board to the initial starting position.
        """
        self.board = chess.Board()
