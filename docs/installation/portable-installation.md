# Instalação portátil — forge-doctor-data

Instala em qualquer diretório/repositório — sem estrutura prévia exigida.

```bash
cd <qualquer-projeto>
forge-doctor-data install                    # escopo projeto (padrão)
forge-doctor-data install --dry-run          # planeja sem escrever
forge-doctor-data install --profile minimal  # só CLI+MCP+marker
forge-doctor-data install --profile full     # skills + agents + todos os hosts
```

O que acontece: assets gerenciados vão para `.agents/`, `.claude/`,
`.devin/`, `.codex/` conforme os hosts detectados; `.mcp.json` ganha uma
entrada gerenciada; `AGENTS.md` recebe um bloco delimitado
`<!-- forge-doctor-data:managed -->` — conteúdo seu nunca é sobrescrito.

Perfis: `minimal` (essencial) · `recommended` (workflow completo, padrão)
· `full` (teto de disclosure — não é autorização extra).
