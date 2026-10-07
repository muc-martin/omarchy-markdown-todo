# Publication preparation

Status: October 7, 2026. Initial submission:
[#10403](https://github.com/omacom/omarchy-plugin-marketplace/issues/10403).
The first commit passed automated checks. A maintainer requested stdin input
for task content; version 1.1.3 adds it and updates CLI and agent instructions.

Official references:

- [Omarchy manual](https://omarchy.org/manual/shell-plugins/)
- [Publishing guide](https://plugins.omarchy.org/publish.html)
- [Submission guide](https://github.com/omacom/omarchy-plugin-marketplace/blob/main/SUBMISSION.md)
- [Submission form](https://github.com/omacom/omarchy-plugin-marketplace/issues/new?template=submit-plugin.yml)

The repository contains one plugin, with its manifest, README and license at
the root. Its new Git history contains only the reviewed package files.
Personal setup history and live tasks were not imported. There are no install
hooks.

Listing metadata: name `todo.md`, plugin ID `todo.md`, category
`Productivity`, tags `bar, quickshell`. ID availability must be checked before
submission. Retired IDs can remain unavailable; the Marketplace makes the final
decision. Changes to the ID require corresponding updates to the manifest,
widget, IPC targets and documentation.

Remaining steps:

1. Review the isolated rendering results and remaining interaction checks in
   `VERIFICATION.md`.
2. Check source, license rights, dependencies and all five submission statements.
3. Upload the reviewed correction, then update the existing submission with the
   exact new commit to rerun validation. Keep the original category and tags.
4. Wait for maintainer review of the current reports and corrected input path.

The current Marketplace process checks an exact commit and requires maintainer
approval (`approved-and-verified`). Local tests do not replace that review.
Later listing updates use the official verification form and the full target
commit SHA. An optional `preview.png` must show only synthetic tasks. The root preview and screenshots use only synthetic tasks.
