---
id: cyc9-08
title: scenarios-doctor-data
status: inbox
created: 2026-10-15
owner: forge-doctor-data
scope: repo
cycle: 9
wave: 3
priority: p1
risk: medium
agent: codex
source: prompt_evo_cycles.md §9.3 Doctors
verification:
  - python -m pytest
---

# Cenários Forge Lab — Forge Doctor Data

## Outcome

Biblioteca versionada de cenários de diagnóstico de dados com fixtures e diagnósticos previamente classificados, medindo precisão, falsos positivos/negativos, tempo de execução, reprodutibilidade e cobertura das regras.

## Grill gate

- Problema observado: regras do doctor existem, mas precisão/cobertura não são medidas contra corpus classificado.
- Usuário afetado: Benchmark Engineer; usuário que confia no diagnóstico.
- Falha concreta: falso positivo/negativo sem medição degrada confiança silenciosamente.
- Decisão: corpus de casos com veredito esperado por regra/domínio (Airflow, Control-M, EMR, Databricks, Terraform, Parquet/Delta, Step Functions/Lambda/Athena, streaming etc.), replay determinístico.
- Fora de escopo: centralizar avaliação no the-forge; cenários que exigem cloud real.
- Critério de parada: precision/recall/FP por regra publicados com evidência; reprodutibilidade ≥ baseline declarada.

## Acceptance

- Fixtures por domínio suportado com expected.yaml (veredito por regra).
- Métricas §9.5 por execução: precision, recall, false_positive_rate, cobertura, tempo, reprodutibilidade.
- Saída compatível com contrato de métricas (cyc9-02); regras não cobertas listadas como `not_available`.
- Casos divergentes (expected vs observed) registrados como ledger de FP/FN.

## Constraints

- Execução local e determinística; sem credenciais.

## Pending

- ⚠ Domínios efetivamente suportados e formato de fixture atual (baseline cyc0-01); gates do repo a confirmar.
