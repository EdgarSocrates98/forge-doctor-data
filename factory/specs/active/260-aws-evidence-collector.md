---
id: 260
title: AWS Evidence Collector — first reference adapter
agent: claude
risk: low
verification:
  - python -m pytest tests/ -x -q
  - ruff check src tests && ruff format --check src tests && mypy
---

# Program V1 - Phase 13: AWS Evidence Collector (prompt_evo_step10 §13.3, P9)

## Context

The collector contract exists (spec 259); AWS is the reference cloud.

## Problem

Glue/EMR/Athena/CloudWatch evidence cannot reach the engine.

## Objectives

- Optional `forge-doctor-data-aws` adapter emitting EvidenceBundles from
  Glue Job Runs, CloudWatch, EMR, Athena, Lake Formation (+ optional
  CloudTrail, Step Functions, MSK/Kinesis).
- Normalized evidence only; the engine consumes bundles offline.

## Non-Objectives

- Cloud calls inside `scan`; bundling boto3 as a core dependency.

## Compatibility

- Separate optional package; core untouched.

## Tests

- Bundle conformance on recorded fixtures (no live AWS in tests).
