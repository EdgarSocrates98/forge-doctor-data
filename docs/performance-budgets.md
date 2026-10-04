# Performance budgets

Performance is measured before it becomes a gate. Benchmarks must report
observations for:

- small, medium, and large scans;
- graph build and fleet merge;
- history read and semantic diff;
- MCP tool latency;
- cold, warm, and incremental scans;
- peak memory and entity/edge counts.

Budgets use a recorded baseline with a robust tolerance rather than a single
machine's absolute limit. A gate reports `unknown` when no baseline exists;
it does not invent a budget. Baselines are content-addressed and reviewed
alongside the benchmark run record.

Fleet scale targets are 10, 50, 100, 500, and 1000 repositories. Current
fixture validation is not evidence that the 500/1000 targets are achieved.

## Recorded runs

`tools/benchmarks/fleet.py` (seeded synthetic workspace, offline) —

| Run | n | files | cold p50/repo | warm mean/repo | wall | peak |
|-----|---|-------|---------------|----------------|------|------|
| 2025-12 | 10 | 30 | 495 ms | 671 ms | 13.7 s | 12.1 MB |
| 2025-12 | 50 | 150 | 427 ms | 583 ms | 56.5 s | — |

Scan time per repo is roughly flat (cold p50 ~430-500 ms) and wall time
scales linearly (~1.1 s/repo end-to-end) through n=50. The 100/500/1000
targets remain unproven; run the same harness before claiming them.
