# main.py

from cup_indicator import CupIndicator
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QSlider
)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self): 
        super().__init__()
        self.setWindowTitle("Getränkekonfigurator Demo")

        # Widget und Layout
        MainWidget = QWidget()
        Layout = QVBoxLayout()

        # Auswahl Getränke Dropdown Menü
        self.drink_selector = QComboBox()
        self.drink_selector.addItems(["Kaffee", "Tee", "Schnaps"])
        Layout.addWidget(QLabel("Getränk auswählen:"))
        Layout.addWidget(self.drink_selector)
        
        # Eingabe Füllmenge
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Füllmenge in ml")
        Layout.addWidget(QLabel("Füllmenge:"))
        Layout.addWidget(self.amount_input)

        # Eingabe Ziehzeit bzw. Intesivität
        self.intensity_input = QSlider(Qt.Horizontal)
        self.intensity_input.setMinimum(0)
        self.intensity_input.setMaximum(10)
        Layout.addWidget(QLabel("Intensivität:"))
        Layout.addWidget(self.intensity_input)

        # Button Anzeigen, auch für Debugging
        self.submit_button = QPushButton("Anzeigen")
        self.submit_button.clicked.connect(self.print_input)
        Layout.addWidget(self.submit_button)

        # Custom Control: CupIndicator
        self.cup = CupIndicator()
        Layout.addWidget(QLabel("Visualisierung:"))
        Layout.addWidget(self.cup)


        # Layout erstellen
        MainWidget.setLayout(Layout)
        self.setCentralWidget(MainWidget)

    def print_input(self):
        drink = self.drink_selector.currentText()
        amount = self.amount_input.text()
        intensity = self.intensity_input.value()
        print(f"Auswahl: {drink}, Füllmenge: {amount} ml, Intensität: {intensity}")
        
        # Simpler Test: z. B. 250ml = 100% Füllstand
        try:
            ml = int(amount)
            fill = min(1.0, ml / 250)
        except ValueError:
            fill = 0.0

        self.cup.set_drink(drink)
        self.cup.set_fill_percent(fill)
        self.cup.set_intensity(intensity)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())