from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QSize
import chess

TILE_SIZE = 80

class ChessBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chess GUI")
        self.setFixedSize(TILE_SIZE * 8, TILE_SIZE * 8)
        self.board = chess.Board()
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.squares = {}

        self.init_board()

    def init_board(self):
        for row in range(8):
            for col in range(8):
                label = QLabel()
                label.setFixedSize(QSize(TILE_SIZE, TILE_SIZE))
                label.setStyleSheet(f"background-color: {'#e0fcde' if (row+col)%2==0 else '#3a7a36'}")
                self.layout.addWidget(label, 7-row, col)  # Flip row for white bottom
                self.squares[(row, col)] = label
