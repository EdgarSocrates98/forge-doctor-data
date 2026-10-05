---
id: 280
title: Cross-Doctor Contract Finalization
agent: claude
risk: high
status: accepted
commit: baac258
verification:
  - python -m pytest tests/unit/test_forge_contracts.py tests/unit/test_contract_boundaries.py -x -q
  - forge-doctor-data contracts conformance --fixtures
---

# RC Hardening Program (prompt_evo_rc_hardening)

forge-contracts manifesto: universal vocabulary, domain prohibition (OpenAPI/GraphQL/QueryExecution), x-* extension rules, negotiation window, engine-free conformance kit proof.

## Evidence

- `docs/forge-contracts.md`
- `tests/unit/test_forge_contracts.py`

## Acceptance Criteria

- Delivered per the program phase; verification commands above pass.
- Claims bounded by proof artifacts (claim-to-evidence rule).
