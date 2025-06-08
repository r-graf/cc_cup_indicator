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
        milk = self.milk_selector.isChecked()
        milk_amount = self.milk_amount.value()
        print(f"Auswahl: {drink}, Füllmenge: {amount} ml, Intensität: {intensity}, Milch: {milk}, Milchmenge: {milk_amount}")
        
        # Simpler Test: z. B. 250ml = 100% Füllstand
        try:
            ml = int(amount)
            fill = min(1.0, ml / 250)
        except ValueError:
            fill = 0.0

        self.cup.set_drink(drink)
        self.cup.set_fill_percent(fill)
        self.cup.set_intensity(intensity)
        self.cup.set_milk(milk, milk_amount)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())