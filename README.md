# Entwicklung eines objektorientierten Customized Controls zur Visualisierung individueller Getränkekonfigurationen in PySide6

https://github.com/r-graf/cc_cup_indicator

## Kurzbeschreibung/Zielsetzung:
Im Rahmen dieser Modularbeit wurde ein benutzerdefiniertes Custom Control (CC) in PySide6 entwickelt, das eine grafische Tasse visualisiert. Dieses CC ermöglicht die dynamische Darstellung von konfigurierbaren Getränkeparametern wie Getränketyp (z.B. Kaffee oder Tee), Füllstand, Milchanteil und Intensität (z.B. Ziehzeit bei Tee oder Stärke bei Kaffee).

Die Logik zur Getränkeauswahl und -konfiguration ist in einer separaten Demoanwendung implementiert, die das Custom Control anschaulich nutzt und seine Wiederverwendbarkeit demonstriert.

## Technische Schwerpunkte:
**Objektorientierte Implementierung:** Entwicklung eines modularen, wartbaren Custom Controls als PySide6 QWidget

**Dynamische Visualisierung:** Zustandsabhängige Darstellung der Tasse inklusive Flüssigkeitsfüllstand, Milchanteil mit Farbverlauf, Getränkefarbe und Intensitätsinterpolation

**Responsive Layouts:** Unterstützung von Layout-Managern für flexible Größen- und Positionsanpassung

**Ereignisgesteuerte Architektur:** Signale für Zustandsänderungen ermöglichen die Integration in komplexe Anwendungen

**Ressourcenmanagement:** Nutzung von SVG-Grafiken für ansprechende und skalierbare Darstellungen

## Features

**Getränketyp-spezifische Darstellung:** Farbe und Overlays (z.B. Teebeutel-SVG bei Tee)

**Interpolation der Farbintensität:** Sanfter Farbverlauf zwischen hell und dunkel für realistische Darstellungen

**Milchdarstellung:** Vertikaler Farbverlauf mit anpassbarer Milchmenge

**Füllstand:** Prozentsatzgesteuerte Darstellung der Flüssigkeit im Tassenumriss

**Fehler-Handling:** Visuelles Feedback bei unbekannten Getränketypen (z.B. rotes „X“)

**Ereignisse (Signale):** Für Änderungen von Füllstand, Getränketyp und Milchstatus zur einfachen Anbindung an andere UI-Komponenten

## Nutzung/Beispiel

Das Custom Control CupIndicator kann wie ein normales Widget in Layouts verwendet werden. Seine Eigenschaften (fill_percent, drink_type, milk, intensity) lassen sich über Properties anpassen, und es stellt Signale (fillChanged, drinkTypeChanged, milkChanged) bereit, um auf Änderungen zu reagieren.

```python
from cup_indicator import CupIndicator
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

app = QApplication([])
window = QMainWindow()
container = QWidget()
layout = QVBoxLayout(container)

cup = CupIndicator()
cup.fill_percent = 0.75
cup.drink_type = "kaffee"
cup.milk = (True, 20)
cup.intensity = 7

layout.addWidget(cup)
window.setCentralWidget(container)
window.show()
app.exec()

```

## Abhängigkeiten

Python 3.7+

PySide6

SVG-Ressourcen im resources-Ordner (z.B. icon.cup.svg, icon.teabag.svg)

