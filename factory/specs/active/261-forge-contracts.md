---
id: 261
title: Forge Contracts — shared versioned contract package
agent: claude
risk: medium
verification:
  - python -m pytest tests/ -x -q
  - ruff check src tests && ruff format --check src tests && mypy
---

# Program V1 - Phase 14: Forge Contracts (prompt_evo_step10 §20, P16)

## Context

Spark Forge, API Forge and The Forger need explicit contracts without
importing Doctor internals.

## Problem

Shared models (Entity, Relationship, Evidence, Finding, Capability,
MigrationPlan, RemediationPlan, HandoffBundle, DiagnosticManifest,
ContractVersion) live inside the engine; consumers would couple to
internals.

## Objectives

- `forge_doctor_data/contracts/` package: versioned, dependency-free
  contract models + ContractVersion negotiation.
- Engine models re-export/subclass the contracts; JSON schemas stay the
  wire source of truth.

## Non-Objectives

- Extracting the engine; publishing a separate PyPI package in-repo
  (evaluated at v1).

## Compatibility

- Existing schema versions unchanged; contracts additive.

## Tests

- Contract serialization roundtrip; version negotiation tests.
