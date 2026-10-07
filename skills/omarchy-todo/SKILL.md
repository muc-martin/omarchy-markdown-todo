---
name: omarchy-todo
description: Manage an Omarchy Markdown To-do list when the user asks to list, add, or complete P0/P1/P2 tasks.
---

# Omarchy To-do

Use only when the user asks to manage tasks. Never publish or commit live data.
Find the plugin checkout under `~/.config/omarchy/plugins/todo.md` and invoke
its bundled helper with Python 3. Do not assume that `omarchy-todo` on PATH is
this version. Confirm the intended data path from the widget's `file` setting,
`OMARCHY_TODO_FILE`, or the default `${XDG_DATA_HOME:-~/.local/share}/omarchy/todo.md`.
Pass the same absolute path with `--file` to every CLI call.

- Read: `python3 PLUGIN/omarchy-todo --file FILE list`.
- Add: start `python3 PLUGIN/omarchy-todo --file FILE add P1 --stdin` and send
  one JSON object through the execution tool's stdin channel:
  `{"text":"Short title","description":"Context and expected result"}`.
- Titles have at most 35 characters. Put further detail in the required description.
- Complete or reopen: read the current row, then use `toggle LINE ETAG --revision REVISION`.
  On conflict, read again and check the intended task before retrying.

Pass task content only through stdin. Never put it in argv, environment variables,
or an execution command string, including here-documents in `bash -c`, `printf`
arguments and `python -c` snippets. These expose content through process listings.
If the tool has no stdin channel, use a file-writing API to create a temporary
JSON file with mode 0600 in a private temporary directory. Redirect stdin using
only that file's path in the command and remove it after the helper finishes.
The JSON fields `text` and `description` must both be strings; additional or
duplicate fields are rejected. Do not use the legacy content arguments.

Keep P0/P1/P2 headings and unrelated Markdown. Descriptions occupy a single
`  description: ...` line directly below the task. Existing tasks without one
remain readable. Prefer CLI mutations: its persistent `.lock` file serializes
cooperating writers. Do not replace or remove the lock file. Direct editor or
agent writes do not take that lock; avoid concurrent writes and never promise
that atomic replacement alone prevents every race. The panel refreshes while
open. Setup, editor choice and rollback are in the plugin's README.
