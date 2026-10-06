---
id: 263
title: v1 Release Candidate — 0.9.0 consolidation gate
agent: claude
risk: high
verification:
  - python -m pytest tests/ -x -q
  - ruff check src tests && ruff format --check src tests && mypy
---

# Program V1 - Phase 16: v1 Release Candidate (prompt_evo_step10 §8,§32, P4)

## Context

Surface grew far beyond `0.7.0`; the consolidation release is `0.9.0`.

## Problem

Version no longer reflects surface or stability claims.

## Objectives — 0.9.0 criteria

- main protected (documented ruleset), CI green with stable checks.
- docs synchronized; `project status --check` enforced.
- package publishable; release verify wired.
- contracts reviewed; MCP modern+legacy; supply chain minimum; E2E
  integration suite.
- CHANGELOG 0.9.0 entry.

## Non-Objectives

- Declaring 1.0.0 (spec 264).

## Compatibility

- Version bump only; SemVer rules documented in docs/deprecation.md.

## Tests

- Full gates + `verify_release.py --tag v0.9.0` dry-run.
