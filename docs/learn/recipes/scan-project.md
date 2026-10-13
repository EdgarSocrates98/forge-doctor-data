# Receita — o que está errado neste projeto de dados?

**O quê:** `forge-doctor-data scan <path>` varre o projeto atrás de problemas
de engenharia de dados — checks versionados, evidence-first.
**Por que:** revisão determinística, não lint genérico.
**Quando:** auditoria de repo de dados, pré-merge, onboarding.
**Quando não:** validação de dados em runtime — scan é estático.

## Passo a passo

```bash
forge-doctor-data scan .                # o help aponta: scan . | checks | explain
forge-doctor-data scan . --format json  # máquina-first
```

## Saída esperada / interpretação

Findings por check com severidade e evidência citável; exit code reflete a
política. `unresolved` é resposta, não lacuna escondida.

## Verificação

`forge-doctor-data doctor` confirma ambiente (`project files indexed`,
`knowledge packs`, `plugins`) antes de culpar o scan.

## Limitações

Análise estática de projeto — não executa pipelines nem conecta em bancos;
profiles existem para domínios (`spark-performance`, `glue-migration`, …).

## Erros comuns

| Sintoma | Causa | Ação |
|---|---|---|
| findings suspeitos de mais | profile errado | `--profile default` vs `strict` |
| check indesejado | regra não se aplica | `--ignore <CHECK-ID>` ou suppressions |

## Uso por agentes

Workflow `scan` do `forge.agentic.json`; findings citam `CHECK-ID` —
`explain <CHECK-ID>` dá a cadeia de evidência.
