# file: chess_board_widget.py

from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QColor, QFont, QPixmap, QPalette
from PyQt6.QtCore import Qt, QEvent
import chess
import sys
import os

BOARD_SIZE = 8
SQUARE_SIZE = 80
ASSET_PATH = "assets/pieces/default/"

THEMES = {
    "light": {
        "light_square": QColor("#EEEED2"),
        "dark_square": QColor("#769656"),
        "label": QColor("#000000")
    },
    "dark": {
        "light_square": QColor("#EEEED2"),
        "dark_square": QColor("#769656"),
        "label": QColor("#FFFFFF")
    }
}

def detect_system_theme():
    palette = QApplication.instance().palette()
    bg_color = palette.color(QPalette.ColorRole.Window)
    return "dark" if bg_color.lightness() < 128 else "light"

class BoardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.update_theme()
        self.setFixedSize(SQUARE_SIZE * BOARD_SIZE + 40, SQUARE_SIZE * BOARD_SIZE + 40)
        self.installEventFilter(self)

        self.board = chess.Board()
        self.piece_images = self.load_piece_images()

    def update_theme(self):
        theme = detect_system_theme()
        self.theme = THEMES[theme]

    def load_piece_images(self):
        symbols = ['P', 'N', 'B', 'R', 'Q', 'K']
        images = {}
        for color in ['w', 'b']:
            for symbol in symbols:
                piece = color + symbol
                path = os.path.join(ASSET_PATH, f"{piece}.png")
                if os.path.exists(path):
                    original = QPixmap(path)
                    images[piece] = original.scaled(
                        SQUARE_SIZE, SQUARE_SIZE,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                else:
                    print(f"[WARN] Missing piece asset: {path}")
        return images

    def event(self, event):
        if event.type() == QEvent.Type.PaletteChange:
            self.update_theme()
            self.update()
        return super().event(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        for rank in range(BOARD_SIZE):
            for file in range(BOARD_SIZE):
                x = file * SQUARE_SIZE + 30
                y = (7 - rank) * SQUARE_SIZE + 10
                square_color = self.theme["light_square"] if (file + rank) % 2 == 0 else self.theme["dark_square"]
                painter.fillRect(x, y, SQUARE_SIZE, SQUARE_SIZE, square_color)

                painter.setPen(self.theme["label"])
                painter.setFont(QFont("Arial", 10))
                if file == 0:
                    painter.drawText(10, y + SQUARE_SIZE // 2 + 5, str(rank + 1))
                if rank == 0:
                    painter.drawText(x + SQUARE_SIZE // 2 - 5, SQUARE_SIZE * 8 + 25, chr(ord('a') + file))

        for square, piece in self.board.piece_map().items():
            file = chess.square_file(square)
            rank = chess.square_rank(square)
            x = file * SQUARE_SIZE + 30
            y = (7 - rank) * SQUARE_SIZE + 10

            symbol = piece.symbol()
            key = ('w' if symbol.isupper() else 'b') + symbol.upper()
            if key in self.piece_images:
                painter.drawPixmap(x, y, self.piece_images[key])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BoardWidget()
    window.setWindowTitle("Chess Board - Pieces")
    window.show()
    sys.exit(app.exec())
