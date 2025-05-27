from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QBrush
from PySide6.QtCore import Qt, QRectF

class CupIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fill_percent = 0.5
        self.color = QColor("#6f4e37")

    def set_fill_percent(self, percent: float):
        if self.color == QColor("#ff007f"):
            self.fill_percent = 1
        else:
            self.fill_percent = max(0.0, min(1.0, percent))
        self.update()

    def set_color(self, drink_type: str):
        if drink_type.lower() == "kaffee":
            self.color = QColor("#6f4e37")
        elif drink_type.lower() == "tee":
            self.color = QColor("#c68e17")
        else:
            self.color = QColor("#ff007f")
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()

        cup_rect = QRectF(width * 0.2, height * 0.1, width * 0.6, height * 0.8)
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(cup_rect, 20, 20)

        fill_height = cup_rect.height() * self.fill_percent
        fill_rect = QRectF(
            cup_rect.left(),
            cup_rect.bottom() - fill_height,
            cup_rect.width(),
            fill_height
        )

        painter.setBrush(QBrush(self.color))
        painter.setPen(Qt.NoPen)
        painter.drawRect(fill_rect)

        # Henkel
        handle_radius = cup_rect.height() * 0.3
        handle_x = cup_rect.right()
        handle_y = cup_rect.center().y()
        painter.setPen(QPen(Qt.black, 3))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(handle_x - 5, handle_y - handle_radius / 2, handle_radius, handle_radius)
