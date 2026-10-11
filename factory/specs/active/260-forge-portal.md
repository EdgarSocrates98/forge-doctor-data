---
id: 260
title: Forge Portal — optional local web UI over the real services
agent: devin
risk: medium
verification:
  - python -m pytest tests/test_portal_adapter.py -x -q
  - python -m pytest -q
  - ruff check src tests && ruff format --check src tests && mypy
  - python scripts/docs/regen_docs.py && python -m pytest tests/test_doc_drift.py tests/test_doc_manifest.py tests/test_command_rationale.py -x -q
---

# Forge Portal — `forge-doctor-data portal` (prompt_evo_portal §FASE 6)

Optional, local-first web UI over the real services — a surface, never a
replacement for CLI/MCP/TUI. Part of the ecosystem-wide Forge Portal
program (canonical server `forge-portal/portal_core/forge_portal.py`,
vendored byte-identical to `src/forge_doctor_data/_forge_portal.py`;
Angular assets vendored to `src/forge_doctor_data/portal_assets/` so the
wheel ships them).

## Acceptance Criteria

- `forge-doctor-data portal` serves the SPA on 127.0.0.1 only, with a
  128-bit session token; `/api/v1/*` refuses without `X-Forge-Session`.
- `portal_adapter.py` maps forge/PortalApi/1 ops onto the real services:
  `install.service` (plan/apply/repair/uninstall/status/doctor/
  mcp_verify), `integrations.hostflow` (host probes), `api.scan` (real
  engine run), `graphview.build_view` (evidence graph on demand),
  `docs/knowledge-program/inventory.jsonl` (docs search).
- Mutations require explicit `confirm` + signed plan token bound to the
  echoed plan; stale/forged tokens refuse `PORTAL-PLAN-STALE` (409).
- Ambiguous task intent refuses `FDD-PORTAL-AMBIGUOUS` with the safe
  verb list; host launch returns the command to copy — never spawns a
  host (no TTY in a browser).
- Honest states: `NOT_INSTALLED` on virgin workspaces even when doctor
  reports `degraded`; skills/agents are `unsupported` (this forge ships
  no host assets today) — empty catalog, never fabricated.
- Missing assets refuse `FDD-PORTAL-NO-ASSETS` with the vendoring hint.

## Context / boundaries

- Read + plan stay side-effect-free; apply writes only inside the
  resolved install target + `~/.forge/`, identical to the CLI path.
- The portal never decides: it observes, plans, and applies what the
  user confirmed. No implicit host launches, no network beyond loopback.

## Constraints

- Vendored file stays byte-parity with `portal_core` — fixes go upstream
  (`forge-portal` repo), never patched locally.
- `portal_adapter.py` is hand-written per forge (like `_installkit`
  consumers) and stays lint/mypy-strict clean.
