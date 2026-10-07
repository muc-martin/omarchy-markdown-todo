# Verification

October 7, 2026. Linux, Bash, Omarchy `4.0.0.alpha`.

## Baseline

Before preparation, the repository mirror matched the installed plugin, CLI
and personal agent skill byte for byte. The working tree had no existing changes.
The production installation was not replaced. Live Markdown task data was not
opened, copied or modified.

## Automated checks

- 18 tests cover Markdown preservation, missing sections, descriptions, line
  endings, required descriptions, short titles, stale revisions, CRLF toggles,
  rejected symlinks, file permissions, conflicting writes, twelve concurrent
  additions, editor arguments without shell execution, XDG/environment paths
  and editor failures.
- `omarchy plugin validate` accepts the package.
- Qt 6 `qmlformat` parses the QML. `qmllint` uses a temporary import alias for
  the installed shell's `qs.*` modules. Warnings remain for dynamic bar and theme
  properties typed as `QObject` and the Quickshell signal type
  `QProcess::ExitStatus`. Exit code 0 alone is not complete UI verification.
- Export uses a fixed file list without reading live task data. Tests and
  manifest validation also pass after isolated archive extraction.
- The published package was cloned, compared byte for byte and tested separately.

## Pending UI checks

The new package has not been loaded into the production shell. Its full runtime
behavior and Marketplace validation remain unverified. Before submission, use
a separate Omarchy test session:

1. Copy `examples/demo.md` to a new temporary directory. Configure the widget
   with that absolute file path. Do not use a live data path.
2. Test opening, Escape, panel switching, IPC open/close, disable/enable,
   shell restart and removal.
3. For a short list, all groups should expand. For a long synthetic list, P2
   collapses first, then P1. P0 stays open and scrolls. Manual P1/P2 choices
   should survive refreshes.
4. Check single-line titles, descriptions on hover and hidden completed tasks.
5. Right-click should open exactly the synthetic file. Test file paths and
   editor arguments containing spaces, plus editor failures.
6. Add a task through the CLI while the panel is open. Change the file before
   a panel click and confirm that it reports a conflict. Read again before retrying.
7. Test light/dark themes, all four bar positions and limited screen height.
8. If needed, capture only the synthetic panel for a preview.

## Limits

Atomic replacement prevents partial files. The CLI lock protects cooperating
CLI writers only. An editor can write between the final contents check and
replacement; coordinate direct edits. Legacy toggles without `--revision` check
only the task line. The UI and optional skill pass the whole-file revision.
Runtime dependencies are not bundled.
