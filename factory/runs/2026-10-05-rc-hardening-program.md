# RC Hardening Program — run record

Date: 2026-10-05
Branch: `feat/rc-hardening-1.0`
Base: `9586dcb` (main, forge-doctor-data 0.9.0)
Program: `prompt_evo_rc_hardening.md` — trust, proof, boundary hardening,
real-world evidence, release discipline.

## Spec ledger

| spec | title | status | commit | evidence |
|------|-------|--------|--------|----------|
| 274 | rc-baseline-freeze | accepted | `9b3bdfe` | `docs/rc-policy.md`, `docs/rc-baseline.json`, `tools/rc_baseline.py`, `docs/api-surface.json` |
| 275 | real-oss-corpus-expansion | accepted | `dbe3084` | `golden/` 10 real slices, `manifest.json` provenance, `metrics.json` per-domain P/R |
| 276 | mcp-boundary-hardening | accepted | `deb7307` | `tests/unit/test_mcp_boundary.py`, `mcp_server.py` fixes |
| 277 | plugin-boundary-hardening | accepted | `a753748` | `tests/unit/test_plugin_boundary.py`, `isolation.py` + `runner.py` fixes |
| 278 | whatif-migration-hardening | accepted | `1121104` | `test_whatif_hardening.py`, `test_hardening.py` (58), 6 source fixes |
| 279 | scale-envelope-extension | accepted | `60d5cde` | `docs/benchmarks/fleet-{scan-n250,merge-n250-n500}.json`, `benchmarks.yml` |
| 280 | cross-doctor-contract-finalization | accepted | `baac258` | `docs/forge-contracts.md`, `test_forge_contracts.py` |
| 281 | rc-pipeline-finalization | accepted | `f94f161` | `release_candidate.py` gates, `schema_freeze.py`, `docs/schema-freeze.json` |
| 282 | 1.0.0-rc1-preparation | accepted | `f73cd42` | version `1.0.0rc1`, CHANGELOG section, `docs/releases/1.0.0-rc1.md` |
| 283 | post-rc-discipline | accepted | `9b3bdfe` | `docs/rc-policy.md` §3-§4 (P0-P3, allowed/forbidden, telemetry, compat rule) |
| 284 | 1.0.0-final-readiness | pending | — | `docs/v1-readiness.md` checklist; full-matrix re-verification + human sign-off on the final tag |

## Tests

- before: 2369 collected, ~80.8% coverage (program start)
- after: 2596 collected; coverage re-measured on final validation leg
- new test files: `test_mcp_boundary.py` (53), `test_plugin_boundary.py`
  (53), `test_whatif_hardening.py` (~25), `test_hardening.py` (58),
  `test_forge_contracts.py` (30), `test_corpus_manifest.py` +
  `test_corpus_ground_truth.py` (24), `test_schema_freeze.py` (7),
  plus freeze/bench/release expansions

## Engine fixes shipped (real-world findings)

- `ICE012` nested `spark.sql.catalog.<name>.<key>` treated as separate
  catalog implementations — FP on real spark-iceberg slice.
- `SRCH004` var-driven encryption attributes claimed "missing" — now
  resolves module-local variable defaults; unprovable → `unknown`.
- `ScanService` returned a plausible report for nonexistent roots —
  now `ScanRequestError` at the shared pipeline gate.
- MCP sandbox: `changes`/`manifest` path args were unconstrained;
  malformed `params`/`arguments` crashed instead of `-32602`;
  `load_pack_ref` traversal escaped the knowledge dir; deep JSON could
  kill the stdio loop.
- Plugin isolation: unbounded child stdout capture, unconfined file
  claims, unvalidated describe rows; runner crashed on non-CheckResult
  plugin output.
- `HandoffBundle.bounded()` truncated by list position, not severity;
  `agent_context` left stale `evidence_refs` after budget trimming.

## Known gaps (honest)

- Scan >250 / merge >500 unproven — stated, not claimed.
- Windows/macOS full unit matrix runs on Ubuntu only (smoke legs
  elsewhere); heavy benchmarks on scheduled gate.
- Plugin ecosystem breadth unexercised (SDK frozen, no third-party
  corpus).
- PyPI publishing manual-only pending maintainer Trusted Publishing
  setup.
- Human sign-off items per `docs/v1-readiness.md` remain open for the
  final tag.
