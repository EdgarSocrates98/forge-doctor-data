---
id: 253
title: Core Architecture Consolidation — isolation, boundaries, no _vN sprawl
agent: claude
risk: high
verification:
  - python -m pytest tests/ -x -q
  - ruff check src tests && ruff format --check src tests && mypy
---

# Program V1 - Phase 6: Core Architecture Consolidation (prompt_evo_step10 §16-18,§21,§27, P12,P13,P17,P23)

## Context

`experiments_v2.py`, `migration_v2.py`, `optimize_v2.py` accreted as
sibling modules; plugins only ran in-process; no deprecation contract.

## Problem

- Generational `_v2` modules lack explicit package architecture.
- Plugin execution had no isolation mode.
- No published deprecation policy before v1.

## Objectives

- `plugins.execution = isolated` subprocess mode (timeout, stdout cap,
  structured results) — process isolation, not a sandbox.
- Consolidate `*_v2` modules into explicit packages with compat facades.
- docs/architecture-boundaries.md (bounded contexts) +
  docs/deprecation.md (removal contract).

## Compatibility

- Old import paths keep working via facades until the documented
  removal version; `plugins.execution` defaults to `trusted`.

## Tests

- Isolation proxy round-trips CheckResults; facade imports stable.
