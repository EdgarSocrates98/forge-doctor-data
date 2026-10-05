---
id: 279
title: Scale Envelope Extension
agent: claude
risk: high
status: accepted
commit: 60d5cde
verification:
  - python -m pytest tests/unit/test_fleet_bench.py -x -q
  - python tools/benchmarks/fleet.py budget-check
---

# RC Hardening Program (prompt_evo_rc_hardening)

Measured scan=250 / merge=500 envelopes with env-block provenance + p95; scheduled regression gate; n=1000 explicitly unproven.

## Evidence

- `tools/benchmarks/fleet.py`
- `docs/benchmarks/fleet-scan-n250.json`
- `docs/benchmarks/fleet-merge-n250-n500.json`
- `docs/benchmarks/fleet-budget.json`
- `docs/performance-budgets.md`
- `.github/workflows/benchmarks.yml`
- `tests/unit/test_fleet_bench.py`

## Acceptance Criteria

- Delivered per the program phase; verification commands above pass.
- Claims bounded by proof artifacts (claim-to-evidence rule).
