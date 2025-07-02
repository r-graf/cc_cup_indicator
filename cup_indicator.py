from pathlib import Path
from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtGui import QPainter, QColor, QBrush, QPolygonF, QFontMetrics, QPen, QLinearGradient
from PySide6.QtCore import Qt, QRectF, QPointF, QSize, Signal
from PySide6.QtSvg import QSvgRenderer


class CupIndicator(QWidget):

    """
    Custom QWidget zur Visualisierung eines Getränkes in einer Tasse mit konfigurierbarem Füllstand,
    Getränketyp, Milchanteil und Intensität.
    
    Signale:
        fillChanged(float): Signal bei Änderung des Füllstands (0.0 bis 1.0).
        drinkTypeChanged(str): Signal bei Änderung des Getränketyps ("kaffee", "tee", "unknown").
        milkChanged(bool, float): Signal bei Änderung des Milchstatus (Bool) und Milchmenge (0-100).
        intensityChanged(float): Signal bei Änderung der Intensität (0.0 bis 1.0).
    """

    fillChanged = Signal(float)
    drinkTypeChanged = Signal(str)
    milkChanged = Signal(bool, float)
    intensityChanged = Signal(float)

    def __init__(self, parent=None):

        """
        Initialisiert das CupIndicator-Widget mit Standardwerten und lädt die SVG-Grafiken.
        Setzt außerdem die Größenrichtlinien.
        """

        super().__init__(parent)
        self._fill_percent = 1.0
        self._color = QColor("#412e20")
        self._drink_type = "none"
        self._milk = False
        self._amount_milk = 0.0
        self._gradient = QLinearGradient()
        self._intensity = 1.0

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
            print(f"SVG nicht gefunden oder ungültig: {cup_svg_path}")
        else:
            print("SVG Renderer ist valide.")
    
    # Policy Einstellung
    def hasHeightForWidth(self) -> bool:
        """Gibt an, dass die Höhe von der Breite abhängt."""
        return True
    
    # Policy Einstellung
    def heightForWidth(self, width: int) -> int:
        """Berechnet die Höhe basierend auf der aktuellen Breite (Quadratische Form)."""
        return width

    # Policy Definierung
    def sizeHint(self) -> QSize:
        """Empfiehlt eine Standardgröße basierend auf der Schriftgröße, mindestens 100x100."""
        font_size = QFontMetrics(self.font()).height()
        size = max(4 * font_size, 100)
        return QSize(size, size)

    @property
    def fill_percent(self):
        """Gibt den aktuellen Füllstand als Wert zwischen 0.0 und 1.0 zurück."""
        return self._fill_percent

    @fill_percent.setter
    def fill_percent(self, percent: float):
        """
        Setzt den Füllstand der Tasse.
        Der Wert wird auf den Bereich 0.0 bis 1.0 begrenzt.
        Bei unbekanntem Getränketyp wird der Füllstand auf 1.0 gesetzt.
        Emitiert das fillChanged-Signal.
        """
        if self._drink_type == "unknown":
            self._fill_percent = 1.0
        else:
            self._fill_percent = max(0.0, min(1.0, percent))
        self.fillChanged.emit(self._fill_percent)
        self.update()

    @property
    def drink_type(self):
        """Gibt den aktuellen Getränketyp zurück ("kaffee", "tee", "unknown")."""
        return self._drink_type

    @drink_type.setter
    def drink_type(self, drink_type: str):
        """
        Setzt den Getränketyp und passt die Farbe sowie das Overlay (z.B. Teebeutel) entsprechend an.
        Unterstützt "kaffee" und "tee". Bei unbekanntem Typ wird ein rotes X angezeigt.
        Emitiert das drinkTypeChanged-Signal.
        """
        self._drink_type = drink_type.lower()
        if self._drink_type == "kaffee":
            self._color = QColor("#412e20")
            self.overlay_svg_renderer = None 
        elif self._drink_type == "tee":
            self._color = QColor("#c68e17")
            teabag_svg_path = Path(__file__).parent / "resources" / "icon.teabag.svg"

            if teabag_svg_path.exists():
                self.overlay_svg_renderer = QSvgRenderer(str(teabag_svg_path))
            else:
                print(f"Teebeutel-SVG nicht gefunden: {teabag_svg_path}")
        else:
            self._drink_type = "unknown"
            self.overlay_svg_renderer = None  # Teebeutel sofort deaktivieren
            self._color = QColor("#ff007f")
        self.drinkTypeChanged.emit(self._drink_type)
        self.update()

    @property
    def milk(self):
        """Gibt zurück, ob Milch hinzugefügt wurde."""
        return self._milk

    @milk.setter
    def milk(self, value: tuple[bool, float]):
        """
        Setzt den Milchstatus und die Milchmenge (0-100 %).
        Erzeugt einen vertikalen Farbverlauf für die Milch.
        Emitiert das milkChanged-Signal.
        
        Args:
            value (tuple[bool, float]): Tuple mit (Milch aktiv?, Milchmenge in %)
        """
        milk, amount = value
        self._milk = milk
        self._amount_milk = max(0, min( 100, amount))
        if self._milk == True:
            gradient = QLinearGradient(0, 0, 0, 1)  # Vertikaler Gradient
            gradient.setCoordinateMode(QLinearGradient.ObjectBoundingMode)
            color = self._color
            gradient.setColorAt(0.0, QColor("#f9f4ef"))
            gradient.setColorAt(0.2 * (amount/100), QColor("#f9f4ef"))
            gradient.setColorAt(0.6 * (amount/100), color)
            self._gradient = gradient
        self.milkChanged.emit(self._milk, self._amount_milk)
        self.update()

    @property
    def intensity(self):
        """Gibt die aktuelle Intensität des Getränks zurück (0.0 bis 1.0)."""
        return self._intensity

    @intensity.setter
    def intensity(self, intensity: float):
        """
        Setzt die Intensität (0 bis 10) des Getränks und interpoliert die Farbe.
        Ignoriert den Wert, wenn der Getränketyp unbekannt ist.
        Emitiert das intensityChanged-Signal.
        """
        if (self._drink_type == "unknown"):
            return
        
        self._intensity = max(0, min((intensity/10), 1))

        if (self._drink_type == "kaffee"):
            start_rgb = (147, 104, 73)   # #936849 Hellbraun
            end_rgb   = ( 65,  46, 32)   # #412e20 Dunkelbraun
        if (self._drink_type == "tee"):
            start_rgb = (232, 177, 61)   # #e8b13d helles Ocker
            end_rgb   = (139,  99, 16)   # #8b6310 dunkles Ocker

        # Interpolation
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * self._intensity)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * self._intensity)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * self._intensity)

        self._color = QColor(r, g, b)
        self.intensityChanged.emit(self._intensity)
        self.update()

    def paintEvent(self, event):
        """
        Überschreibt das Paint-Event, um die Tasse mit Füllstand, Milch und ggf. Teebeutel oder
        Fehleranzeige (X) zu zeichnen.
        """
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
            fill_top_y = cup_bottom_y - self._fill_percent * cup_height
            relative_fill_height = cup_bottom_y - fill_top_y

            slope = 20 / 165  # aus SVG
            bottom_width = svg_rect.width() * 0.55
            top_width = bottom_width + 1.55 * (relative_fill_height * slope)

            center_x = svg_rect.center().x() - side * 0.095  # ggf. Feinkorrektur

            fill_polygon = QPolygonF([
                QPointF(center_x - bottom_width / 2, cup_bottom_y),
                QPointF(center_x + bottom_width / 2, cup_bottom_y),
                QPointF(center_x + top_width / 2, fill_top_y),
                QPointF(center_x - top_width / 2, fill_top_y),
            ])

            # Flüssigkeit zeichnen
            pen = QPen(QColor("black"))
            pen.setWidth(2)   # z.B. 2 Pixel dick
            painter.setPen(pen)
            if self._milk == True and self._drink_type != "unknown":
                painter.setBrush(QBrush(self._gradient))
            else:
                painter.setBrush(QBrush(self._color))
            painter.drawPolygon(fill_polygon)

            # Cup SVG darüber rendern
            self.base_svg_renderer.render(painter, svg_rect)

            # Wenn Getränk nicht erkannt wurde: "X" anzeigen und Teebeutel deaktivieren
            if self._drink_type == "unknown":
                self.overlay_svg_renderer = None  # Teebeutel deaktivieren

                font = painter.font()
                font.setPointSize(int(side * 0.3))
                font.setBold(True)
                painter.setFont(font)

                x_shift = svg_rect.center().x() - (side * 0.25)
                y_pos = svg_rect.center().y() + (side * 0.2)

                painter.setPen(QPen(QColor("white"), 4))
                painter.drawText(QPointF(x_shift, y_pos), "X")
            
            # Teebeutel SVG darüber rendern
            if self.overlay_svg_renderer and self.overlay_svg_renderer.isValid():
                teabag_rect = QRectF(
                    svg_rect.left() - svg_rect.height() * 0.1,
                    svg_rect.top() - svg_rect.height() * 0.03,
                    svg_rect.width() * 0.6,
                    svg_rect.height() * 0.6
                )
                
                self.overlay_svg_renderer.render(painter, teabag_rect)
