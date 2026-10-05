---
id: 273
title: v1.0 Readiness — scorecard, changelog sections, honest gap list
agent: claude
risk: medium
verification:
  - python -m pytest tests/ -x -q
  - grep -c "^### " CHANGELOG.md
---

# Consolidation Wave — Phase I (prompt_evo_consolidacao1 §Phase I)

Readiness is a scorecard, not a sentiment: every claim v1.0 may make
is bound to a proof artifact and the gate that keeps it true.

## Acceptance Criteria

- `docs/v1-readiness.md` — claims table (real repos / scale /
  stable contracts / reproducible outputs / explicit ecosystem
  boundary / reproducible CI / decoupled integration) each mapped to
  proof artifact + gate.
- Pre-tag readiness checklist: full pytest, ruff+mypy, contracts
  conformance fixtures, api-surface check, golden metrics + run,
  lab run, release-candidate dry run, CHANGELOG migration,
  version bump, human sign-off.
- `CHANGELOG.md` `[Unreleased]` organized into Added / Changed /
  Fixed / Deprecated / Removed / Security.
- Honest gap list: n=500/1000 unproven, no `fix` subcommand, PyPI
  publish gated on Trusted Publishing, real-corpus depth is 3 slices.
- `docs/roadmap.md` + `docs/release.md` synced to the new gates.

## Evidence

- Commit `5735717` — scorecard, changelog, doc sync.
