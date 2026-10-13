---
id: 251
title: MCP Modern Compat — legacy/modern protocol adapters
agent: claude
risk: medium
verification:
  - python -m pytest tests/ -x -q
  - ruff check src tests && ruff format --check src tests && mypy
---

# Program V1 - Phase 4: MCP Modern Compat (prompt_evo_step10 §11, P7)

## Context

MCP is the agent-facing surface; protocol revisions shipped without an
adapter story.

## Problem

Single mcp_server implementation; no explicit legacy (2024 / 2025-03 /
2025-06) vs modern handling, no conformance suite.

## Objectives

- Adapter layer: modern protocol path + legacy adapter preserving
  pre-existing initialize/tools-call shapes.
- Conformance tests: initialize, tools/list, tools/call, error shape,
  sandbox path restrictions, backward compatibility.

## Non-Objectives

- Depending on the official MCP SDK at runtime (dev-only if used).

## Compatibility

- Legacy clients keep working; no tool name/schema removal.

## Tests

- Conformance suite green; invalid params produce protocol errors, not
  tracebacks.
