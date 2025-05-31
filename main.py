# main.py

from cup_indicator import CupIndicator
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton
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
        print(f"Auswahl: {drink}, Füllmenge: {amount} ml")
        
        # Simpler Test: z. B. 250ml = 50% Füllstand
        try:
            ml = int(amount)
            fill = min(1.0, ml / 500)
        except ValueError:
            fill = 0.0

        self.cup.set_color(drink)
        self.cup.set_fill_percent(fill)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())