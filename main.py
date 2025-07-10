from PyQt6.QtWidgets import QApplication
from chessboard import ChessBoard
import sys

app = QApplication(sys.argv)
board = ChessBoard()
board.show()
sys.exit(app.exec())
