# Troubleshooting — forge-doctor-data

| Sintoma | Ação |
|---|---|
| `command not found: forge-doctor-data` | rode `./setup.sh` de novo; abra terminal novo (launcher no PATH) |
| `FORGE-INSTALL-LOCKED` | outra instalação em curso; se foi interrompida, o lock expira/recupera sozinho |
| `FORGE-INSTALL-PLAN-NOT-APPROVED` | mutações exigem `--yes` (após o `--dry-run`) |
| `FORGE-INSTALL-NOT-A-REPO` | escopo project precisa de `.git` ou `--root` |
| `install doctor` FAIL em mcp-handshake | `forge-doctor-data install mcp-verify` mostra stderr_tail — a chave usa argv absoluto (shim ou `python -m`); falha real indica servidor quebrado, não PATH |
| arquivo seu sumiu? | não deveria — instalação nunca sobrescreve conteúdo do usuário; backups em `<state_dir>/backups/` |
| drift detectado | `forge-doctor-data install repair` restaura regiões gerenciadas mantendo o resto |
