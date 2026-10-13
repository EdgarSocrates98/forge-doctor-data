# v1.0 readiness scorecard

The claims v1.0 is allowed to make, each bound to a proof artifact and
the gate that keeps it true. A claim without an artifact is marketing;
a gate without a claim is overhead.

| Claim | Proof artifact | Gate |
|-------|----------------|------|
| I work on real repositories | `golden/` — 10 real-oss slices vendored at pinned commits (dbt, Airflow, Terraform/VPC, Spark, spark-iceberg, kafka clients, PyFlink, Trino, elasticsearch TF, glue TF); `golden/metrics.json` `real-oss` P=1.0/R=1.0 per domain | `golden run` in CI + `test_corpus_manifest.py` provenance rules + `golden_metrics --check` + `test_corpus_ground_truth.py` |
| I have a measured scale envelope | `docs/benchmarks/fleet-scan-n250.json` (p50/p95 + env block), `fleet-merge-n250-n500.json` — validated scan=250, merge=500 | `test_fleet_bench.py`, budget keys in `docs/benchmarks/fleet-budget.json`, scheduled `benchmarks.yml` |
| My contracts are stable | `docs/api-surface.json` (stability classes), `docs/schema-freeze.json` (digests of all 20 published schemas) | `test_public_api_freeze.py` + `api_surface --check` + `schema_freeze.py --check` in CI |
| My trust boundaries are tested | `test_mcp_boundary.py` (53), `test_plugin_boundary.py` (53), `test_hardening.py` (58) — hostile inputs, escapes, crashes, confinement | full suite + adversarial layer |
| My outputs are reproducible | `tools/env_manifest.py` per CI leg; deterministic `to_json`/snapshots; byte-identical determinism invariant in `test_mutations.py` + `test_whatif_hardening.py` | full CI matrix + golden snapshot equality |
| My ecosystem boundary is explicit | `forge_doctor_data.contracts` (zero engine imports, frozen `__all__`), `contracts conformance` CLI, `docs/forge-contracts.md` manifesto | `test_contract_boundaries.py`, `test_forge_contracts.py`, subprocess import-isolation tests |
| My handoff is bounded and interoperable | `HandoffBundle.bounded()` severity-first truncation recorded as `UnknownFact`; `x-*` extension namespaces round-trip | `test_hardening.py` §15, `test_forge_contracts.py` extension tests |
| My CI reproduces clean installs | deterministic Poetry bootstrap, manual dep cache, wheel-first smoke on 3 OSes | `ci.yml` static-analysis + unit-tests-{3.11,3.12,3.13} + smokes |
| Integration needs no coupling | `contracts conformance` validates any external payload; Forger receives `HandoffBundle` — routing/scheduling stays out | `test_conformance.py`, `test_handoff` flows |
| My release is reproducible + provenance-bound | `tools/release_candidate.py` artifact set (wheel+sdist, SBOM, SHA256SUMS, manifest, provenance, schemas, env-manifest) | `test_release_candidate.py`, dirty-tree refusal, SDE, digest re-verify |

## Readiness checklist (pre-tag 1.0.0)

Gates that must be green on the final tag commit:

- [ ] `pytest` full suite (unit + integration + adversarial + golden + lab)
- [ ] `ruff check . && ruff format --check .` and `mypy` strict
- [x] `forge-doctor-data contracts conformance --fixtures` - all 10 kinds valid
- [x] `python tools/api_surface.py --check` - no public-surface drift
- [x] `python tools/schema_freeze.py --check` - no wire-schema drift
- [x] `python tools/golden_metrics.py --check` - corpus metrics fresh
- [ ] `forge-doctor-data golden run` - all slices snapshot pass
- [ ] `forge-doctor-data lab run` + `knowledge test` + `project status --check`
- [x] `python tools/release_candidate.py` - dry-run artifact set complete
- [ ] `CHANGELOG.md` `[Unreleased]` content moved under `## [1.0.0]`
- [ ] `pyproject.toml` version bumped to `1.0.0` + `__init__.py` fallback
- [x] `docs/api-surface.json` regenerated post-bump (version is recorded)
- [ ] Human sign-off on `docs/api.md`, `docs/contracts.md`,
  `docs/deprecation.md`, `docs/v1-readiness.md`, `CHANGELOG.md`,
  `README.md`, `SECURITY.md`

(`[x]` = proven during `1.0.0-rc1` preparation; `[ ]` = re-verified on
the final tag or pending human sign-off.)

## Remaining blockers / honest gaps

- **Fleet beyond the envelope unproven** - recorded proof stops at
  n=250 (scan) / n=500 (merge); `docs/performance-budgets.md` states
  the unproven range explicitly.
- **No `fix` subcommand** - diagnostics only; transforms are post-1.0.
- **PyPI publish disabled** - `release.yml` `pypi` job waits on the
  maintainer enabling Trusted Publishing (flip `if: false`).
- **Plugin ecosystem still evolving** - SDK frozen; third-party plugin
  landscape not yet exercised at breadth.
- **What-if edge cases** - fixed change-target vocabulary; compound or
  out-of-vocabulary changes answer `unknown`, not guesses.
- **Windows/macOS depth** - full unit matrix is Ubuntu-only; other OSes
  get wheel-first smoke + CLI legs; heavy benchmarks run on the
  scheduled gate.
