---
id: 252
title: Public Contract Hardening — typed API, audited packs
agent: claude
risk: medium
verification:
  - python -m pytest tests/ -x -q
  - ruff check src tests && ruff format --check src tests && mypy
---

# Program V1 - Phase 5: Public Contract Hardening (prompt_evo_step10 §19,§25, P15,P21)

## Context

Public Python API returned `Any`; knowledge packs had freshness checks
but no release-facing audit classification.

## Problem

- `what_if()`/`migrate_plans()` typed as `Any` erodes the contract.
- Pack states (fresh/stale/expired/invalid_source/unverified) were not
  surfaced as a single audit view.

## Objectives

- Typed returns: `list[WhatIfReport]`, `list[MigrationPlan]`.
- `knowledge audit` command + `audit_packs()` classifier; non-fresh
  exits non-zero for CI review.

## Compatibility

- Return types narrow, never widen; runtime values unchanged.

## Tests

- mypy strict clean; audit statuses deterministic per fixture packs.
