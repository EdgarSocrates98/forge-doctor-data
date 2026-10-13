---
id: 265
title: CI Bootstrap Hardening — deterministic Poetry, wheel smoke, env manifest
agent: claude
risk: medium
verification:
  - python -m pytest tests/unit/test_hermetic_env.py -x -q
  - ruff check src tests tools && ruff format --check src tests
---

# Consolidation Wave — Phase A (prompt_evo_consolidacao1 §Phase A)

Make CI installs reproducible: a green run on any OS must install the
same dependency set the wheel ships, and the environment must be
inspectable after the fact.

## Acceptance Criteria

- Poetry exists before any cache step in `.github/workflows/ci.yml`
  (bootstrap order fixed: pipx Poetry -> manual venv/dep cache ->
  `poetry install`).
- `tools/env_manifest.py` emits a per-leg environment manifest
  (python/poetry/platform/resolved deps) archived as a CI artifact.
- Wheel-first smoke job: build wheel, install into a fresh venv,
  run `forge-doctor-data version`/`scan` against the wheel — never
  the source tree.
- Hermetic tests (`tests/unit/test_hermetic_env.py`): scans do not
  depend on ambient git state, env vars, or network.
- Contract schemas + fixtures ship inside the wheel
  (`pyproject.toml` include rules).

## Evidence

- Commit `da304ea` — ci: deterministic Poetry bootstrap + wheel smoke
  + env manifest.
