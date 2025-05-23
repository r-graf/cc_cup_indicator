# main.py

import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton
)

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
        self.drink_selector.addItems(["Kaffee", "Tee"])
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

        # Layout erstellen
        MainWidget.setLayout(Layout)
        self.setCentralWidget(MainWidget)

    def print_input(self):
        drink = self.drink_selector.currentText()
        amount = self.amount_input.text()
        print(f"Auswahl: {drink}, Füllmenge: {amount} ml")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())