---
id: 283
title: Post-RC Observation Discipline
agent: claude
risk: high
status: accepted
commit: 9b3bdfe
verification:
  - python tools/rc_baseline.py --check
---

# RC Hardening Program (prompt_evo_rc_hardening)

P0-P3 defect triage, allowed/forbidden change lists, manual-only telemetry, forge-contracts/1 compatibility rule (breaks restart RC numbering).

## Evidence

- `docs/rc-policy.md`

## Acceptance Criteria

- Delivered per the program phase; verification commands above pass.
- Claims bounded by proof artifacts (claim-to-evidence rule).
