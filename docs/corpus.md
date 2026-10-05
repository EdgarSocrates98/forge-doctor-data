# Validation corpus

`golden/` is the versioned regression corpus. `golden/manifest.json` is
the index: each entry vendors a repo slice under `<name>/repo/` and its
expected outputs under `<name>/expected/`.

## Provenance contract

Every manifest entry records:

- `origin` — `synthetic` (authored in-repo) or `real` (vendored from an
  upstream project);
- `url`, `commit`, `license` — required for `real` entries, `null` for
  synthetic ones;
- `shape` — one line describing the workload shape the slice covers.

Entries are vendored slices, never fetched at test time. A `real` entry
without `url`+`commit` is a manifest error, not a documentation gap.

## Review path for updates

1. Vendor the slice into `golden/<name>/repo/` (minimal files that keep
   the workload shape; strip secrets and large binaries).
2. Regenerate expected outputs via the golden update path
   (`core.golden.update_golden`) and review the diff like a code change.
3. Update the manifest entry — for `real` origins record the exact
   upstream commit and license.
4. Drift in expected findings is a reviewable diff, not a silent update.

## Metrics

`tools/golden_metrics.py` recomputes finding-level precision/recall for
every entry against its recorded ground truth and writes
`golden/metrics.json`. Snapshots are generated deterministically, so the
gate asserts P=R=1.0 — the report is what *proves* it, split by origin
(`real_only` vs `synthetic_only`) so the real-corpus claim is auditable.
`python tools/golden_metrics.py --check` fails when the file is stale.

## Current coverage

Eight synthetic entries cover authored workload shapes (Glue/EMR/DynamoDB/
Kafka-Iceberg/Lake Formation migrations and runtime topologies). Three
`real` entries vendor upstream OSS slices at pinned commits, each with
its LICENSE file:

- `jaffle-shop-dbt` — dbt-labs/jaffle-shop-classic, the canonical dbt
  example project (staging + marts + schema.yml + seeds)
- `airflow-example-dags` — apache/airflow 2.10.5, five official example
  DAGs
- `terraform-aws-vpc` — terraform-aws-modules/terraform-aws-vpc, a
  production-grade Terraform module

`golden/metrics.json` reports P=1.0 / R=1.0 on both the full corpus and
the real-only subset.
