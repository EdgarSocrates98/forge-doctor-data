# `forge-doctor-data` command reference

Generated from the real CLI parser by `doc_inventory.py` + `doc_reference.py`. Do not hand-edit generated sections — write between `keep:start`/`keep:end` markers. Status vocabulary: `available` unless marked otherwise.

## Groups

- [`advise`](#advise) — 1 command(s)
- [`agent`](#agent) — 5 command(s)
- [`airflow`](#airflow) — 2 command(s)
- [`analytical`](#analytical) — 2 command(s)
- [`architecture`](#architecture) — 2 command(s)
- [`athena`](#athena) — 3 command(s)
- [`aws`](#aws) — 1 command(s)
- [`bench`](#bench) — 2 command(s)
- [`bigquery`](#bigquery) — 2 command(s)
- [`cache`](#cache) — 2 command(s)
- [`capabilities`](#capabilities) — 4 command(s)
- [`catalog`](#catalog) — 2 command(s)
- [`checks`](#checks) — 1 command(s)
- [`ci`](#ci) — 1 command(s)
- [`cloud`](#cloud) — 2 command(s)
- [`collector`](#collector) — 2 command(s)
- [`compatibility`](#compatibility) — 1 command(s)
- [`contract`](#contract) — 2 command(s)
- [`contracts`](#contracts) — 5 command(s)
- [`controlm`](#controlm) — 2 command(s)
- [`data-model`](#data-model) — 2 command(s)
- [`databricks`](#databricks) — 3 command(s)
- [`dbt`](#dbt) — 2 command(s)
- [`delta`](#delta) — 4 command(s)
- [`dependencies`](#dependencies) — 1 command(s)
- [`diagnose`](#diagnose) — 1 command(s)
- [`diff`](#diff) — 1 command(s)
- [`docker`](#docker) — 1 command(s)
- [`doctor`](#doctor) — 1 command(s)
- [`dynamodb`](#dynamodb) — 7 command(s)
- [`emr`](#emr) — 3 command(s)
- [`explain`](#explain) — 1 command(s)
- [`export`](#export) — 1 command(s)
- [`fix`](#fix) — 1 command(s)
- [`fleet`](#fleet) — 6 command(s)
- [`flink`](#flink) — 3 command(s)
- [`git`](#git) — 1 command(s)
- [`glue`](#glue) — 1 command(s)
- [`golden`](#golden) — 4 command(s)
- [`graph`](#graph) — 5 command(s)
- [`history`](#history) — 3 command(s)
- [`iac`](#iac) — 1 command(s)
- [`iceberg`](#iceberg) — 6 command(s)
- [`incident`](#incident) — 3 command(s)
- [`info`](#info) — 1 command(s)
- [`init`](#init) — 1 command(s)
- [`inspect`](#inspect) — 35 command(s)
- [`install`](#install) — 7 command(s)
- [`kafka`](#kafka) — 3 command(s)
- [`kinesis`](#kinesis) — 3 command(s)
- [`knowledge`](#knowledge) — 9 command(s)
- [`lab`](#lab) — 6 command(s)
- [`lakeformation`](#lakeformation) — 7 command(s)
- [`lambda`](#lambda) — 3 command(s)
- [`lineage`](#lineage) — 1 command(s)
- [`lsp`](#lsp) — 1 command(s)
- [`mcp`](#mcp) — 1 command(s)
- [`migrate`](#migrate) — 4 command(s)
- [`neptune`](#neptune) — 8 command(s)
- [`ontology`](#ontology) — 5 command(s)
- [`optimize`](#optimize) — 3 command(s)
- [`parquet`](#parquet) — 2 command(s)
- [`platform`](#platform) — 4 command(s)
- [`plugins`](#plugins) — 8 command(s)
- [`policy`](#policy) — 5 command(s)
- [`project`](#project) — 2 command(s)
- [`python`](#python) — 1 command(s)
- [`quality`](#quality) — 2 command(s)
- [`redshift`](#redshift) — 2 command(s)
- [`reliability`](#reliability) — 3 command(s)
- [`remediate`](#remediate) — 1 command(s)
- [`repo`](#repo) — 1 command(s)
- [`root-cause`](#root-cause) — 1 command(s)
- [`runtime`](#runtime) — 13 command(s)
- [`sbom`](#sbom) — 1 command(s)
- [`scan`](#scan) — 1 command(s)
- [`schema`](#schema) — 3 command(s)
- [`search`](#search) — 2 command(s)
- [`snowflake`](#snowflake) — 2 command(s)
- [`spark`](#spark) — 4 command(s)
- [`stepfunctions`](#stepfunctions) — 2 command(s)
- [`streaming`](#streaming) — 5 command(s)
- [`suppressions`](#suppressions) — 1 command(s)
- [`terraform`](#terraform) — 2 command(s)
- [`trace`](#trace) — 1 command(s)
- [`trino`](#trino) — 2 command(s)
- [`twin`](#twin) — 8 command(s)
- [`version`](#version) — 1 command(s)
- [`what-if`](#what-if) — 1 command(s)
- [`workspace`](#workspace) — 4 command(s)

## advise

### `advise`

Rank findings into a cited action list.

Score = severity + confidence + cluster + fix-safety + plan + policy
+ blast radius; every row cites fingerprints and entity ids.
Advisory only - apply via ``fix``/``remediate`` commands.

**Syntax**

```text
forge-doctor-data advise [path] [fmt] [top]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `fmt` | no | — | text|json |
| `top` | no | — | Show only the top N. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## agent

### `agent`

Deterministic, budget-aware agent context.

**Syntax**

```text
forge-doctor-data agent
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `agent context`

Emit summary-first context constrained by an approximate token budget.

**Syntax**

```text
forge-doctor-data agent context [path] [budget] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory. |
| `budget` | no | — | — |
| `as_json` | no | — | Emit JSON (default). |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `agent delta`

Emit added/removed/unchanged finding fingerprints.

**Syntax**

```text
forge-doctor-data agent delta [path] [since] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory. |
| `since` | no | — | — |
| `as_json` | no | — | Emit JSON (default). |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `agent evidence`

Resolve one lazy evidence reference.

**Syntax**

```text
forge-doctor-data agent evidence <reference> [path] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `reference` | yes | — | finding:<fingerprint> or entity:<id>. |
| `path` | no | — | Project directory. |
| `as_json` | no | — | Emit JSON (default). |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `agent manifest`

Emit compact domains, risks, capabilities, and evidence references.

**Syntax**

```text
forge-doctor-data agent manifest [path] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory. |
| `as_json` | no | — | Emit JSON (default). |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## airflow

### `airflow`

Airflow intelligence: inspect DAGs, tasks, sensors.

**Syntax**

```text
forge-doctor-data airflow
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `airflow inspect`

Summarize the project's Airflow surface from the semantic model.

**Syntax**

```text
forge-doctor-data airflow inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## analytical

### `analytical`

Real-time OLAP engines: ClickHouse / Pinot / Druid inspection.

**Syntax**

```text
forge-doctor-data analytical
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `analytical inspect`

Print the analytical-engine model: tables, engines, schemas, observed.

**Syntax**

```text
forge-doctor-data analytical inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## architecture

### `architecture`

Architecture drift detection.

**Syntax**

```text
forge-doctor-data architecture
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `architecture drift`

Compare the platform contract against code, IaC, and runtime.

**Syntax**

```text
forge-doctor-data architecture drift [path] [contract] [runtime] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |
| `contract` | no | — | Contract file (default: auto-detect). |
| `runtime` | no | — | Exported runtime artifact(s). |
| `as_json` | no | — | Emit JSON. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## athena

### `athena`

Athena workgroup/query intelligence.

**Syntax**

```text
forge-doctor-data athena
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `athena findings`

**Syntax**

```text
forge-doctor-data athena findings [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `athena inspect`

Workgroups, catalogs, named queries, SQL ops, boto3 evidence.

**Syntax**

```text
forge-doctor-data athena inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## aws

### `aws`

Run only aws checks.

**Syntax**

```text
forge-doctor-data aws [path] [ignore] [fmt] [quiet] [fail_on] [verbose] [baseline] [save_baseline] [output] [no_color] [new_only] [no_plugins] [files] [profile] [emit] [show_root] [cache] [stats]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `ignore` | no | — | Suppress a check id. |
| `fmt` | no | — | text|json|html|sarif|agent |
| `quiet` | no | — | Only problems. |
| `fail_on` | no | — | Lowest severity that fails: error|warning. |
| `verbose` | no | — | Internal detail. |
| `baseline` | no | — | Compare against a baseline file or a named baseline in .forge-doctor-data/baselines/<name>.json. |
| `save_baseline` | no | — | Write results to a baseline file or a named baseline in .forge-doctor-data/baselines/<name>.json. |
| `output` | no | — | Write output to a file. |
| `no_color` | no | — | Disable ANSI colors. |
| `new_only` | no | — | Show only findings new vs --baseline. |
| `no_plugins` | no | — | Skip external plugin loading. |
| `files` | no | — | Report findings for these files only. |
| `profile` | no | — | Severity policy: default|strict|security|spark-performance|glue-migration|production. |
| `emit` | no | — | Extra output: FMT or FMT:PATH (repeatable). One may target stdout. |
| `show_root` | no | — | Include the absolute project root in JSON output. |
| `cache` | no | — | Reuse per-file analysis facts (user cache dir; off by default in CI). |
| `stats` | no | — | Scan stats (files, timings, cache, memory) to stderr. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## bench

### `bench`

Performance & scale benchmark.

**Syntax**

```text
forge-doctor-data bench
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `bench run`

Run the benchmark on a project or a generated synthetic corpus.

**Syntax**

```text
forge-doctor-data bench run [path] [files] [seed] [budget] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root (omit to generate a synthetic one). |
| `files` | no | — | Synthetic corpus size. |
| `seed` | no | — | Generator seed. |
| `budget` | no | — | JSON budget thresholds. |
| `as_json` | no | — | Machine-readable output. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## bigquery

### `bigquery`

BigQuery intelligence: inspect the vendor model.

**Syntax**

```text
forge-doctor-data bigquery
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `bigquery inspect`

Print the BigQuery model: datasets, relations, slots, exports.

**Syntax**

```text
forge-doctor-data bigquery inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## cache

### `cache`

Inspect or clear the incremental analysis cache. Bare: Show cache statistics for the project.

**Syntax**

```text
forge-doctor-data cache [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `cache clean`

Delete the incremental analysis cache.

**Syntax**

```text
forge-doctor-data cache clean [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## capabilities

### `capabilities`

Platform capability registry.

**Syntax**

```text
forge-doctor-data capabilities
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `capabilities explain`

Evaluate one capability in context and show status + provenance.

**Syntax**

```text
forge-doctor-data capabilities explain <platform> <capability> [version] [variant] [attribute] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `platform` | yes | — | Platform key (dynamodb, neptune...). |
| `capability` | yes | — | Capability id (DYNAMODB_STREAMS...). |
| `version` | no | — | Platform version. |
| `variant` | no | — | Mode variant (MREC|MRSC...). |
| `attribute` | no | — | Extra fact as key=value. |
| `as_json` | no | — | Machine-readable output. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `capabilities graph`

Render the capability → evidence subgraph for a project.

Capabilities observed in the project evaluate against the versions
its entities declare; each edge carries the deciding pack entry,
matched when-clause, and (for unknowns) the missing evidence.

**Syntax**

```text
forge-doctor-data capabilities graph [path] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |
| `as_json` | no | — | Machine-readable output. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `capabilities list`

List every capability fact by platform with its headline status.

``--json`` emits ``{platform: {capability: status}}``; with
``--provenance`` each row becomes ``{"status", "provenance"}``
carrying the deciding pack entry, matched when-clause, and source.

**Syntax**

```text
forge-doctor-data capabilities list [as_json] [provenance]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `as_json` | no | — | Machine-readable output. |
| `provenance` | no | — | Emit rows with provenance objects. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## catalog

### `catalog`

Metadata catalogs: DataHub/OpenMetadata/Glue/Unity declared estate.

**Syntax**

```text
forge-doctor-data catalog
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `catalog inspect`

Print the declared catalog: datasets, owners, lineage, recipes.

**Syntax**

```text
forge-doctor-data catalog inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## checks

### `checks`

List every registered check id, category and title.

**Syntax**

```text
forge-doctor-data checks
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## ci

### `ci`

Run only ci checks.

**Syntax**

```text
forge-doctor-data ci [path] [ignore] [fmt] [quiet] [fail_on] [verbose] [baseline] [save_baseline] [output] [no_color] [new_only] [no_plugins] [files] [profile] [emit] [show_root] [cache] [stats]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `ignore` | no | — | Suppress a check id. |
| `fmt` | no | — | text|json|html|sarif|agent |
| `quiet` | no | — | Only problems. |
| `fail_on` | no | — | Lowest severity that fails: error|warning. |
| `verbose` | no | — | Internal detail. |
| `baseline` | no | — | Compare against a baseline file or a named baseline in .forge-doctor-data/baselines/<name>.json. |
| `save_baseline` | no | — | Write results to a baseline file or a named baseline in .forge-doctor-data/baselines/<name>.json. |
| `output` | no | — | Write output to a file. |
| `no_color` | no | — | Disable ANSI colors. |
| `new_only` | no | — | Show only findings new vs --baseline. |
| `no_plugins` | no | — | Skip external plugin loading. |
| `files` | no | — | Report findings for these files only. |
| `profile` | no | — | Severity policy: default|strict|security|spark-performance|glue-migration|production. |
| `emit` | no | — | Extra output: FMT or FMT:PATH (repeatable). One may target stdout. |
| `show_root` | no | — | Include the absolute project root in JSON output. |
| `cache` | no | — | Reuse per-file analysis facts (user cache dir; off by default in CI). |
| `stats` | no | — | Scan stats (files, timings, cache, memory) to stderr. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## cloud

### `cloud`

Multi-cloud abstractions: vendor-neutral view over detected services.

**Syntax**

```text
forge-doctor-data cloud
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `cloud inspect`

Print the abstraction view: services by kind, cloud, parity gaps.

**Syntax**

```text
forge-doctor-data cloud inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## collector

### `collector`

Validate normalized evidence bundles.

**Syntax**

```text
forge-doctor-data collector
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `collector validate`

Validate a bundle before offline analysis consumes it.

**Syntax**

```text
forge-doctor-data collector validate <path> [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | yes | — | Normalized evidence bundle JSON. |
| `as_json` | no | — | — |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## compatibility

### `compatibility`

Detect runtimes and show Glue migration risks (knowledge packs).

**Syntax**

```text
forge-doctor-data compatibility [path] [source] [target]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `source` | no | — | Source Glue version. |
| `target` | no | — | Target Glue version. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## contract

### `contract`

Platform contract files.

**Syntax**

```text
forge-doctor-data contract
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `contract validate`

Validate a platform contract's structure and schema version.

**Syntax**

```text
forge-doctor-data contract validate <contract> [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `contract` | yes | — | platform-contract.yml path. |
| `as_json` | no | — | Emit JSON. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## contracts

### `contracts`

Published artifact contracts (verify handoff bundles, schemas).

**Syntax**

```text
forge-doctor-data contracts
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `contracts conformance`

Check a payload against forge-contracts/1 (spec 267).

Validates the payload twice: against the published JSON Schema for its
kind, and through the strict ``from_dict`` model decode. Exit code 1 on
any violation. Other Forge products (The Forger, Spark Forge, agents)
use this to prove they speak the same wire contract.

**Syntax**

```text
forge-doctor-data contracts conformance [payload] [kind] [fixtures] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `payload` | no | — | JSON payload to check, '-' for stdin, or '--fixtures'. |
| `kind` | no | — | Contract kind; auto-detected when omitted. |
| `fixtures` | no | — | Check all bundled canonical fixtures. |
| `as_json` | no | — | Emit the verdict as JSON. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `contracts list`

List the published contract names (see `schema contracts <name>` for a dump).

**Syntax**

```text
forge-doctor-data contracts list
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `contracts schema`

Dump the published forge-contracts/1 JSON Schemas.

**Syntax**

```text
forge-doctor-data contracts schema [name]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `name` | no | — | forge-contracts/1 kind; omit to list all. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `contracts verify`

Validate a JSON artifact against a published contract (stdin or file).

``forge-doctor-data export --format handoff`` output validates against
``handoff-bundle``; other Forge tools use this in their own tests.

**Syntax**

```text
forge-doctor-data contracts verify [bundle] [contract]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `bundle` | no | — | JSON artifact to validate, or '-' for stdin. |
| `contract` | no | — | Contract name (see `contracts list`). |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## controlm

### `controlm`

Control-M intelligence: inspect workflows-as-code.

**Syntax**

```text
forge-doctor-data controlm
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `controlm inspect`

Summarize the project's Control-M surface from the semantic model.

**Syntax**

```text
forge-doctor-data controlm inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## data-model

### `data-model`

Cross-domain access-style inspection.

**Syntax**

```text
forge-doctor-data data-model
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `data-model inspect`

Breakdown of observed access styles across data domains.

**Syntax**

```text
forge-doctor-data data-model inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## databricks

### `databricks`

Databricks workspace/job/UC intelligence.

**Syntax**

```text
forge-doctor-data databricks
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `databricks findings`

**Syntax**

```text
forge-doctor-data databricks findings [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `databricks inspect`

Jobs, clusters, warehouses, UC objects, pipelines, bundles.

**Syntax**

```text
forge-doctor-data databricks inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## dbt

### `dbt`

dbt intelligence: inspect the transformation model.

**Syntax**

```text
forge-doctor-data dbt
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `dbt inspect`

Print the dbt model: models, sources, tests, manifest coverage.

**Syntax**

```text
forge-doctor-data dbt inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## delta

### `delta`

Delta Lake feature and ops intelligence.

**Syntax**

```text
forge-doctor-data delta
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `delta features`

Detected Delta features mapped to protocol requirements.

**Syntax**

```text
forge-doctor-data delta features [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `delta findings`

**Syntax**

```text
forge-doctor-data delta findings [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `delta inspect`

Tables, ops (merge/optimize/vacuum), features, protocol.

**Syntax**

```text
forge-doctor-data delta inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## dependencies

### `dependencies`

Run only dependencies checks.

**Syntax**

```text
forge-doctor-data dependencies [path] [ignore] [fmt] [quiet] [fail_on] [verbose] [baseline] [save_baseline] [output] [no_color] [new_only] [no_plugins] [files] [profile] [emit] [show_root] [cache] [stats]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `ignore` | no | — | Suppress a check id. |
| `fmt` | no | — | text|json|html|sarif|agent |
| `quiet` | no | — | Only problems. |
| `fail_on` | no | — | Lowest severity that fails: error|warning. |
| `verbose` | no | — | Internal detail. |
| `baseline` | no | — | Compare against a baseline file or a named baseline in .forge-doctor-data/baselines/<name>.json. |
| `save_baseline` | no | — | Write results to a baseline file or a named baseline in .forge-doctor-data/baselines/<name>.json. |
| `output` | no | — | Write output to a file. |
| `no_color` | no | — | Disable ANSI colors. |
| `new_only` | no | — | Show only findings new vs --baseline. |
| `no_plugins` | no | — | Skip external plugin loading. |
| `files` | no | — | Report findings for these files only. |
| `profile` | no | — | Severity policy: default|strict|security|spark-performance|glue-migration|production. |
| `emit` | no | — | Extra output: FMT or FMT:PATH (repeatable). One may target stdout. |
| `show_root` | no | — | Include the absolute project root in JSON output. |
| `cache` | no | — | Reuse per-file analysis facts (user cache dir; off by default in CI). |
| `stats` | no | — | Scan stats (files, timings, cache, memory) to stderr. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## diagnose

### `diagnose`

Fingerprint log errors against known signatures (deterministic, offline).

**Syntax**

```text
forge-doctor-data diagnose <source> [fmt] [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `source` | yes | — | Log file path, or '-' to read stdin. |
| `fmt` | no | — | text|json |
| `path` | no | — | Project root for repo-evidence correlations. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## diff

### `diff`

Diff findings: NEW in <new> vs <old>, or in a 'base...head' git range.

**Syntax**

```text
forge-doctor-data diff <old> [new] [path] [semantic] [runtime_impact] [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `old` | yes | — | Older report JSON, git ref, or 'base...head' range. |
| `new` | no | — | Newer report JSON or git ref. |
| `path` | no | — | Repo used to resolve git refs. |
| `semantic` | no | — | Entity-level diff + blast radius (git refs only). |
| `runtime_impact` | no | — | Correlate the semantic diff's changes with recorded runtime history (implies --semantic). |
| `fmt` | no | — | text|json (semantic diff only) |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## docker

### `docker`

Run only docker checks.

**Syntax**

```text
forge-doctor-data docker [path] [ignore] [fmt] [quiet] [fail_on] [verbose] [baseline] [save_baseline] [output] [no_color] [new_only] [no_plugins] [files] [profile] [emit] [show_root] [cache] [stats]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `ignore` | no | — | Suppress a check id. |
| `fmt` | no | — | text|json|html|sarif|agent |
| `quiet` | no | — | Only problems. |
| `fail_on` | no | — | Lowest severity that fails: error|warning. |
| `verbose` | no | — | Internal detail. |
| `baseline` | no | — | Compare against a baseline file or a named baseline in .forge-doctor-data/baselines/<name>.json. |
| `save_baseline` | no | — | Write results to a baseline file or a named baseline in .forge-doctor-data/baselines/<name>.json. |
| `output` | no | — | Write output to a file. |
| `no_color` | no | — | Disable ANSI colors. |
| `new_only` | no | — | Show only findings new vs --baseline. |
| `no_plugins` | no | — | Skip external plugin loading. |
| `files` | no | — | Report findings for these files only. |
| `profile` | no | — | Severity policy: default|strict|security|spark-performance|glue-migration|production. |
| `emit` | no | — | Extra output: FMT or FMT:PATH (repeatable). One may target stdout. |
| `show_root` | no | — | Include the absolute project root in JSON output. |
| `cache` | no | — | Reuse per-file analysis facts (user cache dir; off by default in CI). |
| `stats` | no | — | Scan stats (files, timings, cache, memory) to stderr. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## doctor

### `doctor`

Self-check: config, plugins, cache dir, git, environment health.

**Syntax**

```text
forge-doctor-data doctor [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## dynamodb

### `dynamodb`

DynamoDB intelligence.

**Syntax**

```text
forge-doctor-data dynamodb
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `dynamodb access-patterns`

List observed access operations per table.

**Syntax**

```text
forge-doctor-data dynamodb access-patterns [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `dynamodb capacity`

Billing-mode inventory - structure only, no cost math.

**Syntax**

```text
forge-doctor-data dynamodb capacity [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `dynamodb global-tables`

Global-table modes (MREC/MRSC), regions, transaction semantics.

**Syntax**

```text
forge-doctor-data dynamodb global-tables [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `dynamodb indexes`

GSI/LSI inventory vs observed IndexName usage.

**Syntax**

```text
forge-doctor-data dynamodb indexes [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `dynamodb inspect`

Summarize tables, keys, capacity mode, streams, global tables.

**Syntax**

```text
forge-doctor-data dynamodb inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `dynamodb streams`

Stream configuration and detected consumers.

**Syntax**

```text
forge-doctor-data dynamodb streams [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## emr

### `emr`

EMR deep intelligence (EC2/Serverless/EKS).

**Syntax**

```text
forge-doctor-data emr
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `emr findings`

**Syntax**

```text
forge-doctor-data emr findings [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `emr inspect`

Clusters, serverless apps, EKS virtual clusters, releases, steps.

**Syntax**

```text
forge-doctor-data emr inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## explain

### `explain`

Explain what a check looks for, when it is OK, and how to fix it.

**Syntax**

```text
forge-doctor-data explain <check_id> [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `check_id` | yes | — | Check id, e.g. SPARK001. |
| `as_json` | no | — | Emit rule metadata as JSON. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## export

### `export`

Emit a portable handoff bundle: findings + graph + capabilities + plans.

**Syntax**

```text
forge-doctor-data export [path] [fmt] [output]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `fmt` | no | — | Bundle format: handoff |
| `output` | no | — | Write to file (default: stdout). |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## fix

### `fix`

Preview (or apply) deterministic safe fixes for findings.

**Syntax**

```text
forge-doctor-data fix [path] [apply_] [fix_class] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |
| `apply_` | no | — | Write SAFE transforms to disk. |
| `fix_class` | no | — | Apply tier: 'safe' (default) or 'review'. |
| `as_json` | no | — | Emit JSON audit output. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## fleet

### `fleet`

Fleet/estate intelligence across many repos. Bare: Fleet/estate intelligence over a manifest of repositories.

**Syntax**

```text
forge-doctor-data fleet
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `fleet inspect`

Estate census: repos, merged platform graph, cross-repo links.

**Syntax**

```text
forge-doctor-data fleet inspect <spec>
```

| argument/flag | required | default | description |
|---|---|---|---|
| `spec` | yes | — | Fleet manifest (yaml/json) or a directory. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `fleet portfolio`

Portfolio view: platforms, workloads, duplication, complexity —
facts only, no health score.

**Syntax**

```text
forge-doctor-data fleet portfolio <spec> [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `spec` | yes | — | Fleet manifest (yaml/json) or a directory. |
| `fmt` | no | — | text|json |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `fleet query`

Deterministic estate queries over the merged fleet graph.

**Syntax**

```text
forge-doctor-data fleet query <spec> <what> [target] [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `spec` | yes | — | Fleet manifest (yaml/json) or a directory. |
| `what` | yes | — | runtimes|capability|dependents|findings |
| `target` | no | — | capability id, entity glob, or check id |
| `fmt` | no | — | text|json |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `fleet regressions`

Fleet-level regression aggregation: same regression family across
workloads/repos (e.g. after a platform upgrade).

**Syntax**

```text
forge-doctor-data fleet regressions <spec> [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `spec` | yes | — | Fleet manifest (yaml/json) or a directory. |
| `fmt` | no | — | text|json |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `fleet report`

Estate census + per-repo findings roll-up (built-in checks only).

**Syntax**

```text
forge-doctor-data fleet report <spec> [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `spec` | yes | — | Fleet manifest (yaml/json) or a directory. |
| `fmt` | no | — | text|json |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## flink

### `flink`

Flink deep intelligence.

**Syntax**

```text
forge-doctor-data flink
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `flink findings`

**Syntax**

```text
forge-doctor-data flink findings [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `flink inspect`

Jobs, sources, keyed state, windows, timers, checkpoints, sinks.

**Syntax**

```text
forge-doctor-data flink inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## git

### `git`

Run only git checks.

**Syntax**

```text
forge-doctor-data git [path] [ignore] [fmt] [quiet] [fail_on] [verbose] [baseline] [save_baseline] [output] [no_color] [new_only] [no_plugins] [files] [profile] [emit] [show_root] [cache] [stats]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `ignore` | no | — | Suppress a check id. |
| `fmt` | no | — | text|json|html|sarif|agent |
| `quiet` | no | — | Only problems. |
| `fail_on` | no | — | Lowest severity that fails: error|warning. |
| `verbose` | no | — | Internal detail. |
| `baseline` | no | — | Compare against a baseline file or a named baseline in .forge-doctor-data/baselines/<name>.json. |
| `save_baseline` | no | — | Write results to a baseline file or a named baseline in .forge-doctor-data/baselines/<name>.json. |
| `output` | no | — | Write output to a file. |
| `no_color` | no | — | Disable ANSI colors. |
| `new_only` | no | — | Show only findings new vs --baseline. |
| `no_plugins` | no | — | Skip external plugin loading. |
| `files` | no | — | Report findings for these files only. |
| `profile` | no | — | Severity policy: default|strict|security|spark-performance|glue-migration|production. |
| `emit` | no | — | Extra output: FMT or FMT:PATH (repeatable). One may target stdout. |
| `show_root` | no | — | Include the absolute project root in JSON output. |
| `cache` | no | — | Reuse per-file analysis facts (user cache dir; off by default in CI). |
| `stats` | no | — | Scan stats (files, timings, cache, memory) to stderr. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## glue

### `glue`

Run only glue checks.

**Syntax**

```text
forge-doctor-data glue [path] [ignore] [fmt] [quiet] [fail_on] [verbose] [baseline] [save_baseline] [output] [no_color] [new_only] [no_plugins] [files] [profile] [emit] [show_root] [cache] [stats]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `ignore` | no | — | Suppress a check id. |
| `fmt` | no | — | text|json|html|sarif|agent |
| `quiet` | no | — | Only problems. |
| `fail_on` | no | — | Lowest severity that fails: error|warning. |
| `verbose` | no | — | Internal detail. |
| `baseline` | no | — | Compare against a baseline file or a named baseline in .forge-doctor-data/baselines/<name>.json. |
| `save_baseline` | no | — | Write results to a baseline file or a named baseline in .forge-doctor-data/baselines/<name>.json. |
| `output` | no | — | Write output to a file. |
| `no_color` | no | — | Disable ANSI colors. |
| `new_only` | no | — | Show only findings new vs --baseline. |
| `no_plugins` | no | — | Skip external plugin loading. |
| `files` | no | — | Report findings for these files only. |
| `profile` | no | — | Severity policy: default|strict|security|spark-performance|glue-migration|production. |
| `emit` | no | — | Extra output: FMT or FMT:PATH (repeatable). One may target stdout. |
| `show_root` | no | — | Include the absolute project root in JSON output. |
| `cache` | no | — | Reuse per-file analysis facts (user cache dir; off by default in CI). |
| `stats` | no | — | Scan stats (files, timings, cache, memory) to stderr. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## golden

### `golden`

Golden repositories - snapshot regression suites.

**Syntax**

```text
forge-doctor-data golden
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `golden list`

List golden repositories.

**Syntax**

```text
forge-doctor-data golden list [root]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `root` | no | — | Golden corpus root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `golden run`

Diff current engine output against stored snapshots.

**Syntax**

```text
forge-doctor-data golden run [name] [root] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `name` | no | — | Repo name (default: all). |
| `root` | no | — | Golden corpus root. |
| `as_json` | no | — | Machine-readable output. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `golden update`

Regenerate snapshots — review the diff before committing.

**Syntax**

```text
forge-doctor-data golden update [name] [root]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `name` | no | — | Repo name (default: all). |
| `root` | no | — | Golden corpus root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## graph

### `graph`

Graph intelligence.

**Syntax**

```text
forge-doctor-data graph
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `graph inspect`

Summarize detected graph workloads, languages, and paradigms.

**Syntax**

```text
forge-doctor-data graph inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `graph project`

Project Intelligence Graph: jobs, datasets, infra, orchestrators.

**Syntax**

```text
forge-doctor-data graph project [path] [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |
| `fmt` | no | — | json|dot|mermaid |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `graph schema`

Show the vertex/edge schema reconstructed from static evidence.

**Syntax**

```text
forge-doctor-data graph schema [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `graph traversals`

List traversal inventory with per-traversal shape summary.

**Syntax**

```text
forge-doctor-data graph traversals [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## history

### `history`

Recorded scan snapshots: list, diff, trend. Bare: List recorded snapshots (scan --record).

**Syntax**

```text
forge-doctor-data history [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `history diff`

Diff two snapshots: new/resolved findings, entity + capability + drift deltas.

**Syntax**

```text
forge-doctor-data history diff [path] [a] [b] [last] [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |
| `a` | no | — | Snapshot name or index. |
| `b` | no | — | Snapshot name or index. |
| `last` | no | — | Diff the two latest snapshots. |
| `fmt` | no | — | text|json |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `history trend`

Per-category finding counts + entity counts across the series.

**Syntax**

```text
forge-doctor-data history trend [path] [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |
| `fmt` | no | — | text|json |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## iac

### `iac`

Run only iac checks.

**Syntax**

```text
forge-doctor-data iac [path] [ignore] [fmt] [quiet] [fail_on] [verbose] [baseline] [save_baseline] [output] [no_color] [new_only] [no_plugins] [files] [profile] [emit] [show_root] [cache] [stats]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `ignore` | no | — | Suppress a check id. |
| `fmt` | no | — | text|json|html|sarif|agent |
| `quiet` | no | — | Only problems. |
| `fail_on` | no | — | Lowest severity that fails: error|warning. |
| `verbose` | no | — | Internal detail. |
| `baseline` | no | — | Compare against a baseline file or a named baseline in .forge-doctor-data/baselines/<name>.json. |
| `save_baseline` | no | — | Write results to a baseline file or a named baseline in .forge-doctor-data/baselines/<name>.json. |
| `output` | no | — | Write output to a file. |
| `no_color` | no | — | Disable ANSI colors. |
| `new_only` | no | — | Show only findings new vs --baseline. |
| `no_plugins` | no | — | Skip external plugin loading. |
| `files` | no | — | Report findings for these files only. |
| `profile` | no | — | Severity policy: default|strict|security|spark-performance|glue-migration|production. |
| `emit` | no | — | Extra output: FMT or FMT:PATH (repeatable). One may target stdout. |
| `show_root` | no | — | Include the absolute project root in JSON output. |
| `cache` | no | — | Reuse per-file analysis facts (user cache dir; off by default in CI). |
| `stats` | no | — | Scan stats (files, timings, cache, memory) to stderr. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## iceberg

### `iceberg`

Iceberg intelligence: inspect, maintenance, compatibility.

**Syntax**

```text
forge-doctor-data iceberg
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `iceberg compatibility`

Cross detected runtimes with the Iceberg compatibility pack.

**Syntax**

```text
forge-doctor-data iceberg compatibility [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `iceberg files`

Static small-file risk posture (repartition/coalesce near writes).

**Syntax**

```text
forge-doctor-data iceberg files [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `iceberg inspect`

Summarize the project's Iceberg surface from the semantic model.

**Syntax**

```text
forge-doctor-data iceberg inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `iceberg maintenance`

Maintenance posture: which Iceberg housekeeping ops exist in code.

**Syntax**

```text
forge-doctor-data iceberg maintenance [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `iceberg merge`

Reconstruct every detected MERGE statement from the semantic model.

**Syntax**

```text
forge-doctor-data iceberg merge [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## incident

### `incident`

Dependency-aware incident intelligence (offline).

**Syntax**

```text
forge-doctor-data incident
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `incident explain`

Narrate one incident's evidence path, causes and unknowns.

**Syntax**

```text
forge-doctor-data incident explain <incident_id> [events] [root] [window_minutes]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `incident_id` | yes | — | Incident id from inspect. |
| `events` | no | — | JSON file of change events. |
| `root` | no | — | Project root holding .forge-doctor-data/. |
| `window_minutes` | no | — | Incident grouping/correlation window. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `incident inspect`

Group co-occurring regression episodes into incident windows.

**Syntax**

```text
forge-doctor-data incident inspect [events] [root] [window_minutes] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `events` | no | — | JSON file of change events. |
| `root` | no | — | Project root holding .forge-doctor-data/. |
| `window_minutes` | no | — | Incident grouping/correlation window. |
| `as_json` | no | — | json output |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## info

### `info`

Quick project stats - files, languages, tooling - no checks run.

**Syntax**

```text
forge-doctor-data info [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## init

### `init`

Scaffold a new Python project (pyproject, .gitignore, README, src/, tests/).

**Syntax**

```text
forge-doctor-data init [path] [name] [force]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `name` | no | — | Project name. |
| `force` | no | — | Overwrite existing files. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## inspect

### `inspect`

Domain inspection: `inspect <domain> [path]` (alias of `<domain> inspect`).

**Syntax**

```text
forge-doctor-data inspect
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect airflow`

Alias of `airflow inspect`. Summarize the project's Airflow surface from the semantic model.

**Syntax**

```text
forge-doctor-data inspect airflow [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect analytical`

Alias of `analytical inspect`. Print the analytical-engine model: tables, engines, schemas, observed.

**Syntax**

```text
forge-doctor-data inspect analytical [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect athena`

Alias of `athena inspect`. Workgroups, catalogs, named queries, SQL ops, boto3 evidence.

**Syntax**

```text
forge-doctor-data inspect athena [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect bigquery`

Alias of `bigquery inspect`. Print the BigQuery model: datasets, relations, slots, exports.

**Syntax**

```text
forge-doctor-data inspect bigquery [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect catalog`

Alias of `catalog inspect`. Print the declared catalog: datasets, owners, lineage, recipes.

**Syntax**

```text
forge-doctor-data inspect catalog [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect cloud`

Alias of `cloud inspect`. Print the abstraction view: services by kind, cloud, parity gaps.

**Syntax**

```text
forge-doctor-data inspect cloud [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect controlm`

Alias of `controlm inspect`. Summarize the project's Control-M surface from the semantic model.

**Syntax**

```text
forge-doctor-data inspect controlm [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect data-model`

Alias of `data-model inspect`. Breakdown of observed access styles across data domains.

**Syntax**

```text
forge-doctor-data inspect data-model [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect databricks`

Alias of `databricks inspect`. Jobs, clusters, warehouses, UC objects, pipelines, bundles.

**Syntax**

```text
forge-doctor-data inspect databricks [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect dbt`

Alias of `dbt inspect`. Print the dbt model: models, sources, tests, manifest coverage.

**Syntax**

```text
forge-doctor-data inspect dbt [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect delta`

Alias of `delta inspect`. Tables, ops (merge/optimize/vacuum), features, protocol.

**Syntax**

```text
forge-doctor-data inspect delta [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect dynamodb`

Alias of `dynamodb inspect`. Summarize tables, keys, capacity mode, streams, global tables.

**Syntax**

```text
forge-doctor-data inspect dynamodb [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect emr`

Alias of `emr inspect`. Clusters, serverless apps, EKS virtual clusters, releases, steps.

**Syntax**

```text
forge-doctor-data inspect emr [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect flink`

Alias of `flink inspect`. Jobs, sources, keyed state, windows, timers, checkpoints, sinks.

**Syntax**

```text
forge-doctor-data inspect flink [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect graph`

Alias of `graph inspect`. Summarize detected graph workloads, languages, and paradigms.

**Syntax**

```text
forge-doctor-data inspect graph [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect iceberg`

Alias of `iceberg inspect`. Summarize the project's Iceberg surface from the semantic model.

**Syntax**

```text
forge-doctor-data inspect iceberg [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect incident`

Alias of `incident inspect`. Group co-occurring regression episodes into incident windows.

**Syntax**

```text
forge-doctor-data inspect incident [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect kafka`

Alias of `kafka inspect`. MSK clusters, topics, consumer groups, options, security.

**Syntax**

```text
forge-doctor-data inspect kafka [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect kinesis`

Alias of `kinesis inspect`. Streams, shards, consumers, EFO, retention, flink apps.

**Syntax**

```text
forge-doctor-data inspect kinesis [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect lakeformation`

Alias of `lakeformation inspect`. Census: databases, tables, locations, tags, filters, links, shares.

**Syntax**

```text
forge-doctor-data inspect lakeformation [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect lambda`

Alias of `lambda inspect`. Functions, runtimes, triggers, destinations, idempotency evidence.

**Syntax**

```text
forge-doctor-data inspect lambda [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect neptune`

Alias of `neptune inspect`. Clusters, instances, endpoints, languages, product split.

**Syntax**

```text
forge-doctor-data inspect neptune [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect optimize`

Alias of `optimize inspect`. Multi-objective opportunities with guardrails + tradeoffs.

**Syntax**

```text
forge-doctor-data inspect optimize [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect parquet`

Alias of `parquet inspect`. Summarize the project's Parquet surface from the semantic model.

**Syntax**

```text
forge-doctor-data inspect parquet [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect quality`

Alias of `quality inspect`. Print declared suites, coverage map, and gate wiring.

**Syntax**

```text
forge-doctor-data inspect quality [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect redshift`

Alias of `redshift inspect`. Print the Redshift model: compute, relations, WLM, exports.

**Syntax**

```text
forge-doctor-data inspect redshift [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect search`

Alias of `search inspect`. Print the search model: indices/templates, policies, pipelines, domains.

**Syntax**

```text
forge-doctor-data inspect search [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect snowflake`

Alias of `snowflake inspect`. Print the Snowflake model: warehouses, objects, exports, copies.

**Syntax**

```text
forge-doctor-data inspect snowflake [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect stepfunctions`

Alias of `stepfunctions inspect`. Summarize Step Functions definitions from the semantic model.

**Syntax**

```text
forge-doctor-data inspect stepfunctions [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect streaming`

Alias of `streaming inspect`. Summarize streaming queries from the semantic model.

**Syntax**

```text
forge-doctor-data inspect streaming [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect terraform`

Alias of `terraform inspect`. Summarize the project's Terraform surface from the semantic model.

**Syntax**

```text
forge-doctor-data inspect terraform [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect trino`

Alias of `trino inspect`. Print the Trino model: catalogs, coordinator flags, SQL refs.

**Syntax**

```text
forge-doctor-data inspect trino [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect twin`

Alias of `twin inspect`. Twin summary + invariant report. Exit 1 on hard violations.

**Syntax**

```text
forge-doctor-data inspect twin [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect workspace`

Alias of `workspace inspect`. Build the WorkspaceModel: repos, merged platform graph, cross-repo links.

**Syntax**

```text
forge-doctor-data inspect workspace [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## install

### `install`

Install Forge Doctor Data into a project, workspace or the user home; manage the lifecycle (status, doctor, repair, update, uninstall).

**Syntax**

```text
forge-doctor-data install [scope] [host] [profile] [root] [yes] [dry_run]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `scope` | no | — | project|workspace|user. |
| `host` | no | — | claude|devin|codex|copilot|all. |
| `profile` | no | — | minimal|recommended|full. |
| `root` | no | — | Target root (default: VCS root or cwd). |
| `yes` | no | — | Explicit approval; without it only --dry-run is allowed. |
| `dry_run` | no | — | Plan only — writes nothing. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `install doctor`

Run installation health checks (ledger, MCP availability).

**Syntax**

```text
forge-doctor-data install doctor [scope] [root]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `scope` | no | — | project|workspace|user. |
| `root` | no | — | Target root (default: VCS root or cwd). |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `install mcp-verify`

Handshake the configured MCP server (PASS/BLOCKED/FAIL).

**Syntax**

```text
forge-doctor-data install mcp-verify
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `install repair`

Restore missing managed assets; user-modified content is kept.

**Syntax**

```text
forge-doctor-data install repair [scope] [root] [dry_run]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `scope` | no | — | project|workspace|user. |
| `root` | no | — | Target root (default: VCS root or cwd). |
| `dry_run` | no | — | Plan only — writes nothing. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `install status`

Report drift/health of the resolved installation.

**Syntax**

```text
forge-doctor-data install status [scope] [root]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `scope` | no | — | project|workspace|user. |
| `root` | no | — | Target root (default: VCS root or cwd). |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `install uninstall`

Remove ledger-owned assets only; user content is preserved.

**Syntax**

```text
forge-doctor-data install uninstall [scope] [root] [purge] [dry_run]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `scope` | no | — | project|workspace|user. |
| `root` | no | — | Target root (default: VCS root or cwd). |
| `purge` | no | — | Also remove the forge state dir. |
| `dry_run` | no | — | Plan only — writes nothing. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `install update`

Upgrade the bootstrapped runtime from its registered checkout.

**Syntax**

```text
forge-doctor-data install update [to] [repo] [dry_run]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `to` | no | — | Pin a version (never 'latest'). |
| `repo` | no | — | Checkout to upgrade from. |
| `dry_run` | no | — | Plan only — writes nothing. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## kafka

### `kafka`

Kafka/MSK deep intelligence.

**Syntax**

```text
forge-doctor-data kafka
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `kafka findings`

**Syntax**

```text
forge-doctor-data kafka findings [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `kafka inspect`

MSK clusters, topics, consumer groups, options, security.

**Syntax**

```text
forge-doctor-data kafka inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## kinesis

### `kinesis`

Kinesis deep intelligence.

**Syntax**

```text
forge-doctor-data kinesis
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `kinesis findings`

**Syntax**

```text
forge-doctor-data kinesis findings [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `kinesis inspect`

Streams, shards, consumers, EFO, retention, flink apps.

**Syntax**

```text
forge-doctor-data kinesis inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## knowledge

### `knowledge`

Knowledge-pack provenance. Bare: List all bundled knowledge packs with provenance.

**Syntax**

```text
forge-doctor-data knowledge
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `knowledge audit`

Classify packs as fresh, stale, expired, invalid_source, or unverified.

**Syntax**

```text
forge-doctor-data knowledge audit [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `as_json` | no | — | — |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `knowledge diff`

Semantic pack diff: entries added/removed/changed (not text diff).

**Syntax**

```text
forge-doctor-data knowledge diff <a> <b> [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `a` | yes | — | Pack ref: <domain>/<name> or a JSON path. |
| `b` | yes | — | Pack ref: <domain>/<name> or a JSON path. |
| `as_json` | no | — | — |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `knowledge info`

Show provenance detail for one domain's packs.

**Syntax**

```text
forge-doctor-data knowledge info <domain>
```

| argument/flag | required | default | description |
|---|---|---|---|
| `domain` | yes | — | Pack domain (glue, spark, errors...). |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `knowledge list`

Alias for the default listing.

**Syntax**

```text
forge-doctor-data knowledge list
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `knowledge new`

Scaffold a new knowledge pack with provenance fields + examples.

**Syntax**

```text
forge-doctor-data knowledge new <domain> [kind] [directory]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `domain` | yes | — | Pack domain (e.g. snowflake). |
| `kind` | no | — | versions|errors|capabilities|compatibility |
| `directory` | no | — | Knowledge root (default: bundled). |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `knowledge publish`

Publish checklist: freshness fields valid, conformance clean.

**Syntax**

```text
forge-doctor-data knowledge publish <domain> [bump] [directory] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `domain` | yes | — | Pack domain to validate for publish. |
| `bump` | no | — | Rewrite pack_version/verified_at. |
| `directory` | no | — | Knowledge root (default: bundled). |
| `as_json` | no | — | — |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `knowledge test`

Pack conformance suite: structure, regexes, examples, capabilities.

**Syntax**

```text
forge-doctor-data knowledge test [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `as_json` | no | — | — |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `knowledge verify`

Validate structure + flag packs stale (>90d since verified_at).

**Syntax**

```text
forge-doctor-data knowledge verify
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## lab

### `lab`

Forge Lab - reproducible scenarios with ground truth.

**Syntax**

```text
forge-doctor-data lab
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `lab experiment`

Apply a named hypothesis to a scenario copy and compare findings.

With --before/--after, compares two exported artifact bundles on
declared metrics instead (ExperimentPlan v2: verdicts SUPPORTED /
NOT_SUPPORTED / INCONCLUSIVE / CONSTRAINT_VIOLATED).

Never mutates the fixture: the scenario is copied to a temp dir,
transformed, rescanned hermetically, and reported as
improved | regressed | neutral with reasons.

**Syntax**

```text
forge-doctor-data lab experiment <scenario> [hypothesis] [labs] [before] [after] [expect] [protect] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `scenario` | yes | — | Scenario name or fixture directory. |
| `hypothesis` | no | — | Named transform to apply. |
| `labs` | no | — | Labs root directory. |
| `before` | no | — | Baseline artifact bundle dir. |
| `after` | no | — | Changed artifact bundle dir. |
| `expect` | no | — | Expected effect, e.g. 'scan_bytes:decrease:0.5'. |
| `protect` | no | — | Protected constraint, e.g. 'freshness_seconds:<=:60'. |
| `as_json` | no | — | Machine-readable output. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `lab list`

List discovered scenarios.

**Syntax**

```text
forge-doctor-data lab list [labs]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `labs` | no | — | Labs root directory. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `lab metrics`

Precision/recall/FP rates and coverage per domain + total.

**Syntax**

```text
forge-doctor-data lab metrics [labs] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `labs` | no | — | Labs root directory. |
| `as_json` | no | — | Machine-readable output. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `lab report`

Alias for `lab run` over every scenario (summary view).

**Syntax**

```text
forge-doctor-data lab report [labs] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `labs` | no | — | Labs root directory. |
| `as_json` | no | — | Machine-readable output. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `lab run`

Run scenario(s) and compare engine output to ground truth.

**Syntax**

```text
forge-doctor-data lab run [scenario] [labs] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `scenario` | no | — | Scenario name (default: all). |
| `labs` | no | — | Labs root directory. |
| `as_json` | no | — | Machine-readable output. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## lakeformation

### `lakeformation`

Lake Formation governance intelligence.

**Syntax**

```text
forge-doctor-data lakeformation
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `lakeformation compatibility`

Engine x FGAC/FTA capability report (knowledge-pack driven).

**Syntax**

```text
forge-doctor-data lakeformation compatibility [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `lakeformation cross-account`

Producer/consumer view: external accounts, RAM shares, links.

**Syntax**

```text
forge-doctor-data lakeformation cross-account [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `lakeformation findings`

Run LF### checks against the project.

**Syntax**

```text
forge-doctor-data lakeformation findings [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `lakeformation graph`

Governance graph view: principal -> resource edges.

**Syntax**

```text
forge-doctor-data lakeformation graph [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `lakeformation inspect`

Census: databases, tables, locations, tags, filters, links, shares.

**Syntax**

```text
forge-doctor-data lakeformation inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `lakeformation permissions`

Grant table: principal x permissions x resource.

**Syntax**

```text
forge-doctor-data lakeformation permissions [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## lambda

### `lambda`

Lambda function/trigger intelligence.

**Syntax**

```text
forge-doctor-data lambda
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `lambda findings`

**Syntax**

```text
forge-doctor-data lambda findings [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `lambda inspect`

Functions, runtimes, triggers, destinations, idempotency evidence.

**Syntax**

```text
forge-doctor-data lambda inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## lineage

### `lineage`

Static lineage: which jobs read/write which datasets.

**Syntax**

```text
forge-doctor-data lineage [path] [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `fmt` | no | — | text|json|dot|mermaid|openlineage |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## lsp

### `lsp`

Start a stdio LSP server (requires the optional 'lsp' extra).

**Syntax**

```text
forge-doctor-data lsp
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## mcp

### `mcp`

Start a zero-dep MCP (JSON-RPC stdio) server for agent integrations.

**Syntax**

```text
forge-doctor-data mcp [root]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `root` | no | — | Sandbox all tool path arguments to this directory tree. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## migrate

### `migrate`

Migration intelligence.

**Syntax**

```text
forge-doctor-data migrate
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `migrate explain`

Explain why each service mapped the way it did (spec 234).

Per concept: logical concept, mapping/lossiness, capability gaps the
target pack cannot satisfy, missing evidence, and the source-side
facts that anchored the mapping.

**Syntax**

```text
forge-doctor-data migrate explain [path] [source] [target] [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |
| `source` | no | — | Source platform (snowflake|redshift|…) |
| `target` | no | — | Target platform (bigquery|snowflake|…) |
| `fmt` | no | — | text|json |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `migrate glue`

Glue migration report: knowledge changes + this project's real signals.

**Syntax**

```text
forge-doctor-data migrate glue [path] [source] [target] [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `source` | no | — | Source Glue version. |
| `target` | no | — | Target Glue version. |
| `fmt` | no | — | text|json |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `migrate plan`

Enumerate migration plans; --from/--to build a cross-platform plan.

**Syntax**

```text
forge-doctor-data migrate plan [path] [source] [target] [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |
| `source` | no | — | Source platform (snowflake|redshift|…) |
| `target` | no | — | Target platform (bigquery|snowflake|…) |
| `fmt` | no | — | text|json |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## neptune

### `neptune`

Neptune Database + Analytics intelligence.

**Syntax**

```text
forge-doctor-data neptune
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `neptune analyze-explain`

Alias of `explain` (spec 179 names both entry points).

**Syntax**

```text
forge-doctor-data neptune analyze-explain <file>
```

| argument/flag | required | default | description |
|---|---|---|---|
| `file` | yes | — | Exported explain/profile artifact. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `neptune compatibility`

Query-language vs graph-paradigm compatibility via registry.

**Syntax**

```text
forge-doctor-data neptune compatibility [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `neptune explain`

Analyze a user-supplied explain/profile file (offline).

**Syntax**

```text
forge-doctor-data neptune explain <file>
```

| argument/flag | required | default | description |
|---|---|---|---|
| `file` | yes | — | Exported explain/profile artifact. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `neptune ingest`

Bulk-loader usage and ingestion-relevant config.

**Syntax**

```text
forge-doctor-data neptune ingest [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `neptune inspect`

Clusters, instances, endpoints, languages, product split.

**Syntax**

```text
forge-doctor-data neptune inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `neptune queries`

Per-query shape inventory (language, selectivity, bounds).

**Syntax**

```text
forge-doctor-data neptune queries [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `neptune schema`

Graph schema facts (labels, endpoints) seen by Neptune queries.

**Syntax**

```text
forge-doctor-data neptune schema [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## ontology

### `ontology`

Canonical platform vocabulary (entity/rel kinds, planes, domains). Bare: Print the canonical vocabulary (entity kinds, rel kinds, evidence

**Syntax**

```text
forge-doctor-data ontology [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `fmt` | no | — | text|json |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `ontology access-patterns`

Data-access patterns the ontology distinguishes.

**Syntax**

```text
forge-doctor-data ontology access-patterns [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `as_json` | no | — | — |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `ontology platform`

Platform implementations mapped onto vendor-neutral kinds (spec 230).

**Syntax**

```text
forge-doctor-data ontology platform [name] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `name` | no | — | Platform id/alias for detail (omit to list all). |
| `as_json` | no | — | — |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `ontology validate`

Validate a project's platform graph against the ontology vocabulary.

Reports entities whose free-text producer domain is outside the
vocabulary; enum-constrained fields (kind, rel kind, evidence plane)
cannot drift by construction.

**Syntax**

```text
forge-doctor-data ontology validate <path>
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | yes | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `ontology workloads`

Workload intents and the platform kinds that can serve them.

**Syntax**

```text
forge-doctor-data ontology workloads [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `as_json` | no | — | — |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## optimize

### `optimize`

Optimization candidates + multi-objective opportunities. Bare: Enumerate optimization candidates (v1) when no subcommand given.

**Syntax**

```text
forge-doctor-data optimize [path] [fmt] [top]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `fmt` | no | — | text|json |
| `top` | no | — | Show only the top N. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `optimize explain`

Full detail for one opportunity: effects, tradeoffs, guardrails.

**Syntax**

```text
forge-doctor-data optimize explain <opp_id> [path] [artifact] [adapter]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `opp_id` | yes | — | Opportunity id (OPP-####). |
| `path` | no | — | Project directory to scan. |
| `artifact` | no | — | Exported runtime artifact for perf/cost evidence. |
| `adapter` | no | — | — |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `optimize inspect`

Multi-objective opportunities with guardrails + tradeoffs.

**Syntax**

```text
forge-doctor-data optimize inspect [path] [artifact] [adapter] [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `artifact` | no | — | Exported runtime artifact for perf/cost evidence. |
| `adapter` | no | — | — |
| `fmt` | no | — | — |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## parquet

### `parquet`

Parquet intelligence: inspect.

**Syntax**

```text
forge-doctor-data parquet
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `parquet inspect`

Summarize the project's Parquet surface from the semantic model.

**Syntax**

```text
forge-doctor-data parquet inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## platform

### `platform`

Canonical platform graph.

**Syntax**

```text
forge-doctor-data platform
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `platform blast-radius`

Entities impacted by a change to ``query`` (semantic direction).

**Syntax**

```text
forge-doctor-data platform blast-radius <query> [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `query` | yes | — | Entity id or substring. |
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `platform findings`

Cross-domain platform findings (PLAT### rules).

**Syntax**

```text
forge-doctor-data platform findings [path] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |
| `as_json` | no | — | Emit JSON. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `platform graph`

Entity/relationship census of the canonical platform graph.

**Syntax**

```text
forge-doctor-data platform graph [path] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |
| `as_json` | no | — | Emit JSON. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## plugins

### `plugins`

Inspect and validate external plugins. Bare: List built-in categories and discovered external plugins.

**Syntax**

```text
forge-doctor-data plugins
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `plugins doctor`

Per-plugin health: entry point resolves, api_version supported.

**Syntax**

```text
forge-doctor-data plugins doctor
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `plugins init`

Scaffold a plugin package (pyproject + check + test) under dest/name.

**Syntax**

```text
forge-doctor-data plugins init <name> [dest]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `name` | yes | — | Distribution name, e.g. forge-doctor-data-snowflake. |
| `dest` | no | — | Parent directory. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `plugins install`

Install a plugin via pipx inject (or pip), then validate loading.

**Syntax**

```text
forge-doctor-data plugins install <dist> [dry_run]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `dist` | yes | — | Distribution, e.g. forge-doctor-data-snowflake. |
| `dry_run` | no | — | Print the command only. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `plugins list`

List installed plugins with API version and load/trust status.

**Syntax**

```text
forge-doctor-data plugins list
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `plugins lock`

Pin every installed plugin's content digest to .forge-doctor-data/plugins.lock.

**Syntax**

```text
forge-doctor-data plugins lock [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `plugins validate`

Fail when any installed plugin is incompatible or unloadable.

**Syntax**

```text
forge-doctor-data plugins validate
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `plugins verify`

Verify installed plugins against .forge-doctor-data/plugins.lock.

**Syntax**

```text
forge-doctor-data plugins verify [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## policy

### `policy`

Organization policy packs.

**Syntax**

```text
forge-doctor-data policy
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `policy eval`

Evaluate policy packs and print violations (exit 1 on errors/violations).

**Syntax**

```text
forge-doctor-data policy eval [path] [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |
| `fmt` | no | — | text|json |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `policy list`

List discovered policy packs and their rules.

**Syntax**

```text
forge-doctor-data policy list [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `policy report`

Compliance report: packs, violations by rule, suppression audit.

**Syntax**

```text
forge-doctor-data policy report [path] [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |
| `fmt` | no | — | text|json |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `policy validate`

Lint a policy pack file: schema, duplicate ids, regexes, severities.

**Syntax**

```text
forge-doctor-data policy validate <pack>
```

| argument/flag | required | default | description |
|---|---|---|---|
| `pack` | yes | — | Policy pack file to validate. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## project

### `project`

Project self-inspection: generated status and doc-drift checks.

**Syntax**

```text
forge-doctor-data project
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `project status`

Deterministic project status from source registries.

Same inputs → same bytes: commands, checks, contracts, MCP tools,
knowledge domains, and Loop Factory state are all read from their
source of truth, sorted, and rendered without timestamps.

**Syntax**

```text
forge-doctor-data project status [fmt] [write] [check]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `fmt` | no | — | text|json|markdown |
| `write` | no | — | Regenerate docs\project-status.md (commit the diff). |
| `check` | no | — | Verify docs\project-status.md matches the live registries; exit 1 on drift. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## python

### `python`

Run only python checks.

**Syntax**

```text
forge-doctor-data python [path] [ignore] [fmt] [quiet] [fail_on] [verbose] [baseline] [save_baseline] [output] [no_color] [new_only] [no_plugins] [files] [profile] [emit] [show_root] [cache] [stats]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `ignore` | no | — | Suppress a check id. |
| `fmt` | no | — | text|json|html|sarif|agent |
| `quiet` | no | — | Only problems. |
| `fail_on` | no | — | Lowest severity that fails: error|warning. |
| `verbose` | no | — | Internal detail. |
| `baseline` | no | — | Compare against a baseline file or a named baseline in .forge-doctor-data/baselines/<name>.json. |
| `save_baseline` | no | — | Write results to a baseline file or a named baseline in .forge-doctor-data/baselines/<name>.json. |
| `output` | no | — | Write output to a file. |
| `no_color` | no | — | Disable ANSI colors. |
| `new_only` | no | — | Show only findings new vs --baseline. |
| `no_plugins` | no | — | Skip external plugin loading. |
| `files` | no | — | Report findings for these files only. |
| `profile` | no | — | Severity policy: default|strict|security|spark-performance|glue-migration|production. |
| `emit` | no | — | Extra output: FMT or FMT:PATH (repeatable). One may target stdout. |
| `show_root` | no | — | Include the absolute project root in JSON output. |
| `cache` | no | — | Reuse per-file analysis facts (user cache dir; off by default in CI). |
| `stats` | no | — | Scan stats (files, timings, cache, memory) to stderr. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## quality

### `quality`

Data quality: Deequ/GX/SodaCL/dbt suites, coverage, gate wiring.

**Syntax**

```text
forge-doctor-data quality
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `quality inspect`

Print declared suites, coverage map, and gate wiring.

**Syntax**

```text
forge-doctor-data quality inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## redshift

### `redshift`

Redshift intelligence: inspect the vendor model.

**Syntax**

```text
forge-doctor-data redshift
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `redshift inspect`

Print the Redshift model: compute, relations, WLM, exports.

**Syntax**

```text
forge-doctor-data redshift inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## reliability

### `reliability`

End-to-end SLO & critical-path intelligence.

**Syntax**

```text
forge-doctor-data reliability
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `reliability path`

Critical paths over data-flow edges with per-segment coverage.

**Syntax**

```text
forge-doctor-data reliability path [path] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |
| `as_json` | no | — | — |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `reliability slo`

SLO budgets + SLO001-006 findings over critical paths.

**Syntax**

```text
forge-doctor-data reliability slo [path] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |
| `as_json` | no | — | — |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## remediate

### `remediate`

Print deterministic remediation plans for findings / root causes.

**Syntax**

```text
forge-doctor-data remediate [path] [root_cause] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |
| `root_cause` | no | — | Cluster id (prefix ok), e.g. RC_STREAM_COMMITS. |
| `as_json` | no | — | Emit JSON. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## repo

### `repo`

Run only repository checks.

**Syntax**

```text
forge-doctor-data repo [path] [ignore] [fmt] [quiet] [fail_on] [verbose] [baseline] [save_baseline] [output] [no_color] [new_only] [no_plugins] [files] [profile] [emit] [show_root] [cache] [stats]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `ignore` | no | — | Suppress a check id. |
| `fmt` | no | — | text|json|html|sarif|agent |
| `quiet` | no | — | Only problems. |
| `fail_on` | no | — | Lowest severity that fails: error|warning. |
| `verbose` | no | — | Internal detail. |
| `baseline` | no | — | Compare against a baseline file or a named baseline in .forge-doctor-data/baselines/<name>.json. |
| `save_baseline` | no | — | Write results to a baseline file or a named baseline in .forge-doctor-data/baselines/<name>.json. |
| `output` | no | — | Write output to a file. |
| `no_color` | no | — | Disable ANSI colors. |
| `new_only` | no | — | Show only findings new vs --baseline. |
| `no_plugins` | no | — | Skip external plugin loading. |
| `files` | no | — | Report findings for these files only. |
| `profile` | no | — | Severity policy: default|strict|security|spark-performance|glue-migration|production. |
| `emit` | no | — | Extra output: FMT or FMT:PATH (repeatable). One may target stdout. |
| `show_root` | no | — | Include the absolute project root in JSON output. |
| `cache` | no | — | Reuse per-file analysis facts (user cache dir; off by default in CI). |
| `stats` | no | — | Scan stats (files, timings, cache, memory) to stderr. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## root-cause

### `root-cause`

Correlate scan findings with runtime evidence into causal clusters.

**Syntax**

```text
forge-doctor-data root-cause [path] [runtime] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |
| `runtime` | no | — | Exported runtime artifact(s). |
| `as_json` | no | — | Emit JSON. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## runtime

### `runtime`

Offline runtime evidence (exported artifacts).

**Syntax**

```text
forge-doctor-data runtime
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `runtime baseline`

Robust baselines (median/p95/MAD) per fingerprint or recorded series.

**Syntax**

```text
forge-doctor-data runtime baseline [artifact] [root] [last] [days] [metric] [adapter] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `artifact` | no | — | Artifact to baseline directly (no recording). |
| `root` | no | — | Project root holding .forge-doctor-data/. |
| `last` | no | — | Baseline over last N executions. |
| `days` | no | — | Baseline over last N days. |
| `metric` | no | — | Show one metric only. |
| `adapter` | no | — | Force an adapter instead of auto-detect. |
| `as_json` | no | — | Machine-readable output. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `runtime capacity`

Capacity/saturation signals + trends over recorded history (CAP001-007).

Threshold provenance is config > platform pack > baseline — an
unthresholded dimension reports UNKNOWN, never a global rule.

**Syntax**

```text
forge-doctor-data runtime capacity [root] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `root` | no | — | Project root holding .forge-doctor-data/. |
| `as_json` | no | — | Machine-readable output. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `runtime correlate`

Correlate recorded change events with regression episodes.

Evidence-gated: a correlation is reported only when at least two
evidence legs hold (temporal proximity, entity overlap, graph path,
metric relevance).  Language stays 'correlated with' — never cause.

**Syntax**

```text
forge-doctor-data runtime correlate <events> [root] [window_minutes] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `events` | yes | — | JSON file of change events (deployment export / diff output). |
| `root` | no | — | Project root holding .forge-doctor-data/. |
| `window_minutes` | no | — | Max minutes between change and regression start. |
| `as_json` | no | — | Machine-readable output. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `runtime cost`

Derive technical cost drivers + COST findings (never prices).

**Syntax**

```text
forge-doctor-data runtime cost <artifact> [adapter] [root] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `artifact` | yes | — | Exported engine artifact. |
| `adapter` | no | — | Force an adapter instead of auto-detect. |
| `root` | no | — | Project root for entity drivers/transfers. |
| `as_json` | no | — | Machine-readable output. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `runtime diagnose`

Match the artifact's errors against known error signatures.

**Syntax**

```text
forge-doctor-data runtime diagnose <artifact> [adapter]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `artifact` | yes | — | Exported runtime artifact. |
| `adapter` | no | — | Force an adapter instead of auto-detect. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `runtime executions`

Normalize an exported artifact into QueryExecution spines.

**Syntax**

```text
forge-doctor-data runtime executions <artifact> [adapter] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `artifact` | yes | — | Exported engine artifact. |
| `adapter` | no | — | Force an adapter instead of auto-detect. |
| `as_json` | no | — | Machine-readable output. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `runtime history`

Record an artifact batch and/or list recorded history series.

With ``artifact``, the normalized executions are appended as one
compact JSONL snapshot under ``.forge-doctor-data/execution-history/``
(metrics + fingerprints only — never raw logs or SQL).  Without an
artifact, the stored series are listed.

**Syntax**

```text
forge-doctor-data runtime history [artifact] [root] [kind] [adapter] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `artifact` | no | — | Artifact to record into execution history. |
| `root` | no | — | Project root holding .forge-doctor-data/. |
| `kind` | no | — | production|experiment |
| `adapter` | no | — | Force an adapter instead of auto-detect. |
| `as_json` | no | — | Machine-readable output. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `runtime inspect`

Normalize one artifact into runtime facts (offline).

**Syntax**

```text
forge-doctor-data runtime inspect <artifact> [adapter] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `artifact` | yes | — | Exported runtime artifact. |
| `adapter` | no | — | Force an adapter instead of auto-detect. |
| `as_json` | no | — | Machine-readable output. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `runtime performance`

Derive performance signals + PERF findings from an artifact.

**Syntax**

```text
forge-doctor-data runtime performance <artifact> [adapter] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `artifact` | yes | — | Exported engine artifact. |
| `adapter` | no | — | Force an adapter instead of auto-detect. |
| `as_json` | no | — | Machine-readable output. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `runtime regressions`

Baseline-aware regression detection (PERFREG001-009).

Compares each series' latest window against its own historical
baseline — a single slow run reports as a candidate (INFO), only
persistent breaches warn.

**Syntax**

```text
forge-doctor-data runtime regressions [artifact] [root] [adapter] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `artifact` | no | — | Artifact to analyze (or recorded history when omitted). |
| `root` | no | — | Project root holding .forge-doctor-data/. |
| `adapter` | no | — | Force an adapter instead of auto-detect. |
| `as_json` | no | — | Machine-readable output. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `runtime reliability`

Reliability models, delivery semantics, objectives + REL findings.

**Syntax**

```text
forge-doctor-data runtime reliability <root> [artifact] [adapter] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `root` | yes | — | Project root to analyze. |
| `artifact` | no | — | Optional exported runtime artifact. |
| `adapter` | no | — | Force an adapter instead of auto-detect. |
| `as_json` | no | — | Machine-readable output. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `runtime trend`

Per-series trend direction for one metric (rising/falling/stable).

**Syntax**

```text
forge-doctor-data runtime trend [artifact] [root] [metric] [adapter] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `artifact` | no | — | Artifact to trend directly (no recording). |
| `root` | no | — | Project root holding .forge-doctor-data/. |
| `metric` | no | — | Metric to trend. |
| `adapter` | no | — | Force an adapter instead of auto-detect. |
| `as_json` | no | — | Machine-readable output. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## sbom

### `sbom`

Emit a CycloneDX 1.5 SBOM: deps, plugins, knowledge packs, images.

**Syntax**

```text
forge-doctor-data sbom [path] [fmt] [output]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `fmt` | no | — | cyclonedx|text |
| `output` | no | — | Write output to a file. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## scan

### `scan`

Scan a project for data-engineering problems.

**Syntax**

```text
forge-doctor-data scan [path] [check] [ignore] [fmt] [quiet] [fail_on] [verbose] [baseline] [save_baseline] [output] [watch] [no_color] [new_only] [no_plugins] [files] [profile] [emit] [show_root] [cache] [stats] [stats_format] [evidence_out] [evidence_compact] [record] [keep] [incremental]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `check` | no | — | Limit scan to a category. |
| `ignore` | no | — | Suppress a check id. |
| `fmt` | no | — | text|json|html|sarif|agent |
| `quiet` | no | — | Only problems. |
| `fail_on` | no | — | Lowest severity that fails: error|warning. |
| `verbose` | no | — | Internal detail. |
| `baseline` | no | — | Compare against a baseline file or a named baseline in .forge-doctor-data/baselines/<name>.json. |
| `save_baseline` | no | — | Write results to a baseline file or a named baseline in .forge-doctor-data/baselines/<name>.json. |
| `output` | no | — | Write output to a file. |
| `watch` | no | — | Re-scan whenever files change. |
| `no_color` | no | — | Disable ANSI colors. |
| `new_only` | no | — | Show only findings new vs --baseline. |
| `no_plugins` | no | — | Skip external plugin loading. |
| `files` | no | — | Report findings for these files only. |
| `profile` | no | — | Severity policy: default|strict|security|spark-performance|glue-migration|production. |
| `emit` | no | — | Extra output: FMT or FMT:PATH (repeatable). One may target stdout. |
| `show_root` | no | — | Include the absolute project root in JSON output. |
| `cache` | no | — | Reuse per-file analysis facts (user cache dir; off by default in CI). |
| `stats` | no | — | Scan stats (files, timings, cache, memory) to stderr. |
| `stats_format` | no | — | With --stats: text or json (both written to stderr). |
| `evidence_out` | no | — | Write a dated audit bundle (report + suppressions + policy packs). |
| `evidence_compact` | no | — | With --evidence-out: bundle v2 — compact summary.json sized for token-constrained consumers instead of the full report. |
| `record` | no | — | Append a history snapshot to .forge-doctor-data/history/. |
| `keep` | no | — | With --record: retain only the newest N snapshots. |
| `incremental` | no | — | Rerun only checks whose evidence domains changed; others reuse the previous scan's results. --watch applies it per event. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## schema

### `schema`

Schema extraction and diffing.

**Syntax**

```text
forge-doctor-data schema
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `schema contracts`

Dump the JSON Schemas for Forge Doctor Data's public artifacts.

**Syntax**

```text
forge-doctor-data schema contracts [name]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `name` | no | — | Contract name; omit to list all. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `schema diff`

Diff two schema files, or all schema files across a git range.

**Syntax**

```text
forge-doctor-data schema diff <old> [new] [path] [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `old` | yes | — | Old schema file, or 'base...head' git range. |
| `new` | no | — | New schema file. |
| `path` | no | — | Repo root for git ranges. |
| `fmt` | no | — | text|json |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## search

### `search`

Search platforms: OpenSearch/Elasticsearch indices, policies, domains.

**Syntax**

```text
forge-doctor-data search
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `search inspect`

Print the search model: indices/templates, policies, pipelines, domains.

**Syntax**

```text
forge-doctor-data search inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## snowflake

### `snowflake`

Snowflake intelligence: inspect the vendor model.

**Syntax**

```text
forge-doctor-data snowflake
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `snowflake inspect`

Print the Snowflake model: warehouses, objects, exports, copies.

**Syntax**

```text
forge-doctor-data snowflake inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## spark

### `spark`

Spark checks and runtime diagnosis. Bare: Run only spark checks (default) or a runtime subcommand.

**Syntax**

```text
forge-doctor-data spark [path] [ignore] [fmt] [quiet] [fail_on] [verbose] [no_color] [profile]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory. |
| `ignore` | no | — | Suppress a check id. |
| `fmt` | no | — | text|json|html|sarif|agent |
| `quiet` | no | — | Only problems. |
| `fail_on` | no | — | Lowest severity that fails: error|warning. |
| `verbose` | no | — | Internal detail. |
| `no_color` | no | — | Disable ANSI colors. |
| `profile` | no | — | Severity policy: default|strict|security|spark-performance|glue-migration|production. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `spark eventlog`

Analyze a Spark event log (JSONL) for runtime problems.

**Syntax**

```text
forge-doctor-data spark eventlog <source> [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `source` | yes | — | Event-log file or directory. |
| `fmt` | no | — | text|json |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `spark logs`

Fingerprint a Spark log against error packs and runtime signatures.

**Syntax**

```text
forge-doctor-data spark logs <source> [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `source` | yes | — | Driver/executor log file. |
| `fmt` | no | — | text|json |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `spark plan`

Scan a Spark physical plan for pathological operators.

**Syntax**

```text
forge-doctor-data spark plan <source> [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `source` | yes | — | File containing a physical plan. |
| `fmt` | no | — | text|json |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## stepfunctions

### `stepfunctions`

Step Functions intelligence.

**Syntax**

```text
forge-doctor-data stepfunctions
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `stepfunctions inspect`

Summarize Step Functions definitions from the semantic model.

**Syntax**

```text
forge-doctor-data stepfunctions inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## streaming

### `streaming`

Streaming intelligence.

**Syntax**

```text
forge-doctor-data streaming
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `streaming diagnose`

Deterministic runtime diagnostics over a progress batch series.

**Syntax**

```text
forge-doctor-data streaming diagnose <artifacts>
```

| argument/flag | required | default | description |
|---|---|---|---|
| `artifacts` | yes | — | One or more StreamingQueryProgress JSON exports. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `streaming inspect`

Summarize streaming queries from the semantic model.

**Syntax**

```text
forge-doctor-data streaming inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `streaming progress`

Summarize a Structured Streaming progress artifact (offline).

**Syntax**

```text
forge-doctor-data streaming progress <artifact>
```

| argument/flag | required | default | description |
|---|---|---|---|
| `artifact` | yes | — | StreamingQueryProgress JSON export. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `streaming semantics`

Derived delivery semantics per streaming query.

**Syntax**

```text
forge-doctor-data streaming semantics [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## suppressions

### `suppressions`

Audit configured suppressions: ACTIVE / EXPIRED / UNUSED.

**Syntax**

```text
forge-doctor-data suppressions [path] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `as_json` | no | — | Emit statuses as JSON. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## terraform

### `terraform`

Terraform intelligence: inspect.

**Syntax**

```text
forge-doctor-data terraform
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `terraform inspect`

Summarize the project's Terraform surface from the semantic model.

**Syntax**

```text
forge-doctor-data terraform inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## trace

### `trace`

Explain ONE finding: evidence, enclosing symbol, receiver chain.

**Syntax**

```text
forge-doctor-data trace <check_id> <location> [path] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `check_id` | yes | — | Check id, e.g. SPARK001. |
| `location` | yes | — | file:line, e.g. jobs/etl.py:42. |
| `path` | no | — | Project root. |
| `as_json` | no | — | Emit structured chain. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## trino

### `trino`

Trino intelligence: inspect catalogs, coordinator, lineage.

**Syntax**

```text
forge-doctor-data trino
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `trino inspect`

Print the Trino model: catalogs, coordinator flags, SQL refs.

**Syntax**

```text
forge-doctor-data trino inspect [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## twin

### `twin`

Formal digital twin: validated platform snapshot.

**Syntax**

```text
forge-doctor-data twin
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `twin diff`

Diff two twin-state snapshots: entities, rels, capabilities, drift.

**Syntax**

```text
forge-doctor-data twin diff <a> <b> [path] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `a` | yes | — | Older snapshot (path or recorded name). |
| `b` | yes | — | Newer snapshot (path or recorded name). |
| `path` | no | — | Project directory to scan. |
| `as_json` | no | — | — |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `twin explain`

Show one entity across all five states.

**Syntax**

```text
forge-doctor-data twin explain <entity> [path] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `entity` | yes | — | Entity key to explain across states. |
| `path` | no | — | Project directory to scan. |
| `as_json` | no | — | — |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `twin export`

Emit the deterministic twin snapshot artifact.

**Syntax**

```text
forge-doctor-data twin export [path] [output]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `output` | no | — | Write to file (default: stdout). |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `twin facts`

List state-tagged facts the twin collected.

**Syntax**

```text
forge-doctor-data twin facts [path] [state] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `state` | no | — | Filter: desired|declared|implemented|observed|hypothetical. |
| `as_json` | no | — | — |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `twin inspect`

Twin summary + invariant report. Exit 1 on hard violations.

**Syntax**

```text
forge-doctor-data twin inspect [path] [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `fmt` | no | — | text|json |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `twin reconcile`

Reconcile the five states: every (entity, property) divergence.

**Syntax**

```text
forge-doctor-data twin reconcile [path] [as_json]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `as_json` | no | — | — |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `twin record`

Persist a five-state twin snapshot into the project history dir.

**Syntax**

```text
forge-doctor-data twin record [path] [name]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project directory to scan. |
| `name` | no | — | Snapshot name. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## version

### `version`

Print the installed Forge Doctor Data version.

**Syntax**

```text
forge-doctor-data version
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## what-if

### `what-if`

Evaluate a hypothetical change without executing it. Bare: Evaluate --change target=value specs against the project.

**Syntax**

```text
forge-doctor-data what-if [path] [change] [assume]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |
| `change` | no | — | target=value, e.g. glue-version=5.1 |
| `assume` | no | — | extra assumption fact recorded on the report |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## workspace

### `workspace`

Discover and orchestrate sub-projects. Bare: Discover sub-projects (pyproject.toml) under a workspace root.

**Syntax**

```text
forge-doctor-data workspace [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Workspace root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `workspace diff`

Per-subproject finding diff across a git range.

**Syntax**

```text
forge-doctor-data workspace diff <range_spec> [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `range_spec` | yes | — | 'base...head' git range. |
| `path` | no | — | Repo/workspace root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `workspace inspect`

Build the WorkspaceModel: repos, merged platform graph, cross-repo links.

**Syntax**

```text
forge-doctor-data workspace inspect [path] [fmt]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Workspace root. |
| `fmt` | no | — | text|json |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `workspace scan`

Scan every nested project and aggregate results with a project column.

**Syntax**

```text
forge-doctor-data workspace scan [path] [fmt] [profile] [quiet] [fail_on] [no_plugins]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Workspace root. |
| `fmt` | no | — | text|json|sarif |
| `profile` | no | — | Severity policy: default|strict|security|spark-performance|glue-migration|production. |
| `quiet` | no | — | Only problems. |
| `fail_on` | no | — | Lowest severity that fails: error|warning. |
| `no_plugins` | no | — | Skip external plugin loading. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->
