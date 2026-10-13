---
id: 277
title: Plugin Trust-Boundary Hardening
agent: claude
risk: high
status: accepted
commit: a753748
verification:
  - python -m pytest tests/unit/test_plugin_boundary.py tests/unit/test_plugin*.py tests/unit/test_runner*.py -x -q
---

# RC Hardening Program (prompt_evo_rc_hardening)

53-test boundary suite; bounded-drain child capture, file-claim confinement, describe-row validation, argv bounds; runner converts non-CheckResult plugin output into internal-error findings.

## Evidence

- `tests/unit/test_plugin_boundary.py`
- `src/forge_doctor_data/plugins/isolation.py`
- `src/forge_doctor_data/core/runner.py`
- `docs/plugin-isolation.md`

## Acceptance Criteria

- Delivered per the program phase; verification commands above pass.
- Claims bounded by proof artifacts (claim-to-evidence rule).
