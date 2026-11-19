# Instalação portátil — forge-doctor-data

Instala em qualquer diretório/repositório — sem estrutura prévia exigida.

```bash
cd <qualquer-projeto>
forge-doctor-data install                    # escopo projeto (padrão)
forge-doctor-data install --dry-run          # planeja sem escrever
forge-doctor-data install --profile minimal  # perfil registrado no recibo
forge-doctor-data install --gateway-profile economy  # menor custo de execução
```

O que acontece: `.mcp.json` ganha uma entrada gerenciada com argv
absoluto (nunca depende de PATH); `.forge/context/` recebe o manifesto
`forge/context/v1` + entrada no registry compartilhado; `AGENTS.md`
recebe um bloco compacto `<!-- forge:forge-doctor-data -->` (identidade,
domínios e ponteiros para o manifesto e `AGENT_PROTOCOL.md` — boot L0
mínimo, sem duplicar detalhe de CLI/discovery), `CLAUDE.md` recebe o
bloco `forge:ecosystem` e `AGENT_PROTOCOL.md` é gerado — conteúdo seu
nunca é sobrescrito.

Reinstalação é **incremental**: o ledger compara bytes antes de escrever
— assets idênticos não são reescritos e o recibo reporta `counts`
(`created`/`updated`/`unchanged`/`adopted`/`skipped`/`written` +
`written_bytes`) com zeros honestos. Os campos `status` +
`verification.status` do recibo `forge/InstallReceipt/v1` são deriváveis
para `forge/InstallLifecycle/v1` pelo plano de controle
(`completed` + `PASS` → `verified`; health `healthy` → `ready`).

Perfis: `minimal` · `recommended` (padrão) · `full`. Hoje os três perfis
são **equivalentes em superfície escrita** — este forge não espelha
assets de host; o perfil é declarado no recibo e no manifesto
`forge/context/v1` para o orquestrador ordenar e auditar.

Perfil de execução: `economy` reduz custo e contexto mantendo roteamento
seguro; `balanced` é padrão; `deep` amplia capacidade para tarefas difíceis.
A escolha fica no recibo e é preservada quando o The Forge delega instalação.

Automação: saída JSON é automática fora de TTY (pipes/CI) — não há flags
`--json`/`--no-input` nesta superfície; mutações exigem `--yes` e nunca
pedem confirmação fora de terminal interativo.
