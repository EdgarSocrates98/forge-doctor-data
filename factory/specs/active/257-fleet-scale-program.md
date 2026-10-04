---
id: 257
title: Fleet Scale Program — measured curves at 10-1000 repos
agent: claude
risk: high
verification:
  - python -m pytest tests/ -x -q
  - ruff check src tests && ruff format --check src tests && mypy
---

# Program V1 - Phase 10: Fleet Scale Program (prompt_evo_step10 §15, P11)

## Context

Fleet intelligence exists but scale behaviour is unproven.

## Problem

No measured curves: cold/warm/incremental scan, graph build/merge,
history/portfolio query times, RAM across 10/50/100/500/1000 synthetic
repos. Budgets cannot precede measurement.

## Objectives

- `tools/benchmarks/fleet.py` — deterministic synthetic workspace
  generator + measurement harness (seeded, offline).
- Recorded results in the run record; derived budgets land in
  docs/performance-budgets.md only after measurement.

## Non-Objectives

- Parallel/distributed execution changes before curves exist.

## Compatibility

- Tooling only; no production change.

## Tests

- Generator determinism; benchmark smoke on small N.
