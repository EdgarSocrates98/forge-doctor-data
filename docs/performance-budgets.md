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

Fleet scale targets are 10, 50, 100, 500, and 1000 repositories. The
100+ target is proven by the recorded runs below (streaming merge, spec
269). The 500/1000 targets remain unproven; run the same harness before
claiming them.

## Recorded runs

`tools/benchmarks/fleet.py` (seeded synthetic workspace, offline) —

| Run | n | files | cold p50/repo | warm mean/repo | wall | peak |
|-----|---|-------|---------------|----------------|------|------|
| 2025-12 | 10 | 30 | 495 ms | 671 ms | 13.7 s | 12.1 MB |
| 2025-12 | 50 | 150 | 427 ms | 583 ms | 56.5 s | — |
| 2026-03 | 100 | 300 | 342 ms | 335 ms | 76.7 s | 12.1 MB |

Run artifacts: `docs/benchmarks/fleet-scan-n100.json`,
`docs/benchmarks/fleet-merge-n150.json`. Budget keys gate against
`docs/benchmarks/fleet-budget.json` (recorded baseline x ~3x tolerance).

`tools/benchmarks/fleet.py --merge` (fleet-manifest merge path) —

| Run | n | entities | edges | merge | peak |
|-----|---|----------|-------|-------|------|
| 2026-03 | 10 | 63 | 41 | 3.3 s | 11.0 MB |
| 2026-03 | 50 | 303 | 201 | 3.5 s | 0.7 MB |
| 2026-03 | 100 | 603 | 401 | 6.2 s | 0.9 MB |
| 2026-03 | 150 | 903 | 601 | 11.8 s | 1.1 MB |

Scan time per repo is roughly flat (cold p50 ~340-500 ms) and wall time
scales ~linearly (~0.8-1.1 s/repo end-to-end) through n=100. Merge peak
memory stays ~1 MB independent of n - the streaming merge releases each
repo sub-graph within its iteration, so resident memory is O(merged
graph + largest repo), not O(sum of sub-graphs).
