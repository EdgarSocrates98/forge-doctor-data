---
id: 254
title: Agent Context Protocol — budget-aware deterministic payloads
agent: claude
risk: medium
verification:
  - python -m pytest tests/ -x -q
  - ruff check src tests && ruff format --check src tests && mypy
---

# Program V1 - Phase 7: Agent Context Protocol (prompt_evo_step10 §12, P8)

## Context

Downstream agents (Claude, Codex, Devin, The Forger) need small,
deterministic context — not a full scan dump.

## Problem

No compact projection of evidence: full JSON reports are too large for
agent budgets, and there was no delta/evidence-ref model.

## Objectives

- `agent manifest` — domains, entities, risks, capabilities,
  evidence_refs.
- `agent context --budget N` — summary-first payload trimmed to an
  approximate token budget (deterministic estimate, no tokenizer dep).
- `agent delta --since <ctx>` — added/removed/unchanged fingerprints.
- `agent evidence <ref>` — lazy detail for one finding/entity ref.

## Compatibility

- New `agent` command group; contract `agent-context` version 1.

## Tests

- Budget trimming, delta diffing, evidence resolution, deterministic
  ordering.
