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
| Contract conformance | `schema contracts`, `knowledge test` | JSON schemas + knowledge packs stay coherent |
| MCP conformance | `tests/integration/test_mcp_conformance.py` | Legacy + modern protocol adapters against the official SDK |
| Benchmarks | `bench` command, `tools/benchmarks/*.py` | Measured curves feed `docs/performance-budgets.md`; gates use recorded baselines |

## Adding a mutation case

Append to `_MUTATIONS` in `test_mutations.py`: baseline files, mutated
files, expected check ids. The test first asserts the expected ids are
absent on the baseline (guard against vacuous cases), then that they
appear after mutation. Ground each case in a real check - a mutation no
check covers is a finding to fix in the engine, not in the test.

## Performance gates

`tools/benchmarks/fleet.py --budget <file.json>` compares measured curves
against budget keys (`cold_ms_p50_max`, `cold_ms_mean_max`,
`warm_ms_mean_max`, `ms_per_repo_wall_max`, `peak_mb_max`). A key absent
from the budget reports `unknown` and is not gated - budgets are never
invented.
