---
id: 258
title: Evidence Store — pluggable execution history storage
agent: claude
risk: medium
verification:
  - python -m pytest tests/ -x -q
  - ruff check src tests && ruff format --check src tests && mypy
---

# Program V1 - Phase 11: Execution Store (prompt_evo_step10 §14, P10)

## Context

Execution history was JSONL-only; large histories need indexing without
a server.

## Problem

No store abstraction: readers/writers coupled to JSONL layout.

## Objectives

- `ExecutionStore` protocol: `append`, `iter_samples`, `export_jsonl`.
- `JsonlStore` (portable default) and `SQLiteStore` (stdlib, indexed).
- Every store exports JSONL for auditability; DuckDB stays optional.

## Compatibility

- JSONL format unchanged; SQLite additive.

## Tests

- Roundtrip both stores; deterministic ordering; export equivalence.
