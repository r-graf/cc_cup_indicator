from pathlib import Path
from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtGui import QPainter, QColor, QBrush, QPolygonF, QFontMetrics, QPen
from PySide6.QtCore import Qt, QRectF, QPointF, QSize
from PySide6.QtSvg import QSvgRenderer


class CupIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fill_percent = 1
        self.color = QColor("#6f4e37")
        self.background_color = QColor("white")

        # SizePolicy mit height-for-width
        policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)
        self.setMinimumSize(4 * QFontMetrics(self.font()).height(), 4 * QFontMetrics(self.font()).height())

        # SVG laden
        cup_svg_path = Path(__file__).parent / "resources" / "icon.cup.svg"
        self.base_svg_renderer = QSvgRenderer(str(cup_svg_path))
        self.overlay_svg_renderer = None

        if not cup_svg_path.exists() or not self.base_svg_renderer.isValid():
            print(f"⚠️ SVG nicht gefunden oder ungültig: {cup_svg_path}")
        else:
            print("✅ SVG Renderer ist valide.")
    
    # Policy Einstellung
    def hasHeightForWidth(self) -> bool:
        return True
    
    # Policy Einstellung
    def heightForWidth(self, width: int) -> int:
        return width

    # Policy Definierung
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

    def set_drink(self, drink_type: str):
        """Setzt die Farbe basierend auf dem Getränketyp."""
        drink_type = drink_type.lower()
        if drink_type == "kaffee":
            self.color = QColor("#6f4e37")
        elif drink_type == "tee":
            self.color = QColor("#c68e17")
            teabag_svg_path = Path(__file__).parent / "resources" / "icon.teabag.svg"

            if teabag_svg_path.exists():
                self.overlay_svg_renderer = QSvgRenderer(str(teabag_svg_path))
            else:
                print(f"⚠️ Teebeutel-SVG nicht gefunden: {teabag_svg_path}")
        else:
            self.color = QColor("#ff007f")
        self.update()

    def set_intensity(self, intensity: float):
        """Setzt die Intensität des Getränkes um"""
        alpha = (intensity * 25.5)
        color = self.color
        background = self.background_color
        color.setAlpha(alpha)
        background.setAlpha(max(100-alpha, 0))
        self.color = color
        self.background_color = background
        print(f"Setze Intensität: {intensity}, Alpha: {alpha}, Farbe: {self.color.name()} mit alpha={self.color.alpha()} und Hintergrund {self.background_color.alpha()}")
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

        # Hilfgrößen zur Positionierung
        margin = side * 0.1
        center_x = square.center().x() - (margin * 0.95)
        #bottom_y = square.bottom() - (margin * 1.3)
        cup_full_height = (square.height() - 2 * margin) * 0.8
        top_width = cup_full_height - (1.1 * margin)
        bottom_width = cup_full_height - margin

        # SVG zeichnen (innerhalb Quadrat, mit Rand)
        if self.base_svg_renderer.isValid():
            svg_rect = QRectF(
                square.left() + margin,
                square.top() + margin,
                side - 2 * margin,
                side - 2 * margin
            )

            
            # Fülltrapez berechnen
            cup_height = svg_rect.height() * 0.8
            cup_bottom_y = svg_rect.bottom() - svg_rect.height() * 0.05
            #cup_top_y = cup_bottom_y - cup_height
            fill_top_y = cup_bottom_y - self.fill_percent * cup_height
            relative_fill_height = cup_bottom_y - fill_top_y

            slope = 20 / 165  # aus SVG
            bottom_width = svg_rect.width() * 0.55
            top_width = bottom_width + 1.9 * (relative_fill_height * slope)

            center_x = svg_rect.center().x() - side * 0.095  # ggf. Feinkorrektur

            fill_polygon = QPolygonF([
                QPointF(center_x - bottom_width / 2, cup_bottom_y),
                QPointF(center_x + bottom_width / 2, cup_bottom_y),
                QPointF(center_x + top_width / 2, fill_top_y),
                QPointF(center_x - top_width / 2, fill_top_y),
            ])

            background_polygon = QPolygonF([
                QPointF(center_x - bottom_width / 2, cup_bottom_y),
                QPointF(center_x + bottom_width / 2, cup_bottom_y),
                QPointF(center_x + top_width / 2, fill_top_y),
                QPointF(center_x - top_width / 2, fill_top_y),
            ])

            # Hintergrund für intensity = 0, damit man die weiße Milch sehen kann
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor("#8ce5ff")))
            painter.drawPolygon(background_polygon)

            # Flüssigkeit zeichnen
            pen = QPen(QColor("black"))
            pen.setWidth(2)   # z.B. 2 Pixel dick
            painter.setPen(pen)
            painter.setBrush(QBrush(self.color))
            painter.drawPolygon(fill_polygon)

            # Cup SVG darüber rendern
            self.base_svg_renderer.render(painter, svg_rect)
            
            # Teebeutel SVG darüber rendern
            if self.overlay_svg_renderer and self.overlay_svg_renderer.isValid():
                teabag_rect = QRectF(
                    svg_rect.left() - svg_rect.height() * 0.1,
                    svg_rect.top() - svg_rect.height() * 0.03,
                    svg_rect.width() * 0.6,
                    svg_rect.height() * 0.6
                )
                self.overlay_svg_renderer.render(painter, teabag_rect)