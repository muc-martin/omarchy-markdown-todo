# Verification

October 7, 2026. Linux, Bash, Omarchy `4.0.0.alpha`.

## Baseline

Before preparation, the repository mirror matched the installed plugin, CLI
and personal agent skill byte for byte. The working tree had no existing changes.
The production installation was not replaced. Live Markdown task data was not
opened, copied or modified.

## Automated checks

- 24 tests cover Markdown preservation, missing sections, descriptions, line
  endings, required descriptions, short titles, stale revisions, CRLF toggles,
  rejected symlinks, file permissions, conflicting writes, twelve concurrent
  additions, editor arguments without shell execution, XDG/environment paths
  and editor failures. Stdin tests cover UTF-8 JSON, strict field types and keys,
  duplicate keys, mixed input modes, malformed input without content in error
  output, unchanged data on rejection, title limits and Markdown preservation.
- The original argument-based add was reproduced with synthetic content visible
  in `/proc/<pid>/cmdline`, even with a 0600 task file. The stdin regression test
  supplies synthetic content to a running helper, checks that both fields are
  absent from its actual process arguments, then verifies the saved task.
- `omarchy plugin validate` accepts the package.
- Qt 6 `qmlformat` parses the QML. `qmllint` uses a temporary import alias for
  the installed shell's `qs.*` modules. Warnings remain for dynamic bar and theme
  properties typed as `QObject` and the Quickshell signal type
  `QProcess::ExitStatus`. Exit code 0 alone is not complete UI verification.
- Export uses a fixed file list without reading live task data. Tests and
  manifest validation also pass after isolated archive extraction.
- The published package was cloned, compared byte for byte and tested separately.
- An isolated Quickshell host rendered the current widget using synthetic data.
  Short lists expanded P0/P1/P2; a long list collapsed P2/P1 and kept P0 open.
  Completed tasks were hidden. Light, dark and collapsed screenshots capture only
  the panel via Qt, without desktop content.
- All five public commits and their 32 distinct text blobs were reviewed for
  private paths, task data, credential patterns and email addresses. No such data
  was found. Commit email addresses are GitHub noreply addresses. Historical
  versions retain the earlier first-name label; current package files do not.

## Pending UI checks

The new package has not been loaded into the production shell. Isolated rendering is verified; the interaction checks below and Marketplace
validation are separate checks. Before submission, use
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

Legacy add arguments remain for compatibility and expose their content through
process listings. README and bundled agent instructions use stdin; automation
instructions also keep task content out of shell and Python runner arguments.
