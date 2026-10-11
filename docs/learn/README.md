# Forge Doctor Data — trilha de aprendizado

| Nível | Caminho |
|---|---|
| **Iniciante** | [Quickstart](../installation/quickstart.md) → [first-run](../tutorials/first-run.md) → receita [scanear projeto](recipes/scan-project.md) |
| **Intermediário** | [scan](recipes/scan-project.md) → [checks/profiles](recipes/checks-profiles.md) → [explain](recipes/explain-finding.md) → `forge-doctor-data doctor` |
| **Avançado** | `lab`/`golden` → `policy` packs → `plugins`/`knowledge` packs → `sbom`/`contracts` |
| **Contribuidor** | [CONTRIBUTING](../../CONTRIBUTING.md) → catálogo de checks → golden repositories |
| **Agente (IA)** | [SPEC](../../SPEC.md) → [agent-context](../agent-context.md) → `forge.agentic.json` workflows (`scan`, `doctor`) → `--format json` |

## Receitas (problema → solução)

| Tenho este problema | Receita |
|---|---|
| "O que está errado neste projeto de dados?" | [scan-project](recipes/scan-project.md) |
| "Quero um subset de regras/severidade" | [checks-profiles](recipes/checks-profiles.md) |
| "Por que este finding disparou?" | [explain-finding](recipes/explain-finding.md) |
| "Como instalo o Doctor num projeto?" | [instalar-doctor](recipes/instalar-doctor.md) |
| "Quais findings ataco primeiro?" | [advise-acoes](recipes/advise-acoes.md) |
| "Como separo regressão de dívida antiga?" | [baselines-history](recipes/baselines-history.md) |
| "Como viro gate de CI?" | [ci-gate](recipes/ci-gate.md) |
| "Como estendo com plugins/packs?" | [plugins-knowledge](recipes/plugins-knowledge.md) |
| "Como uso pelo Devin/Claude/Codex?" | [mcp-hosts](recipes/mcp-hosts.md) |
| "Doctor ou Spark Forge?" | [diferenca-sparkforge](recipes/diferenca-sparkforge.md) |
| "Contexto de agente com orçamento?" | [agente-contexto](recipes/agente-contexto.md) |

Hub do ecossistema (descoberta cross-forge): `the-forge/docs/hub/` — install, which-forge, hosts, MCP, troubleshooting.

Índice gerado: [../INDEX.md](../INDEX.md).
