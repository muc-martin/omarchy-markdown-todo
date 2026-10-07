# Markdown To-do for Omarchy

A compact bar panel with P0, P1 and P2 priorities. Markdown is the data source.
Completed tasks stay in the file and disappear from the panel. Titles occupy
one line; descriptions appear on hover.

When opened, the panel expands as many groups as fit within one third of the
screen height, up to 460 style units. It collapses P2 first, then P1. P0 stays
open and scrolls when needed. P1 and P2 can be toggled manually. Colors, fonts,
spacing and corners follow the Omarchy theme. Right-click opens the Markdown
file in an editor. Escape closes the panel.

## Requirements

Omarchy Quattro with `qs.Ui.Panel`, `KeyboardPanel`, `PanelToolTip`,
`PanelSectionHeader`, `PanelSeparator` and `BarIconButton`; Python 3 on PATH.
Developed against Omarchy `4.0.0.alpha`. No Python packages, services, network
requests or privileged setup steps are required.

Editing requires an editor. The default is `omawrite`, with `xdg-open` as a
fallback. Terminal editors need a terminal launcher in the editor command.
The helper does not execute commands through a shell.

## Installation

The code is public. Marketplace submission and isolated UI verification are
still pending. Review the source before installation.

To install from this repository's URL, copy its HTTPS clone URL from GitHub's
**Code** menu and pass it to `omarchy plugin add`. If you already cloned this
repository, run this command from its root:

```sh
omarchy plugin add "$(git remote get-url origin)" --enable
```

The official installer clones and validates the plugin without running install
hooks. The panel calls its bundled helper through Python, so it does not depend
on another `omarchy-todo` installation. Sources are installed under
`~/.config/omarchy/plugins/markdown.todo/`.

Tasks default to `${XDG_DATA_HOME:-$HOME/.local/share}/omarchy/todo.md`.
`list` does not create a data file. The first write creates it with mode 0600.
Initialization preserves an existing file and never replaces it with an example.

Installation is refused if the plugin ID is already in use. Before replacing an
existing installation, compare local changes and back up its checkout and
`shell.json` on the native Linux filesystem. Remove the old plugin with
`omarchy plugin remove markdown.todo` only when you intend to replace it.
Keep task data outside the plugin checkout.

Version 1.1.1 changes the distribution ID to `markdown.todo`. If you installed
an earlier candidate, use `omarchy plugin list` to identify and disable the
previous entry before enabling this plugin. Both versions use the same default
data path; no task migration is needed. Do not enable both against the same file.

## File path and editor

Set options directly on the bar entry in `~/.config/omarchy/shell.json`:

```json
{"id": "markdown.todo", "file": "/absolute/path/tasks.md", "editor": "omawrite"}
```

Empty values use defaults. The panel's `file` setting overrides
`OMARCHY_TODO_FILE`, which overrides the XDG data path. For the CLI, `--file`
overrides `OMARCHY_TODO_FILE`, then the XDG default. Use absolute paths in widget
settings; the helper expands `~`.

Editor precedence: widget `editor` or CLI `--editor`, `OMARCHY_TODO_EDITOR`,
`VISUAL`, `EDITOR`, `omawrite`, then `xdg-open`. Commands are split into arguments
with `shlex.split`. Variables, pipes and shell operators are not expanded.
Examples: `code --wait` or `alacritty -e nvim`. A filename with spaces is passed
as one argument. Environment changes require a shell restart; inline widget
settings reload automatically.

## CLI and agents

Call the bundled helper directly:

```sh
TODO_PLUGIN="$HOME/.config/omarchy/plugins/markdown.todo"
python3 "$TODO_PLUGIN/omarchy-todo" --file /absolute/path/tasks.md list
python3 "$TODO_PLUGIN/omarchy-todo" --file /absolute/path/tasks.md add P1 "Update the guide" --description "Explain editor selection with an example."
python3 "$TODO_PLUGIN/omarchy-todo" --file /absolute/path/tasks.md toggle LINE ETAG --revision REVISION
```

Read `LINE`, `ETAG` and `REVISION` from the current JSON returned by `list`.
After a conflict, read again and check the intended task before retrying.
The legacy two-argument `toggle` form remains supported, but checks only the task
line. Agents should always pass `--revision`.

New CLI titles have at most 35 characters and require a description. Multiline
inputs are normalized to one line. Existing tasks without descriptions remain
readable.

The optional agent skill is in `skills/omarchy-todo/SKILL.md`. Compare and back up
any existing version before copying it to `~/.codex/skills/omarchy-todo/SKILL.md`.
It is not a runtime dependency and is not installed automatically. The helper
can also be copied to `~/.local/bin/omarchy-todo`; compare and back up an existing
CLI before replacing it.

## Markdown format and writes

```markdown
## P1

- [ ] Update the guide
  description: Explain editor selection with an example.
```

The helper preserves unrelated Markdown and existing file permissions. It
serializes CLI writes through a persistent adjacent `.lock` file, writes and
syncs a temporary file in the same directory, then atomically replaces the
target. Symlinks used as the task file or lock are rejected. Do not delete or
replace the lock file while CLI calls are running. Before replacing the target,
the helper checks whether its original contents changed.

Editors and direct agent writes do not automatically take this lock. There is a
small race window between the final contents check and replacement. Coordinate
direct edits with CLI mutations. The lock protects cooperating writers, not
arbitrary applications. While open, the panel refreshes every three seconds.
Stale panel actions are rejected using the file revision.

## Updates, removal and rollback

Update a Git-managed installation with `omarchy plugin update markdown.todo`.
First back up the plugin checkout and `shell.json` on the native filesystem and
inspect local changes. The official updater shows a diff and refuses updates
when local modifications prevent them. File and editor settings remain on the
bar entry; the bundled helper updates with the plugin.

Remove the plugin with `omarchy plugin remove markdown.todo`. Remove an optional
standalone CLI or agent skill separately, or restore their previous versions.
**Never delete the Markdown file or its tasks during rollback.**

For rollback, disable the plugin and back up the current checkout outside the
plugin directory. Restore the previous checkout at its original location and
compare the affected bar entries with the saved configuration. Preserve newer
changes in `shell.json`. Run `omarchy-shell shell rescanPlugins`, then enable the
plugin after checking the restored version.

## Tests

```sh
python3 -m unittest -v test_omarchy_todo.py
omarchy plugin validate .
```

Tests use temporary synthetic tasks. `examples/demo.md` contains open and
completed examples; `examples/empty.md` is an empty template. Live task data is
never read or copied for tests or package export. See `VERIFICATION.md` for
results and the remaining UI checks.

## License and publication

MIT; see `LICENSE` and `THIRD_PARTY_NOTICES.md`. Marketplace submission needs
separate owner approval. This repository is not yet a Marketplace listing.
`PUBLISHING.md` records the submission process and remaining steps.
