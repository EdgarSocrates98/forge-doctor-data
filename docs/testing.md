# Test strategy

The engine is deterministic and offline; every layer below runs without
network, credentials, or an LLM.

## Pyramid

| Layer | Where | What it proves |
|-------|-------|----------------|
| Unit | `tests/unit/` | Analyzers, checks, models, services in isolation |
| Integration flows | `tests/integration/test_flows.py` | CLI-to-CLI journeys: scan -> baseline -> diff, runtime -> history -> regression, workspace/fleet, handoff -> typed contract consumer |
| Metamorphic / mutation | `tests/integration/test_mutations.py` | A detrimental mutation must surface the expected check id; undetected mutations are coverage gaps. Includes a byte-identical determinism invariant |
| Golden corpus | `golden/`, `golden run` | Vendored repo slices vs recorded expected outputs; drift is a diff. Provenance lives in `golden/manifest.json` (see `docs/corpus.md`) |
| Forge Lab | `labs/`, `lab run` | Scenario expectations per domain |
| Contract conformance | `contracts conformance`, `tests/unit/test_conformance.py` | forge-contracts/1 payloads validated twice (JSON Schema + strict model decode); kind auto-detection; bundled canonical fixtures |
| Contract mutation gate | `tests/unit/test_contract_mutations.py` | Every single-field mutation of a valid payload (delete/null/type-flip per required key, all 10 kinds) must be killed by the gate - asserted at 100% kill rate over >=100 mutations |
| Boundary / drift | `tests/unit/test_contract_boundaries.py` | The contracts package never imports engine internals, stays domain-neutral, exports only the frozen vocabulary |
| MCP conformance | `tests/unit/test_mcp_conformance.py` | Legacy + modern protocol adapters against the official SDK |
| MCP boundary | `tests/unit/test_mcp_boundary.py` | Trust-boundary contract: every path-shaped tool argument confined to `--root`, symlink escapes refused, malformed envelopes -> `-32602`, pathological payloads -> `-32700` and the stdio loop survives, resource URIs segment-validated against traversal, plugins off unless the host opts in |
| Plugin boundary | `tests/unit/test_plugin_boundary.py` + `test_plugin_conformance_proofs.py` | Pre-load trust gate in both execution modes, no id shadowing, crash containment, bounded child output (streaming cap + timeout kill), sanitized isolated results |
| Benchmarks | `bench` command, `tools/benchmarks/*.py` | Measured curves feed `docs/performance-budgets.md`; gates use recorded baselines |

## Adding a mutation case

Append to `_MUTATIONS` in `test_mutations.py`: baseline files, mutated
files, expected check ids. The test first asserts the expected ids are
absent on the baseline (guard against vacuous cases), then that they
appear after mutation. Ground each case in a real check - a mutation no
check covers is a finding to fix in the engine, not in the test.

## Critical-path coverage

The forge-contracts/1 critical path (models + version + schemas +
conformance) is held at near-total coverage by its dedicated suites:

| Module | Coverage (measured) |
|--------|---------------------|
| `contracts/models.py` | 98% |
| `contracts/version.py` | 100% |
| `contracts/schemas.py` | 100% |
| `core/conformance.py` | 92% |

Measured with:
`pytest tests/unit/test_contracts*.py tests/unit/test_conformance.py --cov=forge_doctor_data.contracts --cov=forge_doctor_data.core.conformance`
(97% total). Failure injection (`test_contract_mutations.py`) covers the
hostile-input edge cases coverage alone can't prove: truncated JSON,
scalar payloads, wrong/unknown contract families, deep nesting, corrupt
fleet manifests - all fail honestly without tracebacks.

## Performance gates

`tools/benchmarks/fleet.py --budget <file.json>` compares measured curves
against budget keys (`cold_ms_p50_max`, `cold_ms_mean_max`,
`warm_ms_mean_max`, `ms_per_repo_wall_max`, `peak_mb_max`). A key absent
from the budget reports `unknown` and is not gated - budgets are never
invented.
