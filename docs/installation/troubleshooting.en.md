# Troubleshooting — Forge Doctor Data (EN)

| Symptom | Action |
|---|---|
| `command not found: forge-doctor-data` | run `./setup.sh` again; open a **new** terminal (launcher lands on PATH) |
| `FORGE-INSTALL-LOCKED` | another install is running or was interrupted; the lock expires and is recovered automatically — retry |
| `FORGE-INSTALL-PLAN-NOT-APPROVED` | mutations require `--yes` after reviewing `--dry-run` |
| `FORGE-INSTALL-NOT-A-REPO` | project scope needs a `.git` root or `--root` |
| `FORGE-INSTALL-DRIFT` | managed files changed on disk — run `install repair` to heal managed regions, keep your edits |
| MCP `FAIL` + `stderr_tail` | `install mcp-verify` shows the handshake evidence — usually the CLI not on PATH (the server is stdlib-only, no extra to install) |
| stale/partial install | `install uninstall` removes only ledger-owned files; `install status`/`install doctor` show the truth |

Português: [troubleshooting.md](troubleshooting.md).
