---
id: 249
title: Docs/Roadmap Sync — deterministic project status
agent: claude
risk: medium
verification:
  - python -m pytest tests/ -x -q
  - ruff check src tests && ruff format --check src tests && mypy
---

# Program V1 - Phase 2: Docs/Roadmap Sync (prompt_evo_step10 §7, P3)

## Context

The roadmap described shipped features as future work; docs drifted.

## Problem

No deterministic way to prove docs match code: commands, plugins,
contracts, MCP tools, and Factory state were hand-maintained prose.

## Objectives

- `project status` emits implemented capabilities: CLI commands, plugin
  checks, schema/contract versions, MCP tools, Factory spec state.
- `project status --check` fails (CI) when committed docs drift from
  generated output.

## Non-Objectives

- Rewriting prose docs automatically — the check guards sections that
  are generated, not essays.

## Compatibility

- New CLI group only; no existing command changes.

## Tests

- Status output deterministic across runs; `--check` fails on drift.
