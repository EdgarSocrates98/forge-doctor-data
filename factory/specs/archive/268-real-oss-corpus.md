---
id: 268
title: Real OSS Corpus — vendored slices with provenance + precision/recall proof
agent: claude
risk: high
verification:
  - forge-doctor-data golden run
  - python tools/golden_metrics.py --check
  - python -m pytest tests/unit/test_golden_metrics.py -x -q
---

# Consolidation Wave — Phase D (prompt_evo_consolidacao1 §Phase D)

Synthetic fixtures prove the mechanism; real repositories prove the
product. Vendor minimal real OSS slices — never whole repos — each
with upstream URL, exact commit, and license.

## Acceptance Criteria

- Real slices vendored (no test-time network):
  - `jaffle-shop-dbt` (dbt-labs/jaffle-shop-classic @ fd7bfaca, Apache-2.0)
  - `airflow-example-dags` (apache/airflow @ b93c3db6, Apache-2.0, selected DAGs + LICENSE)
  - `terraform-aws-vpc` (terraform-aws-modules @ b3abd6df, Apache-2.0)
- `golden/manifest.json` records provenance for every real entry
  (url, commit, license); synthetic entries declared as such.
- `tools/golden_metrics.py` computes corpus + real-only
  precision/recall against ground truth; `--check` gates staleness;
  `golden/metrics.json` is the recorded artifact.
- Deterministic snapshots regenerate identically; reviewable diffs.
- Metrics: corpus P=1.000 R=1.000, real-only P=1.000 R=1.000,
  11/11 snapshots pass.

## Evidence

- Commit `3fbdd35` — slices, provenance, metrics tool + tests.
