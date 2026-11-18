# Instalação global (escopo user) — forge-doctor-data

Instala uma vez para todos os projetos do usuário:

```bash
forge-doctor-data install --scope user
```

Escreve a entrada MCP gerenciada em `~/.mcp.json` e o ledger de estado em
`~/.forge-doctor-data/` — nenhum arquivo vai para `~/.claude/` ou
`~/.agents/` (não há espelhos de host neste forge hoje), e o registro
`.forge/context/` é de workspace, não de conta. Combinável com
instalações de projeto: o nível mais específico (`project`) sempre
prevalece.
