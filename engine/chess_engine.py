# ./DualityAIChess/engine/chess_engine.py
# LLM-Compatible Chess Engine - Chat Feature
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions LLC.



#system imports
import chess, chess.engine



# ===================================
# CHESS ENGINE CLASS
# ===================================
class ChessEngine:
    # ----------------
    # Initialize
    # ----------------
    def __init__(self, engine_path: str, depth: int = 15):
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)
        self.depth = depth

    # ----------------
    # Suggest Move
    # ----------------
    def suggest_move(self, board: chess.Board):
        result = self.engine.play(board, chess.engine.Limit(depth=self.depth))
        return result.move  # chess.Move

    # ----------------
    # Evaluate
    # ----------------
    def evaluate(self, board: chess.Board):
        info = self.engine.analyse(board, chess.engine.Limit(depth=self.depth))
        return info.get("score")

    # ----------------
    # Close
    # ----------------
    def close(self):
        self.engine.quit()

