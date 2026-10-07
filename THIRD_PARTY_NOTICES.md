# Herkunft und Lizenz

Martin hat MIT am 7. Oktober 2026 für den eigenen To-do-Code gewählt.
CLI, Tests, Beispiele und Agent-Skill stammen aus dem persönlichen Setup.
Die Git-Historie beginnt für das Panel bei Commit `4ef6140`; spätere Änderungen
passen Verhalten und Darstellung an. Ein vollständiger Nachweis jeder früheren
Codeübernahme lässt sich aus der Historie allein nicht ableiten.

Das Panel nutzt Omarchys Muster für Panel-Lebenszyklus, BarIconButton,
KeyboardPanel, PanelKeyCatcher, Abschnitte und Theme-Werte. Der MIT-Hinweis von
Omarchy bleibt vorsorglich im Paket erhalten. Die Komponenten selbst werden
zur Laufzeit importiert und nicht mitgeliefert.

Quellen, geprüft am 7. Oktober 2026:

- https://github.com/omacom/omarchy/blob/quattro/LICENSE
- https://github.com/omacom/omarchy/tree/quattro/shell/Ui
- https://github.com/omacom/omarchy/tree/quattro/shell/plugins/panels/network

Python 3, QtQuick und Quickshell bleiben externe Laufzeitabhängigkeiten.
Das Paket enthält keine kopierten Bibliotheken, Fonts, Icons oder Bilddateien.
Das Symbol ist ein Zeichen aus dem vom Omarchy-Theme bereitgestellten Font.
