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
| `github` | `work start <pull request URL>` and `work start <issue URL>` starters; linkers for the pull request and issue of a Work |
| `wsp` | repository locator backed by `wsp find` (requires the `wsp` CLI) |

Both need `python3`; `github` uses the `gh` CLI when available (needed for
private repositories) and falls back to the public REST API for the starters.

Each plugin is a self-contained directory under `plugins/`, listed in
`marketplace.json`.
