# Work plugin marketplace

A [Work](https://github.com/gustaborges/work) marketplace. Register it, then
install the plugins you want:

```sh
work plugin marketplace add https://github.com/gustaborges/work-cli-marketplace.git
work plugin add github@work
work plugin add wsp@work
```

Registering only records where the catalog lives. `work plugin marketplace
upgrade work` refreshes what is offered; `work plugin update --check` and
`work plugin update github@work` apply a newer version to what you installed.

## Plugins

| Plugin | Components |
| --- | --- |
| `github` | `work start <pull request URL>` / `<issue URL>` starters; pull request and issue linkers; importers for the pull request description, comments and diff and for the issue (only when the Work has the matching link) |
| `wsp` | repository locator backed by `wsp find` (requires the `wsp` CLI) |

Both need `python3`; `github` uses the `gh` CLI when available (needed for
private repositories) and falls back to the public REST API for the starters.

Each plugin is a self-contained directory under `plugins/`, listed in
`marketplace.json`.

## What the github importers write

Importers add files beside the worktree, never inside it, and never overwrite:

| Importer | File |
| --- | --- |
| pull request description | `context/github/pull-request/description.md` |
| pull request comments | `context/github/pull-request/comments.md` |
| pull request diff | `context/github/pull-request/changes.diff` |
| issue | `context/github/issue/issue.md` |

They run automatically after `work start` when the Work carries a
`github.pull_request` / `github.issue` link, and on demand with `work import`.
Importing again is refused while the file exists; remove it first.
