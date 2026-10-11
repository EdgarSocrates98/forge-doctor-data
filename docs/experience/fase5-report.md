# FASE 5 — Forge Doctor Data: relatório de validação

Data: 2026-10-11 · Branch: feat/ultimate-completion

## Entregue

- **`hosts` verb + `get_host_status` MCP tool** (observe-only):
  `integrations/hostflow.py` porta o fluxo dos irmãos — detecta binário,
  versão, auth via subcomando oficial (`claude auth status`,
  `devin auth status`, `codex login status`), e lê a integração via
  `install status`. `hosts <h> --launch` abre o host no repo — só com TTY,
  nunca deslogado (`NEEDS_LOGIN` + `login_hint`), nunca via MCP.
  `copilot` reporta `logged_in: null` honestamente (sem subcomando
  documentado).
- **Menu TUI refeito para a superfície §5.2**: scan / checks / advise /
  history / export / policy list / doctor / install status / hosts /
  mcp-verify / capabilities / graph ui / wizard. O item `['diagnose']`
  era quebrado (exige `source`) — substituído por `scan .`.
  `_SUSPEND_VERBS` ampliado (scan, advise, export).
- **Contrato do menu contra o parser real**: `test_menu_argv_resolves_
  against_real_commands` valida cada argv contra os comandos/grupos
  registrados no typer — item inválido não volta a entrar em silêncio.
- **9 testes do fluxo de hosts** (`tests/unit/test_hosts_flow.py`):
  NOT_DETECTED, READY, NEEDS_LOGIN nunca lança, no_tty recusa com
  `launch_command`, launch real com TTY grava exit code, `all` nunca
  lança, host desconhecido recusa, copilot honesto, MCP observe-only.
- **Documentação**: rationale `hosts` (why/when), `hosts` no README,
  8 receitas PT-BR (instalar, advise, baselines/history, CI gate,
  plugins/knowledge, MCP/hosts, Doctor vs Spark Forge, agent context).
- **Re-selos**: `docs/api-surface.json` (cli `hosts` + mcp
  `get_host_status`, 13→14 tools), pin explícito no freeze test,
  `docs/rc-baseline.json` re-gerado.

## E2E real (scratch `pf`/`fdd-e2e`, repo git efêmero)

| Passo | Resultado |
|---|---|
| `install --yes` | completed, ledger 2 entries, `.mcp.json` managed key |
| `install status` | `healthy`, drift 0 |
| `install mcp-verify` | PASS — handshake real, 14 tools, invoke ok |
| `scan . --quiet` (fixture dbt+Airflow+pandas) | 342 checks, 3 warnings citados (PY002, REP001, REP002) |
| `hosts devin` | READY (devin 3000.11.3, integração healthy) |
| `agent manifest` | contexto real (summary 52p/17i/3w) |
| `devin mcp list` no scratch | `forge-doctor-data` listado nativamente |

## Gates

- Slice tocado + gates de docs/freeze: verde.
- api-surface regenerado; `test_mcp_surface_frozen` pin 13→14.
- Divergência de documentação: 0 (0 missing, 0 undocumented).
- Suíte integral no HEAD: **2638 passed / 1 failed / 0 errors** —
  a única falha era `rc-baseline` com `test_count` nulo (baseline
  gerado sem `--tests`); re-selado com os números medidos da própria
  run (**2639 testes, 82.85% de cobertura**) → verde em re-run.
  JUnit autoritativo: `fdd-suite2.xml`.

## Achados e limitações honestas

- `mcp-verify` depende de `forge-doctor-data` resolvível no PATH — num
  ambiente sem o venv no PATH o handshake reporta BLOCKED com a razão
  ("install incomplete"), não um crash.
- `hosts --launch` lança de verdade quando há console — validado em
  exec com console Windows (o devin TUI abriu); sem TTY a recusa é
  `no_tty` (testado).
- Doctor Data não publica mirrors de skills/agents hoje (decisão do
  repo, documentada em `install/service.py`) — a instalação gerencia
  chave MCP + marcadores AGENTS.md/CLAUDE.md.
- O workflow do host é: `install` → `mcp-verify` → `hosts` → abrir o
  host → pedir em linguagem natural ("rode scan_project…").
