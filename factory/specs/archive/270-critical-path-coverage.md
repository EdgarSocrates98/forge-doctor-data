---
id: 270
title: Critical-Path Coverage — mutation-kill suite + failure injection on gates
agent: claude
risk: medium
verification:
  - python -m pytest tests/unit/test_contract_mutations.py -x -q
  - python -m pytest tests/unit/ -x -q
---

# Consolidation Wave — Phase F (prompt_evo_consolidacao1 §Phase F)

Tests that only assert the happy path cannot prove trust. The gates
themselves must be attacked: corrupt inputs must be caught, injected
failures must surface as honest verdicts — never crashes or silent
passes.

## Acceptance Criteria

- Mutation-kill suite (`test_contract_mutations.py`): systematic
  single-field corruption of every canonical contract fixture —
  each mutation must be rejected by the conformance gate (100% kill
  rate across kinds).
- Failure injection on the conformance path: truncated JSON, wrong
  kinds, version mismatches, missing required fields — all produce
  structured diagnostics, not tracebacks.
- Contract module coverage measured at 97% from its dedicated suite.
- Existing metamorphic (`test_mutations.py` determinism invariant) and
  adversarial/flows failure-injection suites confirmed green.

## Evidence

- Commit `7c20aff` — mutation-kill + failure-injection suite.
