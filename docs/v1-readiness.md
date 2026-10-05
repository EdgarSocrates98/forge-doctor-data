# v1.0 readiness scorecard

The claims v1.0 is allowed to make, each bound to a proof artifact and
the gate that keeps it true. A claim without an artifact is marketing;
a gate without a claim is overhead.

| Claim | Proof artifact | Gate |
|-------|----------------|------|
| I work on real repositories | `golden/{jaffle-shop-dbt,airflow-example-dags,terraform-aws-vpc}` vendored at pinned commits; `golden/metrics.json` `real_only` P=1.0/R=1.0 | `golden run` in CI + `test_corpus_manifest.py` provenance rules + `golden_metrics --check` |
| I scale beyond toy workspaces | `docs/benchmarks/fleet-merge-n150.json` (merge n=150, ~1MB peak), `docs/benchmarks/fleet-scan-n100.json` | `test_fleet_bench.py`, budget keys in `docs/benchmarks/fleet-budget.json` |
| My contracts are stable | `docs/api-surface.json` (stability classes over api/sdk/contracts/MCP/CLI) | `test_public_api_freeze.py` + `api_surface --check` in CI |
| My outputs are reproducible | `tools/env_manifest.py` emitted per CI leg; deterministic `to_json`/snapshots; byte-identical determinism invariant in `test_mutations.py` | full CI matrix + golden snapshot equality |
| My ecosystem boundary is explicit | `forge_doctor_data.contracts` (zero engine imports, frozen `__all__`), `contracts conformance` CLI, canonical fixtures in the wheel | `test_contract_boundaries.py`, `test_conformance.py`, subprocess import-isolation tests |
| My CI reproduces clean installs | deterministic Poetry bootstrap, manual dep cache, wheel-first smoke on 3 OSes | `ci.yml` static-analysis + unit-tests-{3.11,3.12,3.13} + smokes |
| Integration needs no coupling | `contracts conformance` validates any external payload; Forger receives `HandoffBundle` - routing/scheduling stays out | `test_conformance.py`, `test_handoff` flows |

## Readiness checklist (pre-tag)

Gates that must be green on the release candidate commit:

- [ ] `pytest` full suite (unit + integration + adversarial + golden + lab)
- [ ] `ruff check . && ruff format --check .` and `mypy` strict
- [ ] `forge-doctor-data contracts conformance --fixtures` - all 10 kinds valid
- [ ] `python tools/api_surface.py --check` - no public-surface drift
- [ ] `python tools/golden_metrics.py --check` - corpus metrics fresh
- [ ] `forge-doctor-data golden run` - 11/11 snapshot pass
- [ ] `forge-doctor-data lab run` + `knowledge test` + `project status --check`
- [ ] `python tools/release_candidate.py` - dry-run artifact set complete
- [ ] `CHANGELOG.md` `[Unreleased]` content moved under `## [1.0.0]`
- [ ] `pyproject.toml` version bumped to `1.0.0` + `__init__.py` fallback
- [ ] `docs/api-surface.json` regenerated post-bump (version is recorded)
- [ ] Human sign-off on `docs/api.md` stability rules + `docs/deprecation.md`

## Remaining blockers / honest gaps

- **Fleet 500/1000 unproven** - recorded proof stops at n=150 (merge) /
  n=100 (scan). The same harness extends the curve; `docs/performance-budgets.md`
  states the unproven range explicitly.
- **No `fix` subcommand** - diagnostics only; transforms are post-1.0.
- **PyPI publish disabled** - `release.yml` `pypi` job waits on the
  maintainer enabling Trusted Publishing (flip `if: false`).
- **Real corpus depth** - 3 slices prove the mechanism; expanding domain
  coverage (e.g., a real Glue/Airflow hybrid estate) is additive post-1.0
  work, not a contract blocker.
