# forge-doctor-data + Devin CLI

```bash
cd ~/meu-projeto
forge-doctor-data install
```

O que a instalação escreve de verdade:

- `.mcp.json` — entrada gerenciada `forge-doctor-data mcp`, consumida pelo host.
- `.forge/context/` — manifesto `forge/context/v1` + entrada no registry
  compartilhado.
- `AGENTS.md`/`AGENT_PROTOCOL.md` — blocos gerenciados `forge:*` quando já
  existem; nada é criado nem sobrescrito fora dos blocos.
- Agent specs **bundled** no pacote, declarados no manifesto de
  capacidades — não há espelho em `.devin/skills/` ou `.agents/` hoje.

MCP: a entrada `forge-doctor-data mcp` em `.mcp.json` é consumida pelo host.
