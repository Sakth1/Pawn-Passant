from PyQt6.QtWidgets import QWidget, QApplication, QInputDialog
from PyQt6.QtGui import QPainter, QColor, QFont, QPixmap, QPalette, QPen, QBrush, QRadialGradient
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
        "label": QColor("#000000"),
        "highlight": QColor(255, 255, 0, 100),
        "last_move": QColor(0, 0, 255, 100),
        "move_hint": QColor(30, 30, 30, 180)
    },
    "dark": {
        "light_square": QColor("#EEEED2"),
        "dark_square": QColor("#769656"),
        "label": QColor("#FFFFFF"),
        "highlight": QColor(255, 255, 0, 100),
        "last_move": QColor(0, 0, 255, 100),
        "move_hint": QColor(30, 30, 30, 180)
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

        self.selected_square = None
        self.last_move = None
        self.legal_targets = []

        self.dragging = False
        self.drag_start_pos = None
        self.drag_piece = None
        self.drag_pixmap = None
        self.mouse_pos = None

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
                square = chess.square(file, rank)

                square_color = self.theme["light_square"] if (file + rank) % 2 == 0 else self.theme["dark_square"]
                painter.fillRect(x, y, SQUARE_SIZE, SQUARE_SIZE, square_color)

                if self.last_move and square in [self.last_move.from_square, self.last_move.to_square]:
                    painter.fillRect(x, y, SQUARE_SIZE, SQUARE_SIZE, self.theme["last_move"])

                painter.setPen(self.theme["label"])
                painter.setFont(QFont("Arial", 10))
                if file == 0:
                    painter.drawText(10, y + SQUARE_SIZE // 2 + 5, str(rank + 1))
                if rank == 0:
                    painter.drawText(x + SQUARE_SIZE // 2 - 5, SQUARE_SIZE * 8 + 25, chr(ord('a') + file))

        for target in self.legal_targets:
            file = chess.square_file(target)
            rank = chess.square_rank(target)
            cx = file * SQUARE_SIZE + 30 + SQUARE_SIZE // 2
            cy = (7 - rank) * SQUARE_SIZE + 10 + SQUARE_SIZE // 2
            radius = 10
            gradient = QRadialGradient(cx, cy, radius)
            color = self.theme["move_hint"]
            gradient.setColorAt(0.0, color)
            gradient.setColorAt(1.0, QColor(color.red(), color.green(), color.blue(), 0))
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(cx - radius, cy - radius, radius * 2, radius * 2)

        for square, piece in self.board.piece_map().items():
            if self.dragging and square == self.drag_start_pos:
                continue  # Skip drawing the dragged piece here
            file = chess.square_file(square)
            rank = chess.square_rank(square)
            x = file * SQUARE_SIZE + 30
            y = (7 - rank) * SQUARE_SIZE + 10
            symbol = piece.symbol()
            key = ('w' if symbol.isupper() else 'b') + symbol.upper()
            if key in self.piece_images:
                painter.drawPixmap(x, y, self.piece_images[key])

        # Draw the dragged piece following the mouse
        if self.dragging and self.drag_pixmap and self.mouse_pos:
            painter.drawPixmap(
                int(self.mouse_pos.x() - SQUARE_SIZE / 2),
                int(self.mouse_pos.y() - SQUARE_SIZE / 2),
                self.drag_pixmap
            )

    def mousePressEvent(self, event):
        square = self.xy_to_square(event.position().x(), event.position().y())
        if square is not None and self.board.piece_at(square):
            self.selected_square = square
            self.legal_targets = [move.to_square for move in self.board.legal_moves if move.from_square == square]

            # Prepare drag state
            piece = self.board.piece_at(square)
            symbol = piece.symbol()
            key = ('w' if symbol.isupper() else 'b') + symbol.upper()
            if key in self.piece_images:
                self.dragging = True
                self.drag_start_pos = square
                self.drag_piece = piece
                self.drag_pixmap = self.piece_images[key]
                self.mouse_pos = event.position()
            self.update()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.mouse_pos = event.position()
            self.update()

    def mouseReleaseEvent(self, event):
        if not self.dragging:
            return

        drop_square = self.xy_to_square(event.position().x(), event.position().y())
        move = None

        if drop_square is not None:
            move = chess.Move(self.drag_start_pos, drop_square)
            if self.drag_piece.piece_type == chess.PAWN and chess.square_rank(drop_square) in [0, 7]:
                promo_piece, ok = QInputDialog.getItem(self, "Pawn Promotion", "Promote to:", ["Queen", "Rook", "Bishop", "Knight"], 0, False)
                if ok:
                    promo_map = {"Queen": chess.QUEEN, "Rook": chess.ROOK, "Bishop": chess.BISHOP, "Knight": chess.KNIGHT}
                    move = chess.Move(self.drag_start_pos, drop_square, promotion=promo_map[promo_piece])

        if move and move in self.board.legal_moves:
            self.board.push(move)
            self.last_move = move

        self.dragging = False
        self.selected_square = None
        self.drag_start_pos = None
        self.drag_piece = None
        self.drag_pixmap = None
        self.legal_targets = []
        self.update()

    def xy_to_square(self, x, y):
        file = int((x - 30) // SQUARE_SIZE)
        rank = 7 - int((y - 10) // SQUARE_SIZE)
        if 0 <= file < 8 and 0 <= rank < 8:
            return chess.square(file, rank)
        return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BoardWidget()
    window.setWindowTitle("Chess Board - Move Pieces")
    window.show()
    sys.exit(app.exec())
