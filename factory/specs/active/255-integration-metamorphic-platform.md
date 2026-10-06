---
id: 255
title: Integration & Metamorphic Platform — real flows, invariance tests
agent: claude
risk: high
verification:
  - python -m pytest tests/ -x -q
  - ruff check src tests && ruff format --check src tests && mypy
---

# Program V1 - Phase 8: Integration & Metamorphic Testing (prompt_evo_step10 §9-10, P5,P6)

## Context

Unit tests + labs exist but end-to-end flows and invariance properties
were unverified.

## Problem

- No flows proving wheel-install → scan → baseline → diff → new-only.
- No metamorphic guarantees (reformat / reorder must not change
  fingerprints or findings).
- No domain mutation corpus (remove checkpoint/watermark → detect).

## Objectives

- `tests/integration` flows A-E: wheel install/scan/diff; runtime
  history→regression→incident; workspace→fleet→portfolio; handoff
  contract roundtrip; plugin inject→doctor→scan.
- Metamorphic suite: whitespace/key-order/line-order invariance on
  fingerprints and findings.
- Mutation suite: seeded lab mutations must raise expected findings.

## Compatibility

- Test-only; no production API change.

## Tests

- The suite itself is the deliverable; deterministic ordering.
