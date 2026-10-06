---
id: 248
title: Main CI Governance — stable required checks, trusted main
agent: claude
risk: high
verification:
  - python -m pytest tests/ -x -q
  - ruff check src tests && ruff format --check src tests && mypy
---

# Program V1 - Phase 1: Main CI Governance (prompt_evo_step10 §4-6, P0-P2)

## Context

Main shipped a broken experimental script (`_bench_history.py`) that
failed Ruff and proved the pipeline was a single opaque job with no
stable check names for branch protection.

## Problem

- One `quality` job ran lint+types+tests+build under a 3-version matrix:
  slow, unstable names, no governance surface.
- Experimental scripts in repo root could fail package gates.
- No branch protection contract existed.

## Objectives

- Stable required-check job names: `static-analysis`,
  `unit-tests-<py>`, `package-build`, `platform-smoke-<os>`,
  `forge-gates` (dogfood, contracts, Lab, golden).
- Single-Python static job (3.12): lint/type info does not multiply
  across versions.
- Experimental tooling lives in `tools/` and cannot fail the package.
- Coverage gate `fail_under = 80` as the starting floor.

## Non-Objectives

- Setting the GitHub Ruleset itself (needs admin API); configuration is
  documented in docs/release.md instead.

## Compatibility

- No public API/CLI/JSON change. CI job *names* change; documented in
  docs/release.md.

## Tests / Rollout / Rollback

- `ruff check .`, `ruff format --check .`, `mypy`, `pytest` green.
- Rollback: revert ci.yml to the single quality job.
