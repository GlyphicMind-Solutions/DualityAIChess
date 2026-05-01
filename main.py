# ./DualityAIChess/main.py
# LLM-Compatible Chess Engine
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions LLC.



#system import
import tkinter as tk

#local import
from gui.chess_window import ChessWindow



# ========================= #
# ENTRY POINT               #
# ========================= #
if __name__ == "__main__":
    root = tk.Tk()
    app = ChessWindow(root)
    root.mainloop()

