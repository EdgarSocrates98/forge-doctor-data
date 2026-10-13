---
id: 274
title: RC Baseline + Contract Freeze
agent: claude
risk: high
status: accepted
commit: 9b3bdfe
verification:
  - python tools/rc_baseline.py --check
  - python tools/api_surface.py --check
  - python -m pytest tests/unit/test_rc_baseline.py tests/unit/test_public_api_freeze.py -x -q
---

# RC Hardening Program (prompt_evo_rc_hardening)

RC policy + baseline artifact; api-surface freeze with stability classes; public API hash gated.

## Evidence

- `docs/rc-policy.md`
- `docs/rc-baseline.json`
- `tools/rc_baseline.py`
- `tools/api_surface.py`
- `docs/api-surface.json`
- `tests/unit/test_rc_baseline.py`
- `tests/unit/test_public_api_freeze.py`

## Acceptance Criteria

- Delivered per the program phase; verification commands above pass.
- Claims bounded by proof artifacts (claim-to-evidence rule).
