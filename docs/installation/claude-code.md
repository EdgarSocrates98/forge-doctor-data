# forge-doctor-data + Claude Code

```bash
cd ~/meu-projeto
forge-doctor-data install
```

O que a instalação escreve de verdade:

- `.mcp.json` — entrada gerenciada `forge-doctor-data mcp` (chave
  `_forge_managed.forge-doctor-data`), que o `claude` lê da raiz.
- `.forge/context/` — manifesto `forge/context/v1` + entrada no registry
  compartilhado (`capabilities/forge-doctor-data.json`, `ROUTING.md`).
- `CLAUDE.md`/`AGENTS.md`/`AGENT_PROTOCOL.md` — blocos gerenciados
  `<!-- forge:forge-doctor-data:... -->` quando esses arquivos já existem;
  conteúdo fora dos blocos nunca é tocado.
- Os agent specs do forge ficam **bundled** no pacote
  (`forge_doctor_data/installation/assets/agents`) e são declarados no
  manifesto — a instalação não espelha arquivos em `.claude/skills/` ou
  `.claude/agents/` hoje.

MCP: `claude` lê `.mcp.json` da raiz — a entrada `forge-doctor-data mcp` é registrada na instalação.
