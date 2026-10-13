---
id: 264
title: v1.0 Release — stable public contracts
agent: claude
risk: high
verification:
  - python -m pytest tests/ -x -q
  - ruff check src tests && ruff format --check src tests && mypy
---

# Program V1 - Phase 17: v1.0 Release (prompt_evo_step10 §8.2,§32, P4)

## Context

Final gate after the RC proves stable in the wild.

## Objectives — 1.0.0 criteria

- Versioned contracts; typed public API; stable plugin SDK.
- Deprecation policy enforced; MCP compatibility proven.
- Fleet scale measured (spec 257 budgets met).
- Trusted-publishing release; package verified installable from PyPI.
- Real-world validation corpus green (spec 256).

## Non-Objectives

- Feature additions between RC and release.

## Rollback

- Yank policy documented; contracts allow 1.x hotfixes without consumer
  breaks.

## Tests

- All prior gates + release dry-run + post-publish verify.
