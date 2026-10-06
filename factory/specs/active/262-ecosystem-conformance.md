---
id: 262
title: Ecosystem Conformance — cross-product contract suite
agent: claude
risk: medium
verification:
  - python -m pytest tests/ -x -q
  - ruff check src tests && ruff format --check src tests && mypy
---

# Program V1 - Phase 15: Ecosystem Conformance (prompt_evo_step10 §32, P16)

## Context

Contracts are only real if consumers prove they can read them.

## Problem

No suite proving The Forger / Spark Forge / API Forge consume Doctor
artifacts without internals.

## Objectives

- `tests/conformance/` fixtures: handoff bundle, agent context,
  evidence bundle, contracts — each validated against published schemas
  with a simulated external consumer (fresh import, no engine imports).
- CI job `contract-conformance` already exists; this fills it.

## Compatibility

- Test-only.

## Tests

- Consumer simulation decodes every published artifact schema.
