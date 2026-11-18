# Instalação portátil — forge-doctor-data

Instala em qualquer diretório/repositório — sem estrutura prévia exigida.

```bash
cd <qualquer-projeto>
forge-doctor-data install                    # escopo projeto (padrão)
forge-doctor-data install --dry-run          # planeja sem escrever
forge-doctor-data install --profile minimal  # perfil registrado no recibo
forge-doctor-data install --gateway-profile economy  # menor custo de execução
```

O que acontece: `.mcp.json` ganha uma entrada gerenciada; `.forge/context/`
recebe o manifesto `forge/context/v1` + entrada no registry compartilhado;
`AGENTS.md`/`CLAUDE.md` recebem blocos `<!-- forge:forge-doctor-data -->`
quando já existem e `AGENT_PROTOCOL.md` é gerado — conteúdo seu nunca é
sobrescrito.

Perfis: `minimal` · `recommended` (padrão) · `full`. Hoje os três perfis
são **equivalentes em superfície escrita** — este forge não espelha
assets de host; o perfil é declarado no recibo e no manifesto
`forge/context/v1` para o orquestrador ordenar e auditar.

Perfil de execução: `economy` reduz custo e contexto mantendo roteamento
seguro; `balanced` é padrão; `deep` amplia capacidade para tarefas difíceis.
A escolha fica no recibo e é preservada quando o The Forge delega instalação.
