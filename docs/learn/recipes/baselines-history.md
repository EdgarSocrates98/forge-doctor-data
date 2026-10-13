# Receita — baselines e histórico de scans

**O quê:** `scan --record` grava snapshots em `.forge-doctor-data/history/`;
`history`, `history diff`, `history trend` e `scan --baseline` consomem a
série gravada.
**Por que:** finding novo ≠ finding existente — só a série temporal separa
regressão de dívida herdada.
**Quando:** antes de cobrar melhoria; gates que falham só no que é novo.
**Quando não:** primeiro scan de um repo — não há série ainda.

## Passo a passo

```bash
forge-doctor-data scan . --record --keep 30      # grava snapshot, retém 30
forge-doctor-data history                        # lista snapshots
forge-doctor-data history trend                  # contagem por categoria na série
forge-doctor-data history diff <a> <b>           # o que entrou/saiu entre dois
forge-doctor-data scan . --baseline main --new-only   # gate: só findings novos
```

## Saída esperada / interpretação

`history` lista snapshots com timestamp e totais; `trend` mostra a direção
por categoria; `diff` separa `new`/`resolved`. `--baseline main` compara
contra a ref git — findings pré-existentes não quebram o gate.

## Verificação

Depois de `--record`, `forge-doctor-data history` deve listar o snapshot;
sem série gravada a resposta honesta é "No history".

## Limitações

A série vive no repo (`.forge-doctor-data/history/`) — clones novos não
carregam histórico. `diff` compara findings por fingerprint, não por linha.

## Erros comuns

| Sintoma | Causa | Ação |
|---|---|---|
| "No history" | nunca rodou `--record` | `scan . --record` primeiro |
| gate falha em dívida antiga | faltou `--baseline`/`--new-only` | `scan . --baseline <ref> --new-only` |

## Uso por agentes

`get_execution_baseline` e `get_regressions` (MCP) leem a mesma série —
agente compara sem re-rodar scan.
