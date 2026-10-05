# Consolidation Wave — v1 Readiness Run Record (specs 265–273 + sections 5–14)

Date: 2026-10-04 · Branch: `feat/consolidation-v1-readiness`
Base: `cb98730` (`forge-doctor-data 0.9.0`, main)
Program: `prompt_evo_consolidacao1.md` — TRUST > FEATURES, PROOF > BREADTH.

## Per-spec status

| Spec | Title | Status | Evidence |
|------|-------|--------|----------|
| 265 | ci-bootstrap-hardening | delivered | `da304ea` — deterministic Poetry bootstrap, manual venv cache, wheel-first smoke, `tools/env_manifest.py`, `test_hermetic_env.py` |
| 266 | contracts-v1-stabilization | delivered | `d5d54fa` — UnknownFact, x-* extensions, strict null semantics (explicit-null bug fixed), drift test |
| 267 | cross-doctor-conformance | delivered | `8d9218b` — `contracts/schemas.py` (10 kinds), wheel-bundled fixtures, `contracts conformance` CLI, subprocess isolation proof |
| 268 | real-oss-corpus | delivered | `3fbdd35` — jaffle-shop/airflow/terraform-aws-vpc at pinned commits + LICENSE, `golden_metrics.py` P=R=1.0 (corpus + real-only) |
| 269 | fleet-scale-100plus | delivered | `ed97124` — streaming `merge_repos` (no subgraph retention), scan n=100 / merge n=150 artifacts, budget keys |
| 270 | critical-path-coverage | delivered | `7c20aff` — `test_contract_mutations.py` 100% kill rate; failure-injection on conformance path |
| 271 | public-contract-freeze | delivered | `d7deed3` — `tools/api_surface.py` + `docs/api-surface.json`, stability classes, 13 MCP tools pinned |
| 272 | release-candidate-pipeline | delivered | `d221329` — `tools/release_candidate.py`: SHA256SUMS, SBOM, manifest, schema export, provenance; refuses stale/mismatched dist |
| 273 | v1-readiness | delivered | `5735717` — `docs/v1-readiness.md` scorecard + checklist + honest gaps; CHANGELOG sections |

## Sections 5–14 (cross-cutting)

| Section | Deliverable | Commit |
|---------|-------------|--------|
| 5 Shared vocabulary | `DataPlatformGraph` stays engine-side; contracts carry only the frozen universal set | `d5d54fa` |
| 6 Forger preparation | `core/forger.py::accept_request` — `{"kind":"scan"}` in → `HandoffBundle` out; no routing/scheduling | `46bb7c8` |
| 7 Context economy | `HandoffBundle.bounded()` — truncation recorded as `UnknownFact`s | `46bb7c8` |
| 8 Contract extensions | `x-forge-data` stamp on emissions; base vocabulary unpolluted | `46bb7c8` |
| 9 Performance & history | lazy/bounded history iteration, prune, deterministic ordering | `46bb7c8` |
| 10 Knowledge supply chain | `verify_pack` — provenance, staleness, dual pack layouts, cross-domain dependency links (iceberg→glue) | `46bb7c8` |
| 11 Plugin ecosystem | `test_plugin_conformance_proofs.py` — trust-gate-before-load (AST), no-mutation, no-network; isolation trust contract documented | `6b53d70` |
| 12 Security / supply chain | release-candidate SBOM + hashes + provenance; dep review via existing security workflow | `d221329` |
| 13 Docs-as-contract | `test_doc_examples.py` — every fenced `forge-doctor-data …` line resolves against the real click tree (commands, subcommands, flags; `_GraphGroup`/`history` dispatch honored); `tools/*.py` refs exist | `67e6ef8` |
| 14 Architectural drift | contracts→engine import ban + vendor-name ban (docstring-pruned AST) | `d5d54fa` |

## Notable defects caught by the new gates

- `contracts` explicit-null loss on `capabilities` key (Phase B).
- `isolation.py` worker `ep.load()` with no visible trust decision —
  resolved by documenting the caller-owned trust contract + pinning
  gate-before-invoke (section 11).
- Stale 0.7.0 artifacts in `dist/` — the release-candidate version
  gate refused them (Phase H).
- Domain-field false positives on the `<kind>/<domain>.json`
  knowledge-pack layout (section 10).
- Windows argv-length limit in the boundary subprocess test —
  payload moved to a temp file.

## Honest gaps (carried into v1-readiness.md)

- Fleet n=500/1000 unproven (recorded curve stops at 150/100).
- No `fix` subcommand — diagnostics only.
- PyPI publish disabled until Trusted Publishing is enabled.
- Real corpus = 3 slices; domain expansion is post-1.0 additive work.
