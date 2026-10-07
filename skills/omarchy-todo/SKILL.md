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
- Add: `python3 PLUGIN/omarchy-todo --file FILE add P1 "Short title" --description "Context and expected result"`.
- Titles have at most 35 characters. Put further detail in the required description.
- Complete or reopen: read the current row, then use `toggle LINE ETAG --revision REVISION`.
  On conflict, read again and check the intended task before retrying.

Keep P0/P1/P2 headings and unrelated Markdown. Descriptions occupy a single
`  description: ...` line directly below the task. Existing tasks without one
remain readable. Prefer CLI mutations: its persistent `.lock` file serializes
cooperating writers. Do not replace or remove the lock file. Direct editor or
agent writes do not take that lock; avoid concurrent writes and never promise
that atomic replacement alone prevents every race. The panel refreshes while
open. Setup, editor choice and rollback are in the plugin's README.
