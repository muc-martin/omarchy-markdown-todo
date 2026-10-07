# Veröffentlichung vorbereiten

Stand: 7. Oktober 2026. Öffentliches Repository:
https://github.com/muc-martin/omarchy-markdown-todo
Noch keine Store-Einreichung.

Die offiziellen Seiten verweisen auf Git-Verteilung und den Marketplace:

- [Omarchy-Handbuch](https://omarchy.org/manual/shell-plugins/)
- [Publishing Guide](https://plugins.omarchy.org/publish.html)
- [Submission Guide](https://github.com/omacom/omarchy-plugin-marketplace/blob/main/SUBMISSION.md)
- [Einreichungsformular](https://github.com/omacom/omarchy-plugin-marketplace/issues/new?template=submit-plugin.yml)

Das Repository enthält genau dieses Plugin mit Manifest, README und
Lizenz in der Wurzel. Nicht das persönliche Setup-Repository veröffentlichen
und nicht dessen Git-Historie übernehmen. Der Export enthält nur explizit
freigegebene Paketdateien. Es gibt keine Installations-Hooks.

Metadaten: Name `To-do`, aktuelle ID `martin.todo`, Kategorie
`Productivity`, Tags `bar, quickshell`. Die ID ist im am 7. Oktober geladenen
aktuellen Registry-JSON nicht enthalten. Auch zurückgezogene IDs können gesperrt
sein; eine endgültige Reservierung bzw. Verfügbarkeit bestätigt erst der Store.
Vor Veröffentlichung den Namensraum mit dem künftigen GitHub-Eigentümer prüfen.
Eine Änderung der ID erfordert Änderungen in Manifest, Widget, IPC und Anleitung.

Reihenfolge:

1. Isolierte UI-Prüfungen aus `VERIFICATION.md` abschließen.
2. Erledigt: Eigentümer hat `muc-martin/omarchy-markdown-todo` öffentlich erstellt.
3. Erledigt: Paketinhalt mit neuer Git-Historie übernommen; keine Setup-Historie.
4. Erledigt: tatsächliche URL in README und Einreichungsentwurf ergänzt.
5. Code, Lizenzrechte, Abhängigkeiten und die fünf Aussagen der Checkliste prüfen.
6. Eigentümer sieht den fertigen Titel und Text und gibt die Einreichung separat frei.
7. Danach das offizielle Formular verwenden. Fehler im bestehenden Antrag korrigieren.

Der aktuelle Store-Prozess prüft einen konkreten Commit und verlangt eine
Maintainer-Freigabe (`approved-and-verified`). Lokale Tests ersetzen diese Prüfung
nicht. Für spätere Katalogupdates gilt das offizielle Verifizierungsformular mit
der vollständigen Ziel-SHA. Ein optionales `preview.png` ist erlaubt; ein Screenshot
muss ausschließlich synthetische Aufgaben zeigen. Diesem Paket liegt bewusst
noch kein ungetesteter oder produktiver Screenshot bei.
