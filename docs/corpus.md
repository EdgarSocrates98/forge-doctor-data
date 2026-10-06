# Validation corpus

`golden/` is the versioned regression corpus. `golden/manifest.json` is
the index: each entry vendors a repo slice under `<name>/repo/` and its
expected outputs under `<name>/expected/`. Real-OSS entries additionally
carry `ground_truth.json` — a human-declared truth record separate from
the generated snapshots.

## Provenance contract

Every manifest entry records:

- `origin` — `synthetic` (authored in-repo), `real-oss` (vendored from
  an upstream project at a pinned commit), or `adversarial`
  (deliberately-broken fixtures);
- `upstream_repository`, `upstream_url`, `commit_sha`, `license` —
  required for `real-oss` entries, `null` for synthetic ones;
- `vendored_files` — the exact files under `repo/` with per-file
  `sha256`, byte size, and `upstream_path`, making the slice
  tamper-evident;
- `domain` — the check domains the slice exercises;
- `shape`, `reason`, `expected_behavior` — what the workload looks like,
  why it is in the corpus, and what the engine should produce;
- `date_added` — when the slice entered the corpus.

Entries are vendored slices, never fetched at test time. A `real-oss`
entry without provenance is a manifest error, not a documentation gap.
Slice selection favours small, representative files over breadth: enough
evidence to exercise real analyzers and checks, nothing more.

## Ground truth vs generated snapshots

`expected/*.json` files are generated snapshots — they prove the engine
is deterministic. `ground_truth.json` is a human declaration — it proves
the engine is *honest*. Each real-oss slice declares five sets:

- `expected_findings` — check families that must fire (domain coverage);
- `forbidden_findings` — check families that must stay silent
  (cross-domain leakage guard; scoped families like `KFK`/`FLK`/`TRINO`
  must not fire on unrelated slices);
- `expected_entities` / `expected_edges` — graph domains, entity kinds,
  and relationship kinds the slice must produce;
- `expected_unknowns` — checks that must stay silent because the
  evidence cannot support the claim (e.g. broker topology from
  client-only code, or `ICE012` where catalog sub-keys are properties,
  not competing implementations).

`tests/unit/test_real_ground_truth.py` runs the engine live against
every real slice and asserts all five sets.

## Review path for updates

1. Vendor the slice into `golden/<name>/repo/` with
   `tools/vendor_golden.py` (minimal files that keep the workload shape;
   strip secrets and large binaries; the tool records provenance and
   the upstream LICENSE).
2. Scan the slice and review actual findings — real repos are a
   diagnostic surface. A finding the evidence cannot support is an
   engine bug to fix, not a fixture to adjust.
3. Regenerate expected outputs via the golden update path
   (`core.golden.update_golden`) and review the diff like a code change.
4. Write `ground_truth.json` declaring the five sets above.
5. Update the manifest entry — exact upstream commit, license, domains,
   and per-file hashes.
6. Regenerate `golden/metrics.json`. Drift in expected findings is a
   reviewable diff, not a silent update.

## Metrics

`tools/golden_metrics.py` recomputes finding-level precision/recall for
every entry against its recorded ground truth and writes
`golden/metrics.json`. Snapshots are generated deterministically, so the
gate asserts P=R=1.0 — the report is what *proves* it. The file splits:

- `aggregate` — the whole corpus;
- `real_only` / `synthetic_only` — by origin, so the real-corpus claim
  is auditable;
- `by_domain` (+ `precision_by_domain` / `recall_by_domain`) — per
  declared domain, so "works on Kafka/Flink/Trino/…" reads straight off
  the artifact;
- `total_entries` / `passed_entries` / `failed_entries`.

`python tools/golden_metrics.py --check` fails when the file is stale.

## Current coverage

Eight synthetic entries cover authored workload shapes (Glue/EMR/
DynamoDB/Kafka-Iceberg/Lake Formation migrations and runtime
topologies). Ten `real-oss` entries vendor upstream OSS slices at pinned
commits, each with its LICENSE file and byte-verified provenance:

| Entry | Upstream | Domain |
| --- | --- | --- |
| `jaffle-shop-dbt` | dbt-labs/jaffle-shop-classic | dbt |
| `airflow-example-dags` | apache/airflow 2.10.5 | airflow |
| `terraform-aws-vpc` | terraform-aws-modules/terraform-aws-vpc | terraform-aws |
| `spark-py-examples` | apache/spark | spark |
| `iceberg-spark-env` | databricks/docker-spark-iceberg | iceberg, spark |
| `kafka-python-clients` | confluentinc/confluent-kafka-python | kafka |
| `flink-pyflink-examples` | apache/flink | flink |
| `trino-server-dev-etc` | trinodb/trino | trino |
| `elasticsearch-terraform-module` | cloudposse/terraform-aws-elasticsearch | search, terraform-aws |
| `glue-terraform-example` | cloudposse/terraform-aws-glue | glue, terraform-aws |

`golden/metrics.json` reports P=1.0 / R=1.0 on the full corpus, the
real-only subset, and every declared domain.
