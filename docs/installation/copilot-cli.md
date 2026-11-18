# forge-doctor-data + GitHub Copilot CLI

```bash
cd ~/meu-projeto
forge-doctor-data install
```

O que a instalação escreve de verdade:

- `.mcp.json` — entrada gerenciada `forge-doctor-data mcp`.
- `.forge/context/` — manifesto `forge/context/v1` + entrada no registry
  compartilhado; blocos `forge:*` em `AGENTS.md` quando já existe.
- Agent specs **bundled** no pacote, declarados no manifesto — não há
  espelho em `.github/` ou `.agents/` hoje.

Suporte estrutural — a execução real no Copilot é registrada como pendente
na matriz de aceitação até validação em ambiente real.
