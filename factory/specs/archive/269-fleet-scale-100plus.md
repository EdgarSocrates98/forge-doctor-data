---
id: 269
title: Fleet Scale Proof — n=100+ benchmarks, budget keys, streaming merge
agent: claude
risk: high
verification:
  - python -m pytest tests/unit/test_fleet_bench.py tests/unit/test_workspace.py -x -q
  - python tools/benchmarks/fleet.py --mode scan --n 10
  - python tools/benchmarks/fleet.py --mode merge --n 10
---

# Consolidation Wave — Phase E (prompt_evo_consolidacao1 §Phase E)

Prove the workspace/fleet path scales past toy size, and keep the
merge memory-bound instead of retaining every subgraph.

## Acceptance Criteria

- `merge_repos` streams: per-repo subgraphs consumed and released —
  no `sub_graphs` retention list; results identical to pre-change
  (workspace tests).
- `tools/benchmarks/fleet.py` `--mode scan|merge` with seeded synthetic
  repos; records wall time, per-repo mean/p50, peak RSS.
- Scale evidence committed: `docs/benchmarks/fleet-scan-n100.json`
  (n=100, 300 files, cold ~433ms/repo) and
  `docs/benchmarks/fleet-merge-n150.json` (n=150, 903 entities, ~1.1MB
  peak — flat memory confirms streaming).
- Explicit budget keys in `docs/benchmarks/fleet-budget.json`;
  unknown budgets reported as unknown, never invented.
- Honest gap stated in `docs/performance-budgets.md`: n=500/1000
  unproven.

## Evidence

- Commit `ed97124` — streaming merge + n=150 proof + budget keys.
