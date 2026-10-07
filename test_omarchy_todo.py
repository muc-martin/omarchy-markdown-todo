"""Behavior of the plain-Markdown store used by the bar widget."""

import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import importlib.machinery
import importlib.util


SCRIPT = Path(__file__).with_name("omarchy-todo")
LOADER = importlib.machinery.SourceFileLoader("omarchy_todo", str(SCRIPT))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
TODO = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(TODO)


class TodoMarkdownTests(unittest.TestCase):
    def test_empty_file_has_three_priorities(self):
        with tempfile.TemporaryDirectory() as directory:
            rows = TODO.task_rows(TODO.read_lines(Path(directory) / "todo.md"))
            self.assertEqual(rows, {"P0": [], "P1": [], "P2": []})

    def test_add_and_toggle_keep_unrelated_markdown(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "todo.md"
            lines = ["# My list\n", "\n", "## P0\n", "\n", "Note stays.\n", "\n", "## P1\n", "\n", "## P2\n"]
            TODO.insert_task(lines, "P0", "Write tests")
            TODO.write_atomic(path, lines)
            row = TODO.task_rows(TODO.read_lines(path))["P0"][0]
            self.assertEqual(row["text"], "Write tests")
            self.assertIn("Note stays.", path.read_text())
            line = row["line"] - 1
            raw = lines[line]
            self.assertEqual(row["etag"], hashlib.sha256(raw.encode()).hexdigest()[:16])
            lines[line] = raw[:3] + "x" + raw[4:]
            TODO.write_atomic(path, lines)
            self.assertTrue(TODO.task_rows(TODO.read_lines(path))["P0"][0]["done"])
            self.assertIn("Note stays.", path.read_text())

    def test_missing_section_added_without_losing_content(self):
        lines = ["# Existing\n", "\n", "Other prose.\n"]
        TODO.insert_task(lines, "P2", "Later")
        self.assertEqual(TODO.task_rows(lines)["P2"][0]["text"], "Later")
        self.assertIn("Other prose.", "".join(lines))

    def test_unterminated_heading_still_separates_task(self):
        lines = ["## P0"]
        TODO.insert_task(lines, "P0", "One")
        self.assertEqual("".join(lines), "## P0\n- [ ] One\n")

    def test_unterminated_last_task_still_separates_new_task(self):
        lines = ["## P0\n", "- [ ] Existing"]
        TODO.insert_task(lines, "P0", "New")
        self.assertEqual("".join(lines), "## P0\n- [ ] Existing\n- [ ] New\n")

    def test_description_is_attached_to_task_and_survives_toggle(self):
        lines = ["## P0\n", "\n"]
        TODO.insert_task(lines, "P0", "Short title", "More context for the hover")
        row = TODO.task_rows(lines)["P0"][0]
        self.assertEqual(row["description"], "More context for the hover")
        self.assertEqual(lines[row["line"]], "  description: More context for the hover\n")
        index = row["line"] - 1
        lines[index] = lines[index][:3] + "x" + lines[index][4:]
        self.assertEqual(TODO.task_rows(lines)["P0"][0]["description"], row["description"])

    def test_only_immediate_description_line_is_task_metadata(self):
        lines = ["## P0\n", "- [ ] Plain\n", "\n", "  description: Unrelated prose\n"]
        self.assertEqual(TODO.task_rows(lines)["P0"][0]["description"], "")

    def test_cli_add_description_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "todo.md"
            subprocess.run(
                [str(SCRIPT), "--file", str(path), "add", "P1", "Short title", "--description", "Extra context"],
                check=True,
            )
            result = subprocess.run(
                [str(SCRIPT), "--file", str(path), "list"],
                check=True, capture_output=True, text=True,
            )
            self.assertEqual(json.loads(result.stdout)["P1"][0]["description"], "Extra context")


class TodoSafetyTests(unittest.TestCase):
    def cli(self, path, *args, input=None):
        return subprocess.run([str(SCRIPT), "--file", str(path), *args],
                              input=input, capture_output=True, text=True)

    def test_stdin_round_trip_normalizes_content_without_interpreting_it(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks with spaces.md"
            path.write_text("# Existing\n\nKeep this note.\n\n## P1\n")
            path.chmod(0o640)
            payload = {"text": "  - Review ä; $(id)\n", "description": "First\n## P0\n- [ ] Injected"}
            result = self.cli(path, "add", "P1", "--stdin", input=json.dumps(payload))
            self.assertEqual(result.returncode, 0, result.stderr)
            rows = json.loads(self.cli(path, "list").stdout)
            self.assertEqual(rows["P0"], [])
            self.assertEqual(len(rows["P1"]), 1)
            row = rows["P1"][0]
            self.assertEqual(row["text"], "- Review ä; $(id)")
            self.assertEqual(row["description"], "First ## P0 - [ ] Injected")
            self.assertIn("Keep this note.", path.read_text())
            self.assertEqual(path.stat().st_mode & 0o777, 0o640)
            result = self.cli(path, "toggle", str(row["line"]), row["etag"], "--revision", row["revision"])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(json.loads(self.cli(path, "list").stdout)["P1"][0]["done"])

    def test_stdin_rejects_invalid_payload_without_echoing_or_changing_data(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.md"
            path.write_text("Keep existing data\n")
            before = path.read_bytes()
            marker = "Synthetic private marker"
            invalid = ["", marker, "[]", "null",
                       json.dumps({"text": marker}),
                       json.dumps({"text": marker, "description": "Context", "extra": True}),
                       json.dumps({"text": [marker], "description": "Context"}),
                       json.dumps({"text": marker, "description": 42}),
                       '{"text":"' + marker + '","text":"Other","description":"Context"}',
                       '{"text":"' + marker + '","te\\u0078t":"Other","description":"Context"}',
                       json.dumps({"text": marker, "description": "Context"}) + " {}",
                       json.dumps({"text": "\ud800", "description": marker})]
            for payload in invalid:
                with self.subTest(payload=payload):
                    result = self.cli(path, "add", "P0", "--stdin", input=payload)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertNotIn(marker, result.stdout + result.stderr)
                    self.assertEqual(path.read_bytes(), before)

    def test_stdin_rejects_non_utf8_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.md"
            result = subprocess.run([str(SCRIPT), "--file", str(path), "add", "P0", "--stdin"],
                                    input=b'{"text":"\xff","description":"Context"}', capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(path.exists())
            self.assertNotIn(b"\xff", result.stderr)

    def test_stdin_keeps_required_description_and_title_limit(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.md"
            for payload in [{"text": " ", "description": "Context"},
                            {"text": "Task", "description": " \n"},
                            {"text": "a" * 36, "description": "Context"}]:
                result = self.cli(path, "add", "P0", "--stdin", input=json.dumps(payload))
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(path.exists())
            result = self.cli(path, "add", "P0", "--stdin",
                              input=json.dumps({"text": "a" * 35, "description": "Context"}))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_stdin_cannot_mix_with_content_arguments(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.md"
            for args in [("Task", "--stdin"), ("--stdin", "--description", "Context"),
                         ("Task", "--description", "Context", "--stdin")]:
                result = self.cli(path, "add", "P0", *args, input="")
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(path.exists())

    @unittest.skipUnless(Path("/proc/self/cmdline").exists(), "Linux process arguments required")
    def test_stdin_task_content_is_absent_from_running_process_arguments(self):
        import fcntl
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.md"
            payload = {"text": "Synthetic private title", "description": "Synthetic private description"}
            with path.with_name(path.name + ".lock").open("w") as lock:
                fcntl.flock(lock, fcntl.LOCK_EX)
                child = subprocess.Popen([str(SCRIPT), "--file", str(path), "add", "P2", "--stdin"],
                                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE, text=True)
                try:
                    child.stdin.write(json.dumps(payload))
                    child.stdin.close()
                    child.stdin = None
                    arguments = Path(f"/proc/{child.pid}/cmdline").read_bytes()
                    self.assertIn(b"--stdin", arguments)
                    for value in payload.values():
                        self.assertNotIn(value.encode(), arguments)
                finally:
                    fcntl.flock(lock, fcntl.LOCK_UN)
                    stdout, stderr = child.communicate(timeout=10)
                self.assertEqual(child.returncode, 0, stderr)
                self.assertEqual(stdout + stderr, "")
                row = json.loads(self.cli(path, "list").stdout)["P2"][0]
                self.assertEqual(row["text"], payload["text"])
                self.assertEqual(row["description"], payload["description"])

    def test_description_and_short_title_required(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.md"
            for args in [("add", "P0", "Task"),
                         ("add", "P0", "Task", "--description", "  "),
                         ("add", "P0", "a" * 36, "--description", "Context")]:
                self.assertNotEqual(self.cli(path, *args).returncode, 0)
                self.assertFalse(path.exists())

    def test_revision_rejects_changed_description_and_duplicate_task(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.md"
            self.assertEqual(self.cli(path, "add", "P1", "Task", "--description", "First").returncode, 0)
            row = json.loads(self.cli(path, "list").stdout)["P1"][0]
            path.write_text(path.read_text().replace("First", "Changed"))
            before = path.read_bytes()
            result = self.cli(path, "toggle", str(row["line"]), row["etag"], "--revision", row["revision"])
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(before, path.read_bytes())

    def test_crlf_revision_and_toggle(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.md"
            path.write_bytes(b"## P0\r\n- [ ] Task\r\n  description: Detail\r\n")
            row = json.loads(self.cli(path, "list").stdout)["P0"][0]
            self.assertEqual(self.cli(path, "toggle", str(row["line"]), row["etag"], "--revision", row["revision"]).returncode, 0)
            self.assertIn(b"- [x] Task\r\n", path.read_bytes())

    def test_symlink_file_and_lock_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "target"
            target.write_text("Keep me")
            path = Path(directory) / "tasks.md"
            path.symlink_to(target)
            self.assertNotEqual(self.cli(path, "add", "P0", "Task", "--description", "Detail").returncode, 0)
            path.unlink()
            path.with_name(path.name + ".lock").unlink()
            path.with_name(path.name + ".lock").symlink_to(target)
            self.assertNotEqual(self.cli(path, "init").returncode, 0)
            self.assertEqual(target.read_text(), "Keep me")

    def test_permissions_preserved_and_init_keeps_existing_data(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.md"
            self.assertEqual(self.cli(path, "init").returncode, 0)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            path.chmod(0o640)
            before = path.read_bytes()
            self.assertEqual(self.cli(path, "init").returncode, 0)
            self.assertEqual(before, path.read_bytes())
            self.assertEqual(self.cli(path, "add", "P2", "Task", "--description", "Context").returncode, 0)
            self.assertEqual(path.stat().st_mode & 0o777, 0o640)

    def test_external_edit_before_replace_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.md"
            path.write_text("Original")
            before = path.read_bytes()
            path.write_text("External edit")
            with self.assertRaises(ValueError):
                TODO.write_atomic(path, ["CLI change"], before, check_snapshot=True)
            self.assertEqual(path.read_text(), "External edit")
            self.assertEqual(list(path.parent.glob(".todo-*")), [])

    def test_parallel_adds_keep_all_tasks(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.md"
            children = [subprocess.Popen([str(SCRIPT), "--file", str(path), "add", "P2",
                                         f"Task {i}", "--description", "Synthetic context"])
                        for i in range(12)]
            self.assertEqual([child.wait() for child in children], [0] * 12)
            self.assertEqual(len(json.loads(self.cli(path, "list").stdout)["P2"]), 12)

    def test_environment_data_path_and_explicit_override(self):
        import os
        with tempfile.TemporaryDirectory() as directory:
            env = dict(os.environ, XDG_DATA_HOME=directory)
            env.pop("OMARCHY_TODO_FILE", None)
            result = subprocess.run([str(SCRIPT), "init"], env=env, capture_output=True)
            self.assertEqual(result.returncode, 0)
            default = Path(directory) / "omarchy/todo.md"
            self.assertTrue(default.exists())
            custom = Path(directory) / "custom.md"
            env["OMARCHY_TODO_FILE"] = str(custom)
            self.assertEqual(subprocess.run([str(SCRIPT), "init"], env=env, capture_output=True).returncode, 0)
            explicit = Path(directory) / "explicit.md"
            self.assertEqual(subprocess.run([str(SCRIPT), "--file", str(explicit), "init"], env=env, capture_output=True).returncode, 0)
            self.assertTrue(custom.exists())
            self.assertTrue(explicit.exists())

    def test_editor_failure_keeps_existing_data(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks.md"
            path.write_text("Keep this document")
            self.assertNotEqual(self.cli(path, "edit", "--editor", "/missing/editor").returncode, 0)
            self.assertEqual(path.read_text(), "Keep this document")

    def test_editor_arguments_without_shell(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tasks with spaces.md"
            log = Path(directory) / "arguments.json"
            editor = Path(directory) / "editor.py"
            editor.write_text("import json, sys; open(sys.argv[1], 'w').write(json.dumps(sys.argv[2:]))")
            import shlex
            command = shlex.join(["python3", str(editor), str(log), "literal;$(ignored)"])
            self.assertEqual(self.cli(path, "edit", "--editor", command).returncode, 0)
            self.assertEqual(json.loads(log.read_text()), ["literal;$(ignored)", str(path)])


if __name__ == "__main__":
    unittest.main()
