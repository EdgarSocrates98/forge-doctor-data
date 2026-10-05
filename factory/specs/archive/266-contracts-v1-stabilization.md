---
id: 266
title: forge-contracts/1 Stabilization — UnknownFact, x-*, strict null semantics
agent: claude
risk: high
verification:
  - python -m pytest tests/unit/test_contracts_hardening.py tests/unit/test_contract_boundaries.py -x -q
  - ruff check src tests && mypy src
---

# Consolidation Wave — Phase B (prompt_evo_consolidacao1 §Phase B)

Freeze the universal vocabulary and make `forge_doctor_data.contracts`
a dependency-free, JSON-native boundary that tolerates forward- and
backward-compatible wire drift without ever fabricating facts.

## Acceptance Criteria

- Vocabulary frozen: `Entity`, `Relationship`, `Evidence`, `Finding`,
  `Capability`, `UnknownFact`, `MigrationPlan`, `RemediationPlan`,
  `HandoffBundle`, `DiagnosticManifest`, `ContractVersion`
  (`forge-contracts/1`).
- `UnknownFact` carries honest unknowns through the wire — never
  fabricated, always surfaced.
- `x-*` extension fields preserved on round-trip (forward compat);
  unknown non-`x-` keys rejected or surfaced, never silently dropped.
- Strict null semantics: explicit `null` is distinguishable from key
  absence in every `from_dict` (the `capabilities: null` bug class is
  tested).
- Deterministic `to_dict()` — byte-identical output for identical
  state; sorted keys/entities.
- `from_dict` tolerates legacy wire forms (e.g. dict-form remediation
  actions normalize to description strings).
- Architectural drift test (`test_contract_boundaries.py`):
  `forge_doctor_data.contracts` imports zero engine modules; no
  vendor/domain names in the contract layer (docstrings pruned from
  the AST scan).

## Evidence

- Commit `d5d54fa` — contract hardening + boundary tests.
