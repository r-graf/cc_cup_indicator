from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient, QPolygonF
from PySide6.QtCore import Qt, QRectF, QPointF

class CupIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fill_percent = 0.5
        self.color = QColor("#6f4e37")

    ## Füllstand einstellen
    def set_fill_percent(self, percent: float):
        if self.color == QColor("#ff007f"):
            self.fill_percent = 1
        else:
            self.fill_percent = max(0.0, min(1.0, percent))
        self.update()

    ## Flüssigkeitsfarbe einstellenelf.color 
    def set_color(self, drink_type: str):
        if drink_type.lower() == "kaffee":
            self.color = QColor("#6f4e37")
        elif drink_type.lower() == "tee":
            self.color = QColor("#c68e17")
        else:
            self.color = QColor("#ff007f")
        self.update()


    ## paintEvent
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        full_height = self.height()
        top_width = 0.75 * full_height
        bottom_width = 0.5 * top_width

        center_x = self.width() / 2
        top_y = 0
        bottom_y = full_height

        # X-Koordinaten berechnen
        top_left_x = center_x - top_width / 2
        top_right_x = center_x + top_width / 2
        bottom_left_x = center_x - bottom_width / 2
        bottom_right_x = center_x + bottom_width / 2

        # Trapez zeichnen
        trapezoid = QPolygonF([
            QPointF(top_left_x, top_y),
            QPointF(top_right_x, top_y),
            QPointF(bottom_right_x, bottom_y),
            QPointF(bottom_left_x, bottom_y)
        ])

        # Rahmen zeichnen
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(QBrush(Qt.NoBrush))
        painter.drawPolygon(trapezoid)

        # Füllung berechnen
        fill_height = full_height * self.fill_percent
        fill_top_y = bottom_y - fill_height
        fill = QPolygonF([
            QPointF(bottom_left_x, bottom_y),
            QPointF(bottom_right_x, bottom_y),
            QPointF(top_right_x, fill_top_y),
            QPointF(top_left_x, fill_top_y),
        ])

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.color))
        painter.drawPolygon(fill)
