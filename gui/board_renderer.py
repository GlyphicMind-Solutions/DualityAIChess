# ./DualityAIChess/gui/chess_window.py
# LLM-Compatible Chess Engine GUI Interface
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions LLC.



#system imports
import os, chess
import tkinter as tk
from PIL import Image, ImageTk



# ==============================
# BOARD RENDERER CLASS
# ==============================
class BoardRenderer:
    """
    Renders the chessboard with a custom background image (duality glyph)
    and themed angelic/demonic pieces.
    """
    # ----------------
    # Initialize
    # ----------------
    def __init__(self, canvas: tk.Canvas, board: chess.Board):

        #canvas-board
        self.canvas = canvas
        self.board = board
        self.square_size = 60
        self.images = {}

        # background
        self.background_image_normal = None
        self.background_image_reversed = None
        self.background_tk = None
        self._load_background()

        #game pieces
        self._load_piece_images()

        #highlights
        self.highlight_items = []


# ====================================
# Loading Section
# ====================================
    # ----------------------------
    # Load Background
    # ----------------------------
    def _load_background(self):
        base = os.path.join(os.getcwd(), "assets", "board")

        normal_path = os.path.join(base, "duality_board.png")
        reversed_path = os.path.join(base, "duality_board_reversed.png")

        if os.path.exists(normal_path):
            self.background_image_normal = Image.open(normal_path)
        else:
            print(f"[BoardRenderer] Missing normal board: {normal_path}")

        if os.path.exists(reversed_path):
            self.background_image_reversed = Image.open(reversed_path)
        else:
            print(f"[BoardRenderer] Missing reversed board: {reversed_path}")

    # ---------------------------
    # Load Piece Images
    # ---------------------------
    def _load_piece_images(self):
        base_path = os.path.join(os.getcwd(), "assets", "pieces")

        piece_map = {
            "P": ("angelic", "white_pawn.png"),
            "N": ("angelic", "white_knight.png"),
            "B": ("angelic", "white_bishop.png"),
            "R": ("angelic", "white_rook.png"),
            "Q": ("angelic", "white_queen.png"),
            "K": ("angelic", "white_king.png"),

            "p": ("demonic", "black_pawn.png"),
            "n": ("demonic", "black_knight.png"),
            "b": ("demonic", "black_bishop.png"),
            "r": ("demonic", "black_rook.png"),
            "q": ("demonic", "black_queen.png"),
            "k": ("demonic", "black_king.png"),
        }

        for piece, (folder, filename) in piece_map.items():
            path = os.path.join(base_path, folder, filename)
            if not os.path.exists(path):
                print(f"[BoardRenderer] Missing piece image: {path}")
                continue

            img = Image.open(path)
            self.images[piece] = img


# ===============================================
# Draw Section
# ===============================================
    # -------------------
    # Draw Board
    # -------------------
    def draw_board(self):
        # Fixed board size (matches old 8x8 * 60px)
        width = 8 * self.square_size
        height = 8 * self.square_size

        # Clear canvas
        self.canvas.delete("all")

        # Draw background if available, else fallback to squares
        self._draw_background(width, height)

        # Draw pieces on top
        self._draw_pieces()

    # ---------------------
    # Draw Background
    # ---------------------
    def _draw_background(self, width, height):
        # Choose background based on whose turn it is
        white_to_move = self.board.turn == chess.WHITE

        img = (
            self.background_image_normal if white_to_move
            else self.background_image_reversed
        )

        if not img:
            return

        resized = img.resize((width, height), Image.LANCZOS)
        self.background_tk = ImageTk.PhotoImage(resized)
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_tk)

    # ---------------------
    # Draw Squares
    # ---------------------
    def _draw_squares(self):
        light_color = "#E0F7FA"  # translucent white
        dark_color = "#263238"   # translucent black

        for rank in range(8):
            for file in range(8):
                x1 = file * self.square_size
                y1 = rank * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size

                color = light_color if (rank + file) % 2 == 0 else dark_color
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#FFFF00", outline="", stipple="gray50")

    # -----------------------
    # Draw Pieces
    # -----------------------
    def _draw_pieces(self):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if not piece:
                continue

            symbol = piece.symbol()
            if symbol not in self.images:
                continue

            img = self.images[symbol]
            resized = img.resize((self.square_size, self.square_size), Image.LANCZOS)
            tk_img = ImageTk.PhotoImage(resized)

            if not hasattr(self, "_image_refs"):
                self._image_refs = []
            self._image_refs.append(tk_img)

            file = chess.square_file(square)
            rank = 7 - chess.square_rank(square)

            x = file * self.square_size
            y = rank * self.square_size

            self.canvas.create_image(x, y, anchor="nw", image=tk_img)


# ===============================================
# Highlighting Section
# ===============================================
    # -----------------------
    # Clear Highlights
    # -----------------------
    def clear_highlights(self):
        for item in self.highlight_items:
            self.canvas.delete(item)
        self.highlight_items.clear()

    # -----------------------
    # Highlight Square
    # -----------------------
    def highlight_square(self, file, rank, color="#00A2FF"):
        size = self.square_size
        x1 = file * size
        y1 = (7 - rank) * size
        x2 = x1 + size
        y2 = y1 + size

        item = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=color,
            outline="",
            stipple="gray50",   # <-- transparency simulation
            tags="highlight"
        )
        self.highlight_items.append(item)

    # -----------------------
    # Highlight Legal Moves
    # -----------------------
    def highlight_legal_moves(self, board, from_square):
        self.clear_highlights()

        file = chess.square_file(from_square)
        rank = chess.square_rank(from_square)
        self.highlight_square(file, rank, color="#FFF59D")  # selected square

        for move in board.legal_moves:
            if move.from_square == from_square:
                f = chess.square_file(move.to_square)
                r = chess.square_rank(move.to_square)
                item = self.canvas.create_rectangle(
                    f * self.square_size,
                    (7 - r) * self.square_size,
                    f * self.square_size + self.square_size,
                    (7 - r) * self.square_size + self.square_size,
                    fill="#B3E5FC",
                    outline="",
                    stipple="gray50",   # <-- transparency
                    tags="highlight"
                )
                self.highlight_items.append(item)
