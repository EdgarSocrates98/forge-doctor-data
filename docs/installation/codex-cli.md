# forge-doctor-data + Codex CLI

```bash
cd ~/meu-projeto
forge-doctor-data install
```

O que a instalação escreve de verdade:

- `.mcp.json` — entrada gerenciada `forge-doctor-data mcp`.
- `.forge/context/` — manifesto `forge/context/v1` + entrada no registry
  compartilhado; blocos `forge:*` em `AGENTS.md` quando já existe.
- Agent specs **bundled** no pacote, declarados no manifesto — não há
  espelho em `.codex/` ou `.agents/` hoje.

MCP: o `codex` não lê `.mcp.json` de projeto (observado em codex-cli
0.160.0) — a entrada gerenciada é registrada mesmo assim, mas para o
servidor entrar no Codex use `codex mcp add` ou declare o servidor em
`~/.codex/config.toml`; o instalador não escreve esse arquivo hoje.
