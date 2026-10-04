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
