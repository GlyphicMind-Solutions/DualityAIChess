# /Chess/cli.py
# LLM-Compatible Chess Engine
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions LLC.



#system imports
import sys, chess

#local imports
from logic.game_state import GameState
from engine.llm_engine import LLMEngine
from engine.move_selector import MoveSelector



# =======================
# CHESS APP CLASS
# =======================
class ChessApp:
    """
    Main orchestrator for the Chess application.
    Wires together game state, LLM engine, and move selection.
    CLI-based loop for now; GUI can hook into the same GameState + MoveSelector.
    """
    # ----------------
    # Initialize
    # ----------------
    def __init__(self):
        self.state = GameState()
        self.engine = LLMEngine()
        self.selector = MoveSelector(self.engine)

        self.mode = self.engine.get_mode()
        print(f"[ChessApp] Mode: {self.mode}")
        print(f"[ChessApp] White model: {self.engine.get_white_model()}")
        print(f"[ChessApp] Black model: {self.engine.get_black_model()}")


# =========================================
# MAIN LOOP
# =========================================
    # ----------------
    # Run
    # ----------------
    def run(self):
        """
        Main game loop.
        For now, this is a CLI loop; GUI will later call into the same methods.
        """
        print("[ChessApp] Starting new game.")
        print(self.state.get_board())

        while not self.state.is_game_over():
            board = self.state.get_board()

            if self.mode == "user_vs_user":
                self._handle_user_turn(board)

            elif self.mode == "user_vs_llm":
                if board.turn == chess.WHITE:
                    self._handle_user_turn(board)
                else:
                    self._handle_llm_turn(board)

            elif self.mode == "llm_vs_llm":
                self._handle_llm_turn(board)

            else:
                print(f"[ChessApp] Unknown mode: {self.mode}")
                break

            print(self.state.get_board())

        self._print_result()


# =========================================
# TURN HANDLERS
# =========================================
    # -----------------
    # Handl User Turn
    # -----------------
    def _handle_user_turn(self, board: chess.Board):
        """
        Handles a human player's move via CLI input.
        GUI will later replace this with event-driven input.
        """
        color = "White" if board.turn == chess.WHITE else "Black"
        print(f"\n{color} to move (user).")

        while True:
            user_input = input("Enter your move in UCI (e.g., e2e4) or 'quit': ").strip()
            if user_input.lower() in ("quit", "exit"):
                print("[ChessApp] Exiting game.")
                sys.exit(0)

            try:
                move = chess.Move.from_uci(user_input)
            except Exception:
                print("Invalid UCI format. Try again.")
                continue

            if move in board.legal_moves:
                self.state.apply_move(move)
                break
            else:
                print("Illegal move. Try again.")

    # -----------------
    # Handle LLM Turn
    # -----------------
    def _handle_llm_turn(self, board: chess.Board):
        """
        Handles an LLM player's move using MoveSelector.
        """
        color = "White" if board.turn == chess.WHITE else "Black"
        print(f"\n{color} to move (LLM). Thinking...")

        move = self.selector.select_move(board)

        if move is None:
            print("[ChessApp] LLM failed to produce a move. Ending game.")
            self.state.board = board
            return

        print(f"[ChessApp] LLM plays: {move.uci()}")
        self.state.apply_move(move)

    # ----------------
    # Print Result
    # ----------------
    def _print_result(self):
        """
        Prints the final result and outcome.
        """
        print("\n[ChessApp] Game over.")
        print(self.state.get_board())
        print(f"Result: {self.state.result()}")

        outcome = self.state.outcome()
        if outcome is not None:
            print(f"Termination: {outcome.termination}")
            print(f"Winner: {outcome.winner}")


# ========================= #
# ENTRY POINT               #
# ========================= #
if __name__ == "__main__":
    app = ChessApp()
    app.run()

