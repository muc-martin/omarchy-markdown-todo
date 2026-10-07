# Markdown To-do für Omarchy

Ein kompaktes Bar-Panel mit P0, P1 und P2. Markdown bleibt die Datenquelle.
Erledigte Aufgaben bleiben in der Datei und verschwinden aus dem Panel.
Titel stehen in einer Zeile, die Beschreibung erscheint im Hover.

Beim Öffnen klappt das Panel so viele Gruppen auf, wie in ein Drittel der
Bildschirmhöhe passen (höchstens 460 Style-Einheiten). Es schließt zuerst P2,
dann P1; P0 bleibt offen und kann scrollen. P1/P2 lassen sich manuell umschalten.
Farben, Fonts, Abstände und Rundungen kommen vom Omarchy-Theme.
Rechtsklick öffnet die Markdown-Datei; Escape schließt das Panel.

## Voraussetzungen

Omarchy Quattro mit `qs.Ui.Panel`, `KeyboardPanel`, `PanelToolTip`,
`PanelSectionHeader`, `PanelSeparator` und `BarIconButton`; Python 3 auf PATH.
Entwickelt gegen lokal installiertes Omarchy `4.0.0.alpha`.
Es gibt keine Python-Pakete, Dienste, Netzwerkanfragen oder privilegierten Schritte.
Zum Bearbeiten braucht man einen Editor: standardmäßig `omawrite`, sonst
`xdg-open`; eigene Editorwahl siehe unten. Terminaleditoren brauchen einen
Terminalstarter im Editorbefehl. Der Helfer startet keine Shell.

## Installation

Repository: https://github.com/muc-martin/omarchy-markdown-todo

Der Code ist öffentlich; die Store-Einreichung und der isolierte UI-Test stehen
noch aus. Nach Prüfung des Codes installieren:

```sh
omarchy plugin add https://github.com/muc-martin/omarchy-markdown-todo.git --enable
```

Der offizielle Installer klont und prüft das Plugin. Er führt keine Installations-
Hooks aus. Das Panel ruft den mitgelieferten Helfer direkt mit Python auf;
es hängt nicht von einer separat installierten `omarchy-todo`-Version ab.
Quellen werden nach `~/.config/omarchy/plugins/martin.todo/` installiert.
Die Aufgaben liegen standardmäßig unter
`${XDG_DATA_HOME:-$HOME/.local/share}/omarchy/todo.md`.
`list` erzeugt keine Datendatei. Der erste Schreibvorgang legt sie mit Modus 0600 an.
Eine existierende Datei wird beim Initialisieren niemals durch ein Beispiel ersetzt.

Eine vorhandene Installation mit derselben ID führt zur Ablehnung. Vor einem
bewussten Wechsel lokale Änderungen vergleichen, Plugin und `shell.json` auf
dem nativen Linux-Dateisystem sichern, dann den alten Eintrag mit
`omarchy plugin remove martin.todo` entfernen. Keine produktive Installation
nur für einen Test ersetzen. Die Daten bleiben außerhalb des Plugins erhalten.

## Pfad und Editor

Inline-Einstellungen am Bar-Eintrag in `~/.config/omarchy/shell.json`:

```json
{"id": "martin.todo", "file": "/absolute/path/tasks.md", "editor": "omawrite"}
```

Leere Werte nutzen die Vorgaben. Im Panel hat `file` Vorrang vor
`OMARCHY_TODO_FILE`, danach folgt der XDG-Datenpfad.
Für die CLI gilt `--file` vor `OMARCHY_TODO_FILE` vor dem XDG-Datenpfad.
Verwende bei Widget-Einstellungen absolute Pfade; `~` wird vom Helfer expandiert.
Editor-Reihenfolge: Widget-`editor` bzw. CLI-`--editor`, `OMARCHY_TODO_EDITOR`,
`VISUAL`, `EDITOR`, `omawrite`, `xdg-open`.
Editorbefehle werden mit `shlex.split` in Argumente zerlegt. Es gibt keine
Variablenexpansion, Pipes oder Shell-Operatoren. Beispiele: `code --wait` oder
`alacritty -e nvim`. Dateinamen mit Leerzeichen werden als ein Argument angehängt.
Eine geänderte Sitzungsvariable erreicht eine bereits laufende Shell erst nach
Neustart; Inline-Einstellungen laden automatisch neu.

## CLI und Agenten

Optional den mitgelieferten Helfer direkt aufrufen:

```sh
TODO_PLUGIN="$HOME/.config/omarchy/plugins/martin.todo"
python3 "$TODO_PLUGIN/omarchy-todo" --file /absolute/path/tasks.md list
python3 "$TODO_PLUGIN/omarchy-todo" --file /absolute/path/tasks.md add P1 "Handbuch ergänzen" --description "Editorwahl mit einem Beispiel erklären."
python3 "$TODO_PLUGIN/omarchy-todo" --file /absolute/path/tasks.md toggle LINE ETAG --revision REVISION
```

`LINE`, `ETAG` und `REVISION` kommen aus dem aktuellen JSON von `list`.
Bei Konflikten erneut lesen und die gemeinte Aufgabe prüfen. Die alte
Zwei-Argument-Form von `toggle` bleibt kompatibel, prüft aber nur die Aufgabenzeile.
Agenten sollen immer `--revision` übergeben. Neue CLI-Titel haben höchstens
35 Zeichen; Beschreibungen sind Pflicht. Mehrzeilige Eingaben werden zu einer
Zeile zusammengezogen. Alte Aufgaben ohne Beschreibung bleiben lesbar.

Der optionale Skill liegt unter `skills/omarchy-todo/SKILL.md`. Vor dem Kopieren
nach `~/.codex/skills/omarchy-todo/SKILL.md` vorhandene Fassungen vergleichen und
sichern. Er ist keine Laufzeitabhängigkeit und wird nicht automatisch installiert.
Die CLI dieses Pakets kann separat nach `~/.local/bin/omarchy-todo` kopiert werden;
auch dabei bestehende Fassungen vorher vergleichen und sichern.

## Format und Schreibschutz

```markdown
## P1

- [ ] Handbuch ergänzen
  description: Editorwahl mit einem Beispiel erklären.
```

Der Helfer bewahrt fremde Markdown-Abschnitte und vorhandene Dateirechte.
Er serialisiert CLI-Schreibvorgänge über die dauerhafte Nachbardatei `.lock`,
schreibt eine temporäre Datei im selben Verzeichnis, synchronisiert sie und
ersetzt das Ziel atomar. Symbolische Links als Datendatei oder Lock werden
abgelehnt. Die `.lock`-Datei während laufender Aufrufe weder löschen noch ersetzen.
Vor dem Ersetzen wird die vorher gelesene Datei auf Änderungen geprüft.

Editoren und direkte Agent-Schreibvorgänge nehmen diese Sperre nicht automatisch.
Zwischen der letzten Prüfung und dem Ersetzen bleibt ein kurzes Zeitfenster.
Direkte Änderungen daher nicht gleichzeitig mit CLI-Mutationen ausführen.
Die Sperre schützt kooperierende Schreiber; sie ist keine Dateisystemsperre
für beliebige Anwendungen. Das Panel liest alle drei Sekunden neu, solange es
geöffnet ist. Eine veraltete Panelaktion wird anhand der Dateiversion abgelehnt.

## Update, Entfernung und Rollback

Git-verwaltete Installationen aktualisieren mit `omarchy plugin update martin.todo`.
Vorher Plugin-Checkout und `shell.json` in einem nativen Zustandsverzeichnis sichern
und lokale Änderungen prüfen. Der offizielle Updater zeigt den Diff und verweigert
Updates bei störenden lokalen Änderungen. Daten- und Editorwahl bleiben im
Bar-Eintrag; der Helfer ist Teil desselben Updates.

Entfernen: `omarchy plugin remove martin.todo`. Eine separat installierte CLI und
einen optionalen Skill nur gezielt entfernen oder aus der Sicherung wiederherstellen.
**Die Markdown-Datei und ihre Daten niemals beim Rollback löschen.**

Rollback: Plugin deaktivieren, aktuellen Checkout außerhalb des Plugin-Verzeichnisses
sichern, die vorher gesicherte Pluginfassung am alten Ort wiederherstellen und die
betroffenen Bar-Einträge aus der Sicherung abgleichen. `shell.json` nicht blind über
neuere Änderungen kopieren. Danach `omarchy-shell shell rescanPlugins` ausführen.
Die neue Fassung erst wieder aktivieren, wenn die gewünschte Version geprüft ist.

## Tests

```sh
python3 -m unittest -v test_omarchy_todo.py
omarchy plugin validate .
```

Tests nutzen ausschließlich temporäre, synthetische Aufgaben. `examples/demo.md`
enthält offene und erledigte Beispiele; `examples/empty.md` ist ein leeres Gerüst.
Die echte Aufgabenliste wird für Tests und Paketexport weder gelesen noch kopiert.
Weitere Prüfergebnisse und offene UI-Prüfungen stehen in `VERIFICATION.md`.

## Lizenz und Veröffentlichung

MIT, siehe `LICENSE` und `THIRD_PARTY_NOTICES.md`.
Das Repository wurde vom Eigentümer erstellt. Die Store-Einreichung braucht
eine separate Freigabe. Dieses Repository ist noch kein Marketplace-Eintrag.
`PUBLISHING.md` beschreibt den geprüften Weg und die verbleibenden Schritte.
