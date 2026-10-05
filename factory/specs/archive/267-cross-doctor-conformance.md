---
id: 267
title: Cross-Doctor Conformance — canonical schemas, fixtures, conformance CLI
agent: claude
risk: high
verification:
  - python -m pytest tests/unit/test_conformance.py -x -q
  - forge-doctor-data contracts conformance --fixtures
  - ruff check src tests && mypy src
---

# Consolidation Wave — Phase C (prompt_evo_consolidacao1 §Phase C)

Any Doctor — including a non-Python one — must be able to validate a
payload against `forge-contracts/1` without importing the engine.

## Acceptance Criteria

- Canonical JSON Schemas (draft 2020-12 subset) for all 10 contract
  kinds in `forge_doctor_data.contracts.schemas` — pure data, no
  engine imports.
- Canonical fixtures under `contracts/fixtures/*.json` generated from
  model `to_dict()` output and shipped in the wheel.
- `core/conformance.py` two-layer check: schema shape validation +
  strict model decode + contract-version negotiation, with kind
  auto-detection.
- `forge-doctor-data contracts conformance <file|-> [--kind K]
  [--fixtures] [--json]` CLI; `contracts schema [kind]` dumps schemas;
  `contracts verify` validates artifacts.
- Subprocess proof: a consumer with only `forge_doctor_data.contracts`
  on sys.path decodes every fixture — zero engine imports.

## Evidence

- Commit `8d9218b` — conformance layer, schemas, fixtures, CLI.
