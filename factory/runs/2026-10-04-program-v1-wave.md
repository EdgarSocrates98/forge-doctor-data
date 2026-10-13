# Program V1 — Step-10 Wave Run Record (specs 248–264)

Date: 2026-10-04 · Specs: `factory/specs/active/248..264`
Priority: QUALITY > RELIABILITY > CONTRACTS > SCALE > INTEROP > FEATURES.

## Per-spec status

| Spec | Title | Status | Evidence |
|------|-------|--------|----------|
| 248 | main-ci-governance | delivered | `docs/governance.md` (ruleset, stable check names), CI `forge-gates` incl. doc-drift job |
| 249 | docs-roadmap-sync | delivered | `project status --write/--check` deterministic, `docs/project-status.md` generated, drift gated in CI |
| 250 | release-supply-chain | delivered | 0.9.0 bump (`pyproject`, `__init__`), CHANGELOG, `tools/verify_release.py`, security workflow |
| 251 | mcp-modern-compat | delivered | `integrations/mcp_protocol.py` legacy+modern adapters, official-SDK conformance suite (`tests/integration/test_mcp_conformance.py`) |
| 252 | public-contract-hardening | delivered | `contracts/` package: versioned models, negotiation, `core/contract_adapters.py`, roundtrip tests |
| 253 | core-architecture-consolidation | delivered | `_v2` modules folded into `core/experiments`, `core/migration`, `core/optimization` packages; facades kept (`experiments_v2.py` etc.) |
| 254 | agent-context-protocol | delivered | `agent manifest/context --budget/delta/evidence` (pre-existing), budget-aware compaction tested |
| 255 | integration-metamorphic-platform | delivered | `tests/integration/test_flows.py` (25 flows) + `test_mutations.py` (7 mutations + determinism invariant) |
| 256 | real-world-validation | partial | `golden/manifest.json` + `docs/corpus.md` + provenance tests. Real OSS slices still to vendor |
| 257 | fleet-scale-program | partial | `tools/benchmarks/fleet.py` seeded harness; n=10/50 measured (`docs/performance-budgets.md`). 100/500/1000 unproven |
| 258 | evidence-store | delivered | `core/execution_store.py` + evidence bundle `--evidence-out` (pre-existing, hardened) |
| 259 | collector-sdk | delivered | `core/collectors.py`, `cli/collector.py`, docs/tests (pre-existing, hardened) |
| 260 | aws-evidence-collector | delivered | AWS collector + tests (pre-existing, hardened) |
| 261 | forge-contracts | delivered | `forge_doctor_data/contracts` (spec chose in-repo package over separate dist) |
| 262 | ecosystem-conformance | partial | Contract + MCP + knowledge + golden conformance in `forge-gates`; external-ecosystem adapter tests limited |
| 263 | v1-release-candidate | not started | Release-candidate automation pending; version at 0.9.0 by design |
| 264 | v1-release | not started | Depends on 263 |

## Fixes uncovered by the new tests

- `contracts/models.py` — `HandoffBundle.from_dict`/`RemediationPlan`
  now normalize the emitted wire form (capabilities mapping, action
  objects, integer `contract_version`) instead of assuming structured
  objects; found by the handoff flow test.
- `project status --check` — trailing-newline-only diffs no longer
  report false drift.
- `docs/project-status.md` regenerated after every CLI surface change
  (inspect aliases, project command).

## Commits in this wave

- `2848b1a` metamorphic/mutation suite (P6)
- `b41c88a` integration flows + contract fix (P5)
- `510a4c7` fleet benchmark harness + measured curves (P11)
- `9907de3` versioned corpus manifest (256)
- Earlier: specs, `--stats`, `project status`, 0.9.0, governance/domain
  docs, `_v2` consolidation, MCP adapters, contracts, inspect aliases.

## Open items for the next wave

- Vendor real OSS slices into `golden/` (spec 256).
- Run `tools/benchmarks/fleet.py` at n=100/500/1000 and record budgets
  (spec 257) before claiming scale.
- Release-candidate pipeline (spec 263): wheel install smoke + supply
  chain sign-off → 1.0.0 (spec 264).
