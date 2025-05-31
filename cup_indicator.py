from pathlib import Path
from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtGui import QPainter, QColor, QBrush, QPolygonF, QFontMetrics
from PySide6.QtCore import Qt, QRectF, QPointF, QSize
from PySide6.QtSvg import QSvgRenderer


class CupIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fill_percent = 0.5
        self.color = QColor("#6f4e37")

        # SizePolicy mit height-for-width
        policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)

        # SVG laden
        svg_path = Path(__file__).parent / "resources" / "icon.tea.cup.optimized.svg"
        self.svg_renderer = QSvgRenderer(str(svg_path))
        if not svg_path.exists() or not self.svg_renderer.isValid():
            print(f"⚠️ SVG nicht gefunden oder ungültig: {svg_path}")
        else:
            print("✅ SVG Renderer ist valide.")

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, width: int) -> int:
        return width

    def sizeHint(self) -> QSize:
        font_size = QFontMetrics(self.font()).height()
        size = max(4 * font_size, 100)
        return QSize(size, size)

    def set_fill_percent(self, percent: float):
        """Setzt den Füllstand im Bereich 0.0–1.0."""
        if self.color == QColor("#ff007f"):
            self.fill_percent = 1.0
        else:
            self.fill_percent = max(0.0, min(1.0, percent))
        self.update()

    def set_color(self, drink_type: str):
        """Setzt die Farbe basierend auf dem Getränketyp."""
        drink_type = drink_type.lower()
        if drink_type == "kaffee":
            self.color = QColor("#6f4e37")
        elif drink_type == "tee":
            self.color = QColor("#c68e17")
        else:
            self.color = QColor("#ff007f")
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.white)

        # Quadrat innerhalb der aktuellen Größe
        side = min(self.width(), self.height())
        x = (self.width() - side) / 2
        y = (self.height() - side) / 2
        square = QRectF(x, y, side, side)

        # Geometrie für Flüssigkeit
        full_height = square.height()
        top_width = 0.75 * full_height
        bottom_width = 0.5 * top_width
        fill_height = full_height * self.fill_percent
        bottom_y = square.bottom()
        fill_top_y = bottom_y - fill_height
        center_x = square.center().x()

        # Füllform (Trapez)
        fill_shape = QPolygonF([
            QPointF(center_x - bottom_width / 2, bottom_y),
            QPointF(center_x + bottom_width / 2, bottom_y),
            QPointF(center_x + top_width / 2, fill_top_y),
            QPointF(center_x - top_width / 2, fill_top_y),
        ])

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.color))
        painter.drawPolygon(fill_shape)

        # SVG zeichnen (innerhalb Quadrat, mit Rand)
        if self.svg_renderer.isValid():
            margin = side * 0.1
            svg_rect = QRectF(
                square.left() + margin,
                square.top() + margin,
                side - 2 * margin,
                side - 2 * margin
            )
            self.svg_renderer.render(painter, svg_rect)
