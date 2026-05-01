# ./DualityAIChess/gui/chess_window.py
# LLM-Compatible Chess Engine GUI Interface
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions LLC.



#system imports
import os, chess, threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

#local imports
from gui.board_renderer import BoardRenderer
from logic.game_state import GameState
from engine.llm_engine import LLMEngine
from engine.move_selector import MoveSelector
from engine.chat_selector import ChatSelector
from engine.chess_engine import ChessEngine



# ====================================================
# Chess Window Class
# ====================================================
class ChessWindow:
    """
    Full GUI for the LLM Chess system.
    Allows player assignment, chat, move input, saving, undo, restart, etc.
    Includes:
    - Hybrid LLM + Stockfish move selection
    - Turn indicator + player banner
    - Move log + chat log
    - Optional engine suggestion commentary
    - Optional coach/commentator auto-comments
    - Last-move + arrow visualization hooks
    """
    # --------------------
    # Initialize
    # --------------------
    def __init__(self, root):

        # Window Title
        self.root = root
        self.root.title("Duality AI Chess - GlyphicMind Solutions")

        # Core engine components
        self.state = GameState()
        self.engine = LLMEngine()
        self.chess_engine = ChessEngine(
            engine_path=os.path.join(os.getcwd(), "engine", "core", "stockfish-ubuntu-x86-64-avx2"),
            depth=12
        )
        self.selector = MoveSelector(self.engine, self.chess_engine)

        # GUI layout
        self._build_top_info()
        self._build_menu()
        self._build_player_assignment()
        self._build_board()
        self._build_side_panel()

        # Renderer
        self.renderer = BoardRenderer(self.board_canvas, self.state.get_board())
        self.renderer.draw_board()

        # Chat Selector
        self.chat_selector = ChatSelector(self.engine)

        # Binding
        self.board_canvas.bind("<Button-1>", self.on_press)
        self.board_canvas.bind("<B1-Motion>", self.on_drag)
        self.board_canvas.bind("<ButtonRelease-1>", self.on_release)
        self.selected_square = None
        self.drag_data = {
            "from_square": None,
            "piece": None,
            "image": None,
        }

        # Visualization state
        self.last_move_from = None
        self.last_move_to = None
        self.last_arrow_id = None
        self.engine_arrow_id = None

        # Shutdown
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)


# ====================================================
# Builder Section
# ====================================================
    # ---------------------------------------------------------
    # Build Top Info (Banner + Turn + Thinking + Eval)
    # ---------------------------------------------------------
    def _build_top_info(self):

        top_frame = ttk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Player banner
        self.player_label = ttk.Label(top_frame, text="White: -    Black: -")
        self.player_label.pack(side=tk.LEFT, padx=(0, 20))

        # Turn indicator
        self.turn_label = ttk.Label(top_frame, text="Turn: -")
        self.turn_label.pack(side=tk.LEFT, padx=(0, 20))

        # Thinking indicator
        self.thinking_label = ttk.Label(top_frame, text="")
        self.thinking_label.pack(side=tk.LEFT, padx=(0, 20))

        # Eval bar (optional, only used if engine supports evaluation)
        self.eval_canvas = tk.Canvas(top_frame, width=80, height=16, bg="#222222", highlightthickness=1, highlightbackground="#555555")
        self.eval_canvas.pack(side=tk.RIGHT, padx=(20, 0))
        self._draw_eval_bar(0.0)

    # ---------------------------------------------------------
    # Build Menu
    # ---------------------------------------------------------
    def _build_menu(self):

        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)

        #restart game
        game_menu.add_command(label="Restart Game", command=self.restart_game)

        #undo move
        game_menu.add_command(label="Undo Move", command=self.undo_move)
        game_menu.add_separator()

        #save game
        game_menu.add_command(label="Save Game", command=self.save_game)
        game_menu.add_separator()

        #exit game
        game_menu.add_command(label="Exit", command=self.root.quit)

        #game menu
        menubar.add_cascade(label="Game", menu=game_menu)
        self.root.config(menu=menubar)

    # ---------------------------------------------------------
    # Build Player Assignment
    # ---------------------------------------------------------
    def _build_player_assignment(self):

        frame = ttk.Frame(self.root)
        frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        #white dropdown
        ttk.Label(frame, text="White:").pack(side=tk.LEFT)
        self.white_var = tk.StringVar()
        self.white_dropdown = ttk.Combobox(
            frame,
            textvariable=self.white_var,
            values=["User"] + list(self.engine.model_configs.keys()),
            state="readonly",
            width=20
        )
        self.white_dropdown.current(0)
        self.white_dropdown.pack(side=tk.LEFT, padx=5)

        #black dropdown
        ttk.Label(frame, text="Black:").pack(side=tk.LEFT)
        self.black_var = tk.StringVar()
        self.black_dropdown = ttk.Combobox(
            frame,
            textvariable=self.black_var,
            values=["User"] + list(self.engine.model_configs.keys()),
            state="readonly",
            width=20
        )
        self.black_dropdown.current(1 if len(self.engine.model_configs) > 0 else 0)
        self.black_dropdown.pack(side=tk.LEFT, padx=5)

        #chat model dropdown
        ttk.Label(frame, text="Chat Model:").pack(side=tk.LEFT, padx=(20, 0))
        self.chat_var = tk.StringVar()
        self.chat_dropdown = ttk.Combobox(
            frame,
            textvariable=self.chat_var,
            values=["None"] + list(self.engine.model_configs.keys()),
            state="readonly",
            width=20
        )
        self.chat_dropdown.current(0)
        self.chat_dropdown.pack(side=tk.LEFT, padx=5)

        #chat mode dropdown
        ttk.Label(frame, text="Chat Mode:").pack(side=tk.LEFT, padx=(20, 0))
        self.chat_mode_var = tk.StringVar()
        self.chat_mode_dropdown = ttk.Combobox(
            frame,
            textvariable=self.chat_mode_var,
            values=["None", "Coach", "Commentator"],
            state="readonly",
            width=20
        )
        self.chat_mode_dropdown.current(0)
        self.chat_mode_dropdown.pack(side=tk.LEFT, padx=5)

        #start game button
        start_btn = ttk.Button(frame, text="Start Game", command=self.start_game)
        start_btn.pack(side=tk.LEFT, padx=10)

    # ---------------------------------------------------------
    # Build Board
    # ---------------------------------------------------------
    def _build_board(self):

        #board size / canvas
        self.board_canvas = tk.Canvas(self.root, width=480, height=480)
        self.board_canvas.pack(side=tk.LEFT, padx=10, pady=10)

    # ---------------------------------------------------------
    # Build Side Panel (Move Log + Chat)
    # ---------------------------------------------------------
    def _build_side_panel(self):

        panel = ttk.Frame(self.root)
        panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        #log box
        self.move_log = tk.Text(panel, height=25, width=28, state="disabled")
        self.move_log.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        #chat box
        self.chat_box = tk.Text(panel, height=20, width=50, state="disabled")
        self.chat_box.pack(fill=tk.BOTH, expand=True)
        self.chat_box.tag_config("user", foreground="#64B5F6")
        self.chat_box.tag_config("coach", foreground="#81C784")
        self.chat_box.tag_config("commentator", foreground="#FFB74D")
        self.chat_box.tag_config("llm", foreground="#CE93D8")

        #user input box
        self.input_var = tk.StringVar()
        input_entry = ttk.Entry(panel, textvariable=self.input_var)
        input_entry.pack(fill=tk.X, pady=5)

        #send button
        send_btn = ttk.Button(panel, text="Send", command=self.send_message)
        send_btn.pack()


# ====================================================
# Threading Section
# ====================================================
    # --------------------
    # ASYNC LLM Move
    # --------------------
    def _async_llm_move(self):
        # ----------
        # Worker
        # ----------
        def worker():
            board = self.state.get_board()
            move = self.selector.select_move(board)

            # schedule GUI update on main thread
            self.root.after(0, lambda: self._apply_llm_move(move))

        threading.Thread(target=worker, daemon=True).start()



# ====================================================
# Game Control Section
# ====================================================
    # --------------
    # Start Game
    # --------------
    def start_game(self):

        #select chat model
        chat_choice = self.chat_var.get()
        self.engine.chat_model = None if chat_choice == "None" else chat_choice
        self.chat_selector.mode = self.chat_mode_var.get()
        self._log(f"Chat Model: {self.engine.chat_model}")

        white = self.white_var.get()
        black = self.black_var.get()

        # Configure engine mode + model assignment
        if white == "User" and black == "User":
            self.engine.mode = "user_vs_user"
            self.engine.white_model = None
            self.engine.black_model = None

        elif white == "User" and black != "User":
            # User plays white, LLM plays black
            self.engine.mode = "user_vs_llm"
            self.engine.white_model = None
            self.engine.black_model = black

        elif white != "User" and black == "User":
            # LLM plays white, User plays black
            self.engine.mode = "user_vs_llm"
            self.engine.white_model = white
            self.engine.black_model = None

        else:
            # LLM vs LLM
            self.engine.mode = "llm_vs_llm"
            self.engine.white_model = white
            self.engine.black_model = black

        self._log(f"Game started. Mode: {self.engine.mode}")
        self._log(f"White: {white}, Black: {black}")

        # Update banner
        self.player_label.config(text=f"White: {white}    Black: {black}")

        # Reset board + visuals
        self.state.reset()
        self.renderer.board = self.state.get_board()
        self.renderer.draw_board()
        self._update_turn_indicator()
        self._clear_arrows()
        self._draw_eval_for_current_position()

        # If white is LLM, make the first move
        if self.engine.white_model is not None:
            self._maybe_llm_move()

    # --------------
    # Restart Game
    # --------------
    def restart_game(self):
        self.state.reset()
        self.selected_square = None
        self.renderer.board = self.state.get_board()
        #redraw board / clear arrors
        self.renderer.draw_board()
        self._clear_arrows()
        self._draw_eval_for_current_position()
        #update log / indicator
        self._update_turn_indicator()
        self._log("Game restarted.")

    # --------------
    # Undo Moves
    # --------------
    def undo_move(self):

        self.state.undo()
        #redraw board / clear arrors
        self.renderer.draw_board()
        self._clear_arrows()
        self._draw_eval_for_current_position()
        #update log / indicator
        self._update_turn_indicator()
        self._log("Move undone.")

    # --------------------
    # Save Game
    # --------------------
    def save_game(self):

        moves = self.state.move_history()
        if not moves:
            messagebox.showinfo("Save Game", "No moves to save.")
            return

        default_dir = os.path.join(os.getcwd(), "saves")
        os.makedirs(default_dir, exist_ok=True)

        file_path = filedialog.asksaveasfilename(
            initialdir=default_dir,
            title="Save Game",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )

        if not file_path:
            return

        with open(file_path, "w") as f:
            for i, move in enumerate(moves, start=1):
                f.write(f"{i}. {move}\n")

        self._log(f"Game saved to: {file_path}")


# =========================================================
# Move Handling Section
# =========================================================
    # ---------------------------
    # Coordinates to Square
    # ---------------------------
    def _coords_to_square(self, event):
        file = event.x // self.renderer.square_size
        rank = 7 - (event.y // self.renderer.square_size)
        if 0 <= file < 8 and 0 <= rank < 8:
            return chess.square(file, rank)
        return None

    # -----------------
    # Handle User Move
    # -----------------
    def _handle_user_move(self, move_text):

        board = self.state.get_board()

        try:
            move = board.parse_uci(move_text)
        except Exception:
            return False  # not a move

        if move not in board.legal_moves:
            self._log("Illegal move.")
            return True

        self.state.apply_move(move)
        self.renderer.draw_board()

        # Log move
        color_label = "White" if board.turn == chess.BLACK else "Black"
        player_label = "User"
        self._log_move(color_label, player_label, move.from_square, move.to_square)

        # Visuals
        self._highlight_last_move(move.from_square, move.to_square)
        self._clear_engine_arrow()
        self._draw_eval_for_current_position()
        self._update_turn_indicator()

        # Maybe LLM responds
        self._maybe_llm_move()
        return True

    # ---------------------
    # Maybe LLM Move
    # ---------------------
    def _maybe_llm_move(self):

        board = self.state.get_board()

        # Game Over
        if self.state.is_game_over():
            self._declare_winner()
            return

        # Mode Checks
        if self.engine.mode == "user_vs_user":
            return

        # User plays white → block LLM on white's turn
        if self.engine.mode == "user_vs_llm" and self.engine.white_model is None and board.turn == chess.WHITE:
            return

        # User plays black → block LLM on black's turn
        if self.engine.mode == "user_vs_llm" and self.engine.black_model is None and board.turn == chess.BLACK:
            return

        # LLM turn (async)
        self._async_llm_move()

    # -------------------
    # Apply LLM Move
    # -------------------
    def _apply_llm_move(self, move):
        if move is None:
            self._log("LLM failed to produce a move.")
            return

        board = self.state.get_board()

        # Log move
        color_label = "White" if board.turn == chess.WHITE else "Black"
        player_label = (
            self.engine.get_white_model() if board.turn == chess.WHITE
            else self.engine.get_black_model()
        )
        self._log_move(color_label, player_label, move.from_square, move.to_square)
        self._log(f"LLM plays: {move.uci()}")

        # Engine suggestion arrow
        engine_move = None
        if self.selector.chess_engine:
            try:
                engine_move = self.selector.chess_engine.suggest_move(board)
            except Exception:
                engine_move = None

        if engine_move and engine_move != move:
            self._log(f"Engine suggested: {engine_move.uci()}", "commentator")
            self._draw_engine_arrow(engine_move)
        else:
            self._clear_engine_arrow()

        # Apply move
        self.state.apply_move(move)
        self.renderer.draw_board()

        # Visuals
        self._highlight_last_move(move.from_square, move.to_square)
        self._draw_eval_for_current_position()
        self._update_turn_indicator()

        # Auto chat
        self._auto_chat_on_move(board)

        # Continue LLM vs LLM
        if self.engine.mode == "llm_vs_llm":
            self.root.after(50, self._maybe_llm_move)


# =========================================================
# Drag & Drop Handlers
# =========================================================
    # ----------------
    # On Press
    # ----------------
    def on_press(self, event):
        square = self._coords_to_square(event)
        if square is None:
            return

        board = self.state.get_board()
        piece = board.piece_at(square)
        if not piece:
            return

        # store drag info
        self.drag_data["from_square"] = square
        self.drag_data["piece"] = piece

        # highlight selected square
        self.renderer.clear_highlights()
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        self.renderer.highlight_square(file, rank)

        # highlight legal moves
        self.renderer.highlight_legal_moves(board, square)

    # ----------------
    # On Drag
    # ----------------
    def on_drag(self, event):
        # optional: you can implement piece-following cursor later
        pass

    # ----------------
    # On Release
    # ----------------
    def on_release(self, event):
        from_sq = self.drag_data["from_square"]
        if from_sq is None:
            return

        to_sq = self._coords_to_square(event)
        if to_sq is None:
            return

        board = self.state.get_board()
        move = chess.Move(from_sq, to_sq)

        # clear drag state
        self.drag_data["from_square"] = None
        self.drag_data["piece"] = None

        # clear highlights
        self.renderer.clear_highlights()

        # validate move
        if move in board.legal_moves:
            self.state.apply_move(move)
            self.renderer.draw_board()

            # Log move
            color_label = "White" if board.turn == chess.BLACK else "Black"
            player_label = "User" if (
                (color_label == "White" and self.engine.white_model is None) or
                (color_label == "Black" and self.engine.black_model is None)
            ) else "LLM"
            self._log_move(color_label, player_label, move.from_square, move.to_square)

            # Visuals
            self._highlight_last_move(move.from_square, move.to_square)
            self._clear_engine_arrow()
            self._draw_eval_for_current_position()
            self._update_turn_indicator()

            # Maybe LLM responds
            self._maybe_llm_move()


# ========================================================
# Visual Helpers Section
# ========================================================
    # -------------------------
    # Turn Indicator
    # -------------------------
    def _update_turn_indicator(self):
        board = self.state.get_board()
        color = "White" if board.turn == chess.WHITE else "Black"

        if color == "White":
            player = "User" if self.engine.white_model is None else self.engine.white_model
        else:
            player = "User" if self.engine.black_model is None else self.engine.black_model

        self.turn_label.config(text=f"Turn: {color} ({player})")

    # -------------------------
    # Thinking Indicator
    # -------------------------
    def _set_thinking(self, is_thinking: bool):
        self.thinking_label.config(text="Thinking..." if is_thinking else "")

    # -------------------------
    # Eval Bar Drawing
    # -------------------------
    def _draw_eval_bar(self, score: float):
        """
        score: centipawn-like, positive = white better, negative = black better.
        We clamp to [-5, 5] for visualization.
        """
        self.eval_canvas.delete("all")

        # background
        self.eval_canvas.create_rectangle(0, 0, 80, 16, fill="#222222", outline="#555555")

        # clamp score
        max_cp = 500.0
        if score > max_cp:
            score = max_cp
        if score < -max_cp:
            score = -max_cp

        # map score to [0, 80]
        mid = 40
        offset = int((score / max_cp) * mid)
        bar_center = mid + offset

        # white side (left)
        self.eval_canvas.create_rectangle(0, 0, bar_center, 16, fill="#ffffff", outline="")
        # black side (right)
        self.eval_canvas.create_rectangle(bar_center, 0, 80, 16, fill="#000000", outline="")

        # center line
        self.eval_canvas.create_line(40, 0, 40, 16, fill="#888888")

    # ---------------------------------------
    # Draw Eval For Current Position
    # ---------------------------------------
    def _draw_eval_for_current_position(self):
        """
        If the chess engine supports evaluation, use it.
        Otherwise, draw a neutral bar.
        """
        board = self.state.get_board()
        score = 0.0

        if hasattr(self.chess_engine, "evaluate"):
            try:
                score = float(self.chess_engine.evaluate(board))
            except Exception:
                score = 0.0

        self._draw_eval_bar(score)

    # -------------------------
    # Last Move Highlight
    # -------------------------
    def _highlight_last_move(self, from_sq, to_sq):
        self.last_move_from = from_sq
        self.last_move_to = to_sq

        self.renderer.clear_highlights()

        from_file = chess.square_file(from_sq)
        from_rank = chess.square_rank(from_sq)
        to_file = chess.square_file(to_sq)
        to_rank = chess.square_rank(to_sq)

        self.renderer.highlight_square(from_file, from_rank)
        self.renderer.highlight_square(to_file, to_rank)

    # -------------------------
    # Arrow Helpers
    # -------------------------
    def _clear_arrows(self):
        if self.last_arrow_id is not None:
            self.board_canvas.delete(self.last_arrow_id)
            self.last_arrow_id = None
        if self.engine_arrow_id is not None:
            self.board_canvas.delete(self.engine_arrow_id)
            self.engine_arrow_id = None

    # -----------------------
    # Clear Engine Arrow
    # -----------------------
    def _clear_engine_arrow(self):
        if self.engine_arrow_id is not None:
            self.board_canvas.delete(self.engine_arrow_id)
            self.engine_arrow_id = None

    # -----------------------
    # Draw Engine Arrow
    # -----------------------
    def _draw_engine_arrow(self, move: chess.Move):
        self._clear_engine_arrow()

        size = self.renderer.square_size
        from_file = chess.square_file(move.from_square)
        from_rank = chess.square_rank(move.from_square)
        to_file = chess.square_file(move.to_square)
        to_rank = chess.square_rank(move.to_square)

        x1 = from_file * size + size / 2
        y1 = (7 - from_rank) * size + size / 2
        x2 = to_file * size + size / 2
        y2 = (7 - to_rank) * size + size / 2

        self.engine_arrow_id = self.board_canvas.create_line(
            x1, y1, x2, y2,
            fill="#FFB74D",
            width=3,
            arrow=tk.LAST
        )

    # -----------------------
    # Declare Winner
    # -----------------------
    def _declare_winner(self):
        board = self.state.get_board()

        # Checkmate
        if board.is_checkmate():
            winner = "White" if board.turn == chess.BLACK else "Black"
            self._log("Game Over")
            self._log(f"{winner} wins!")
            return

        # Draw conditions
        if board.is_stalemate():
            self._log("Game Over")
            self._log("Draw by stalemate.")
            return

        if board.is_insufficient_material():
            self._log("Game Over")
            self._log("Draw by insufficient material.")
            return

        if board.is_seventyfive_moves():
            self._log("Game Over")
            self._log("Draw by 75-move rule.")
            return

        if board.is_fivefold_repetition():
            self._log("Game Over")
            self._log("Draw by repetition.")
            return

        # Fallback to PGN result
        result = board.result()
        if result == "1-0":
            self._log("Game Over")
            self._log("White wins!")
        elif result == "0-1":
            self._log("Game Over")
            self._log("Black wins!")
        else:
            self._log("Game Over")
            self._log("Draw.")


# ========================================================
# Chat Section 
# ========================================================
    # ----------------
    # Send Message
    # ----------------
    def send_message(self):

        msg = self.input_var.get().strip()
        if not msg:
            return

        # User always logs as "user"
        self._log(f"User: {msg}", "user")
        self.input_var.set("")

        # If user is playing, treat input as a move
        if self.engine.mode in ("user_vs_llm", "user_vs_user"):
            if self._handle_user_move(msg):
                return

        # Otherwise, treat as chat
        self._handle_chat_message(msg)

    # ---------------------
    # Handle Chat Message
    # ---------------------
    def _handle_chat_message(self, msg):

        if not self.engine.chat_model:
            self._log("No chat model selected.")
            return

        board = self.state.get_board()
        history = self.state.move_history()

        response = self.chat_selector.respond(msg, board, history)
        if not response:
            return

        # Determine label + tag based on chat mode
        mode = self.chat_mode_var.get()

        if mode == "Coach":
            label = "Coach"
            tag = "coach"

        elif mode == "Commentator":
            label = "Commentator"
            tag = "commentator"

        else:
            # Neutral fallback → use model name
            label = self.engine.chat_model
            tag = "llm"

        self._log(f"{label}: {response}", tag)

    # -------------------------
    # Auto Chat On Move
    # -------------------------
    def _auto_chat_on_move(self, board_before_move):
        """
        When in Coach or Commentator mode, auto-generate commentary
        after each LLM move.
        """
        if not self.engine.chat_model:
            return

        mode = self.chat_mode_var.get()
        if mode not in ("Coach", "Commentator"):
            return

        board = self.state.get_board()
        history = self.state.move_history()

        # Simple generic prompt for commentary
        prompt = "Comment on the last move and the current position."

        response = self.chat_selector.respond(prompt, board, history)
        if not response:
            return

        if mode == "Coach":
            label = "Coach"
            tag = "coach"
        else:
            label = "Commentator"
            tag = "commentator"

        self._log(f"{label}: {response}", tag)


# ==========================================
# Log Section
# ==========================================
    # ------------
    # Log
    # ------------
    def _log(self, text, tag=None):

        self.chat_box.config(state="normal")
        if tag:
            self.chat_box.insert(tk.END, text + "\n", tag)
        else:
            self.chat_box.insert(tk.END, text + "\n")
        self.chat_box.config(state="disabled")
        self.chat_box.see(tk.END)

    # ------------
    # Log Move
    # ------------
    def _log_move(self, color_label, player_label, move_from, move_to):

        from_name = chess.square_name(move_from)
        to_name = chess.square_name(move_to)
        line = f"{color_label} - {player_label}:\n {from_name} -> {to_name}"
        self.move_log.config(state="normal")
        self.move_log.insert(tk.END, line + "\n")
        self.move_log.config(state="disabled")
        self.move_log.see(tk.END)


# ====================================================
# Event Handling Section
# ====================================================
    # ---------------------
    # On Close
    # ---------------------
    def _on_close(self):
        # Stop Stockfish cleanly
        try:
            if self.chess_engine and hasattr(self.chess_engine, "engine"):
                self.chess_engine.engine.quit()
        except:
            pass

        # Cancel any pending after() callbacks
        try:
            self.root.after_cancel(self._maybe_llm_move)
        except:
            pass

        # Destroy the window
        self.root.destroy()

        # Force Python to exit (kills lingering threads)
        os._exit(0)


# ========================= #
# ENTRY POINT               #
# ========================= #
if __name__ == "__main__":
    root = tk.Tk()
    app = ChessWindow(root)
    root.mainloop()

