---
id: 259
title: Collector SDK — normalized evidence bundles
agent: claude
risk: medium
verification:
  - python -m pytest tests/ -x -q
  - ruff check src tests && ruff format --check src tests && mypy
---

# Program V1 - Phase 12: Collector SDK (prompt_evo_step10 §13, P9)

## Context

`scan` must never call the cloud; external evidence needs a separate
ingestion seam.

## Problem

No contract for externally-collected evidence (Glue runs, CloudWatch,
Athena) to enter the offline engine.

## Objectives

- `EvidenceBundle`/`EvidenceRecord` schema
  `forge-doctor-data/evidence-bundle@1`.
- `EvidenceCollector` protocol; `collector validate <bundle>` command.
- Architecture documented in docs/collectors.md.

## Non-Objectives

- Implementing the AWS collector itself (spec 260).

## Compatibility

- New module/commands; `scan` unchanged and offline.

## Tests

- Bundle validation, deterministic serialization, validator errors.
