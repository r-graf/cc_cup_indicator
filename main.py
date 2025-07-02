# main.py

from cup_indicator import CupIndicator
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QSlider, QCheckBox
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

        # Haken für die Milchauswahl
        self.milk_selector = QCheckBox("Milch", self)
        self.milk_amount = QSlider(Qt.Horizontal)
        Layout.addWidget(QLabel("Milch"))
        Layout.addWidget(self.milk_selector)
        Layout.addWidget(self.milk_amount)
        
        # Eingabe Füllmenge
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Füllmenge in ml")
        Layout.addWidget(QLabel("Füllmenge: [ml, 0 : 250]"))
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
        self.cup.fillChanged.connect(self.on_fill_changed)
        self.cup.drinkTypeChanged.connect(self.on_drink_type_changed)
        self.cup.milkChanged.connect(self.on_milk_changed)
        self.cup.intensityChanged.connect(self.on_intensity_changed)
        Layout.addWidget(QLabel("Visualisierung:"))
        Layout.addWidget(self.cup)


        # Layout erstellen
        MainWidget.setLayout(Layout)
        self.setCentralWidget(MainWidget)

    def print_input(self):
        drink = self.drink_selector.currentText()
        amount = self.amount_input.text()
        fill_percent = self.cup.fill_percent
        intensity = self.intensity_input.value()
        milk = self.milk_selector.isChecked()
        milk_amount = self.milk_amount.value()
        print(f"Auswahl: {drink}, Füllmenge: {amount} ml, relative Füllmenge: {fill_percent}, Intensität: {intensity}, Milch: {milk}, Milchmenge: {milk_amount}")
        
        # Simpler Test: z. B. 250ml = 100% Füllstand
        try:
            ml = int(amount)
            fill = min(1.0, ml / 250)
        except ValueError:
            fill = 0.0

        self.cup.drink_type=drink
        self.cup.fill_percent = fill
        self.cup.intensity = intensity
        self.cup.milk = (milk, milk_amount)

    def on_fill_changed(self, new_fill):
        print(f"[Signal] Füllstand wurde geändert auf: {new_fill:.2f}")

    def on_drink_type_changed(self, new_type):
        print(f"[Signal] Getränketyp wurde geändert auf: {new_type}")

    def on_milk_changed(self, has_milk: bool, amount: float):
        print(f"[Signal] Milch geändert: {has_milk}, Menge: {amount}")

    def on_intensity_changed(self, intensity: float):
        print(f"[Signal] Intensität geändert auf: {intensity}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
