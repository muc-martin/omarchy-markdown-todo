# Publication preparation

Status: October 7, 2026. The public repository contains the plugin package.
No Marketplace submission has been made.

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
3. Fill the repository URL in the submission draft using this repository's URL.
4. Show the completed title and body to the owner and obtain separate approval.
5. Use the official form after approval. Correct feedback in the existing request.

The current Marketplace process checks an exact commit and requires maintainer
approval (`approved-and-verified`). Local tests do not replace that review.
Later listing updates use the official verification form and the full target
commit SHA. An optional `preview.png` must show only synthetic tasks. The root preview and screenshots use only synthetic tasks.
