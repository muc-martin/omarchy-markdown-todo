# Prüfung

7. Oktober 2026, Linux, Bash, Omarchy `4.0.0.alpha`.

## Ausgangsstand

Vor der Bearbeitung stimmen Repo-Mirror und installierter `martin.todo`-Ordner
byteweise überein. Auch die CLI und der persönliche Agent-Skill stimmen überein.
Keine bestehenden Git-Änderungen. Die produktive Installation wurde nicht ersetzt.
Die echte Markdown-Datei wurde weder geöffnet noch kopiert oder verändert.

## Automatisch geprüft

- 18 Tests: Markdown-Erhalt, fehlende Abschnitte, Beschreibungen, Zeilenenden,
  Pflichtbeschreibung, kurze Titel, veraltete Revision, CRLF-Toggle,
  abgelehnte Symlinks, Dateirechte, konfliktbedingter Schreibabbruch,
  zwölf parallele Ergänzungen und Editorargumente ohne Shell-Ausführung, XDG-/Umgebungspfade und Editorfehler.
- `omarchy plugin validate` akzeptiert das Paket.
- QML-Syntaxprüfung mit Qt 6 `qmlformat` und Typprüfung mit `qmllint`.
  Für `qs.*` braucht der normale Qt-Linter einen temporären Importalias auf die
  installierte Shell. Es verbleiben Warnungen für dynamische Bar-Eigenschaften
  und Theme-Eigenschaften (`QObject`) und den Quickshell-Signaltyp `QProcess::ExitStatus`.
  Exit-Code 0 allein bedeutet hier keine vollständige UI-Verifikation.
- Paketexport aus einer festen Dateiliste; kein Live-Datenpfad als Eingabe.
  Exportiertes Archiv isoliert entpackt: alle 18 Tests und Manifestprüfung bestehen.

## Noch ausstehende UI-Prüfung

Das neue Paket wurde nicht in die produktive Shell geladen. Keine Bestätigung
für das vollständige neue Widget zur Laufzeit und kein Store-Prüfergebnis.
Vor Einreichung in einer separaten Omarchy-Testsession prüfen:

1. `examples/demo.md` in ein neues temporäres Verzeichnis kopieren. Den Widget-
   Eintrag mit diesem absoluten Dateipfad konfigurieren; keinen Live-Pfad verwenden.
2. Öffnen, Escape, Panelwechsel, IPC öffnen/schließen, deaktivieren/aktivieren,
   Shell-Neustart und Entfernung prüfen.
3. Kurze Liste: alle Gruppen offen. Lange synthetische Liste: zuerst P2, dann P1
   geschlossen; P0 bleibt offen und scrollt. Manuelle P1/P2-Auswahl bleibt bei Refresh.
4. Titel einzeilig, Beschreibung im Hover, erledigte Aufgabe ausgeblendet.
5. Editor per Rechtsklick öffnet genau die synthetische Datei. Datei- und Editorwahl
   mit Leerzeichen prüfen, Editorfehler kontrollieren.
6. CLI-Ergänzung bei offenem Panel sichtbar; externe Änderung vor Klick führt zu
   Konflikt statt stiller Änderung. Danach erneut lesen und gezielt klicken.
7. Helles und dunkles Theme, linke/rechte/obere/untere Bar und begrenzte Bildschirmhöhe.
8. Bei Bedarf nur das synthetische Panel als Preview aufnehmen.

## Grenzen

Atomare Ersetzung verhindert halbe Dateien. Die CLI-Sperre schützt nur
kooperierende CLI-Schreiber. Ein Editor kann im letzten kurzen Zeitfenster
zwischen Inhaltsprüfung und Ersetzung schreiben; direkte Änderungen koordinieren.
Legacy-Toggle ohne `--revision` prüft nur die Zeile. Die UI und der neue Skill
übergeben die gesamte Revision. Laufzeitabhängigkeiten werden nicht mitgeliefert.
