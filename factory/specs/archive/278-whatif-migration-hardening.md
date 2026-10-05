---
id: 278
title: What-If / Migration Hardening
agent: claude
risk: high
status: accepted
commit: 1121104
verification:
  - python -m pytest tests/unit/test_whatif_hardening.py tests/unit/test_hardening.py -x -q
---

# RC Hardening Program (prompt_evo_rc_hardening)

Determinism + no-mutation + exhaustive concept-registry sweep (missing evidence never yields DIRECT); 58-test §12-18 suite; ScanRequestError on bad paths; corrupt-snapshot ValueError; load_pack traversal guard; severity-first bounded() + evidence_refs resync.

## Evidence

- `tests/unit/test_whatif_hardening.py`
- `tests/unit/test_hardening.py`
- `src/forge_doctor_data/core/service.py`
- `src/forge_doctor_data/core/execution_history.py`
- `src/forge_doctor_data/core/knowledge.py`
- `src/forge_doctor_data/core/agent_context.py`
- `src/forge_doctor_data/contracts/models.py`

## Acceptance Criteria

- Delivered per the program phase; verification commands above pass.
- Claims bounded by proof artifacts (claim-to-evidence rule).
