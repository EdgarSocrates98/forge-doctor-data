# `forge-doctor-data` command reference

Generated from the real CLI parser by `doc_inventory.py` + `doc_reference.py`. Do not hand-edit generated sections — write between `keep:start`/`keep:end` markers. `por que`/`quando` lines come from the curated `command-rationale.json` — edit rationale there, never here. Status vocabulary: `available` unless marked otherwise.

Rationale coverage: **90/90** first-level groups curated in `command-rationale.json`.

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
- [`graph`](#graph) — 7 command(s)
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

**para que:** Rank findings into a cited action list.

Score = severity + confidence + cluster + fix-safety + plan + policy
+ blast radius; every row cites fingerprints and entity ids.
Advisory only - apply via ``fix``/``remediate`` commands.

- **por que:** ordena findings numa lista de ações citadas (severidade+confiança+cluster+segurança do fix)
- **quando usar:** depois do scan: priorizar o que atacar primeiro com justificativa

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

**para que:** Deterministic, budget-aware agent context.

- **por que:** contexto de agente determinístico e com orçamento
- **quando usar:** montar contexto econômico para um host/agente

**Syntax**

```text
forge-doctor-data agent
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `agent context`

**para que:** Emit summary-first context constrained by an approximate token budget.

- **por que:** contexto de agente determinístico e com orçamento
- **quando usar:** montar contexto econômico para um host/agente

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

**para que:** Emit added/removed/unchanged finding fingerprints.

- **por que:** contexto de agente determinístico e com orçamento
- **quando usar:** montar contexto econômico para um host/agente

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

**para que:** Resolve one lazy evidence reference.

- **por que:** contexto de agente determinístico e com orçamento
- **quando usar:** montar contexto econômico para um host/agente

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

**para que:** Emit compact domains, risks, capabilities, and evidence references.

- **por que:** contexto de agente determinístico e com orçamento
- **quando usar:** montar contexto econômico para um host/agente

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

**para que:** Airflow intelligence: inspect DAGs, tasks, sensors.

- **por que:** inteligência Airflow: inspeciona DAGs, tasks, sensors
- **quando usar:** revisar definição de DAGs Airflow com evidência

**Syntax**

```text
forge-doctor-data airflow
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `airflow inspect`

**para que:** Summarize the project's Airflow surface from the semantic model.

- **por que:** inteligência Airflow: inspeciona DAGs, tasks, sensors
- **quando usar:** revisar definição de DAGs Airflow com evidência

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

**para que:** Real-time OLAP engines: ClickHouse / Pinot / Druid inspection.

- **por que:** engines OLAP real-time: inspeção ClickHouse/Pinot/Druid
- **quando usar:** perguntas sobre motores analíticos detectados

**Syntax**

```text
forge-doctor-data analytical
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `analytical inspect`

**para que:** Print the analytical-engine model: tables, engines, schemas, observed.

- **por que:** engines OLAP real-time: inspeção ClickHouse/Pinot/Druid
- **quando usar:** perguntas sobre motores analíticos detectados

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

**para que:** Architecture drift detection.

- **por que:** detecta drift de arquitetura
- **quando usar:** verificar se a arquitetura divergiu do declarado

**Syntax**

```text
forge-doctor-data architecture
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `architecture drift`

**para que:** Compare the platform contract against code, IaC, and runtime.

- **por que:** detecta drift de arquitetura
- **quando usar:** verificar se a arquitetura divergiu do declarado

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

**para que:** Athena workgroup/query intelligence.

- **por que:** inteligência de workgroup/query Athena
- **quando usar:** revisar queries e workgroups Athena com evidência

**Syntax**

```text
forge-doctor-data athena
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `athena findings`

- **por que:** inteligência de workgroup/query Athena
- **quando usar:** revisar queries e workgroups Athena com evidência

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

**para que:** Workgroups, catalogs, named queries, SQL ops, boto3 evidence.

- **por que:** inteligência de workgroup/query Athena
- **quando usar:** revisar queries e workgroups Athena com evidência

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

**para que:** Run only aws checks.

- **por que:** roda só checks da categoria aws
- **quando usar:** escopo estreito de checks AWS no scan

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

**para que:** Performance & scale benchmark.

- **por que:** benchmark de performance e escala
- **quando usar:** medir a própria ferramenta ou comparar runs

**Syntax**

```text
forge-doctor-data bench
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `bench run`

**para que:** Run the benchmark on a project or a generated synthetic corpus.

- **por que:** benchmark de performance e escala
- **quando usar:** medir a própria ferramenta ou comparar runs

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

**para que:** BigQuery intelligence: inspect the vendor model.

- **por que:** inteligência BigQuery: inspeciona o modelo do vendor
- **quando usar:** revisar datasets/jobs BigQuery com evidência

**Syntax**

```text
forge-doctor-data bigquery
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `bigquery inspect`

**para que:** Print the BigQuery model: datasets, relations, slots, exports.

- **por que:** inteligência BigQuery: inspeciona o modelo do vendor
- **quando usar:** revisar datasets/jobs BigQuery com evidência

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

**para que:** Inspect or clear the incremental analysis cache. Bare: Show cache statistics for the project.

- **por que:** inspeciona/limpa o cache de análise incremental
- **quando usar:** ver o que está cacheado ou forçar re-análise

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

**para que:** Delete the incremental analysis cache.

- **por que:** inspeciona/limpa o cache de análise incremental
- **quando usar:** ver o que está cacheado ou forçar re-análise

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

**para que:** Platform capability registry.

- **por que:** registry de capabilities da plataforma
- **quando usar:** perguntar o que o doctor declara atender

**Syntax**

```text
forge-doctor-data capabilities
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `capabilities explain`

**para que:** Evaluate one capability in context and show status + provenance.

- **por que:** registry de capabilities da plataforma
- **quando usar:** perguntar o que o doctor declara atender

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

**para que:** Render the capability → evidence subgraph for a project.

Capabilities observed in the project evaluate against the versions
its entities declare; each edge carries the deciding pack entry,
matched when-clause, and (for unknowns) the missing evidence.

- **por que:** registry de capabilities da plataforma
- **quando usar:** perguntar o que o doctor declara atender

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

**para que:** List every capability fact by platform with its headline status.

``--json`` emits ``{platform: {capability: status}}``; with
``--provenance`` each row becomes ``{"status", "provenance"}``
carrying the deciding pack entry, matched when-clause, and source.

- **por que:** registry de capabilities da plataforma
- **quando usar:** perguntar o que o doctor declara atender

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

**para que:** Metadata catalogs: DataHub/OpenMetadata/Glue/Unity declared estate.

- **por que:** catálogos de metadados: DataHub/OpenMetadata/Glue/Unity declarados
- **quando usar:** revisar o estate de catálogos declarado

**Syntax**

```text
forge-doctor-data catalog
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `catalog inspect`

**para que:** Print the declared catalog: datasets, owners, lineage, recipes.

- **por que:** catálogos de metadados: DataHub/OpenMetadata/Glue/Unity declarados
- **quando usar:** revisar o estate de catálogos declarado

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

**para que:** List every registered check id, category and title.

- **por que:** lista todo check_id registrado, categoria e título
- **quando usar:** descobrir quais checks existem antes de rodar

**Syntax**

```text
forge-doctor-data checks
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## ci

### `ci`

**para que:** Run only ci checks.

- **por que:** roda só checks da categoria ci
- **quando usar:** escopo de checks de CI/CD

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

**para que:** Multi-cloud abstractions: vendor-neutral view over detected services.

- **por que:** abstrações multi-cloud: visão vendor-neutral sobre serviços detectados
- **quando usar:** pergunta cross-cloud sem amarrar a um vendor

**Syntax**

```text
forge-doctor-data cloud
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `cloud inspect`

**para que:** Print the abstraction view: services by kind, cloud, parity gaps.

- **por que:** abstrações multi-cloud: visão vendor-neutral sobre serviços detectados
- **quando usar:** pergunta cross-cloud sem amarrar a um vendor

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

**para que:** Validate normalized evidence bundles.

- **por que:** valida bundles de evidência normalizados
- **quando usar:** conferir um bundle de coleta antes de analisar

**Syntax**

```text
forge-doctor-data collector
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `collector validate`

**para que:** Validate a bundle before offline analysis consumes it.

- **por que:** valida bundles de evidência normalizados
- **quando usar:** conferir um bundle de coleta antes de analisar

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

**para que:** Detect runtimes and show Glue migration risks (knowledge packs).

- **por que:** detecta runtimes e mostra riscos de migração Glue (knowledge packs)
- **quando usar:** avaliar compatibilidade/migração com fonte versionada

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

**para que:** Platform contract files.

- **por que:** arquivos de contrato da plataforma
- **quando usar:** inspecionar contratos versionados

**Syntax**

```text
forge-doctor-data contract
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `contract validate`

**para que:** Validate a platform contract's structure and schema version.

- **por que:** arquivos de contrato da plataforma
- **quando usar:** inspecionar contratos versionados

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

**para que:** Published artifact contracts (verify handoff bundles, schemas).

- **por que:** contratos de artefatos publicados (bundles de handoff, schemas)
- **quando usar:** verificar handoffs contra schema publicado

**Syntax**

```text
forge-doctor-data contracts
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `contracts conformance`

**para que:** Check a payload against forge-contracts/1 (spec 267).

Validates the payload twice: against the published JSON Schema for its
kind, and through the strict ``from_dict`` model decode. Exit code 1 on
any violation. Other Forge products (The Forger, Spark Forge, agents)
use this to prove they speak the same wire contract.

- **por que:** contratos de artefatos publicados (bundles de handoff, schemas)
- **quando usar:** verificar handoffs contra schema publicado

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

**para que:** List the published contract names (see `schema contracts <name>` for a dump).

- **por que:** contratos de artefatos publicados (bundles de handoff, schemas)
- **quando usar:** verificar handoffs contra schema publicado

**Syntax**

```text
forge-doctor-data contracts list
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `contracts schema`

**para que:** Dump the published forge-contracts/1 JSON Schemas.

- **por que:** contratos de artefatos publicados (bundles de handoff, schemas)
- **quando usar:** verificar handoffs contra schema publicado

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

**para que:** Validate a JSON artifact against a published contract (stdin or file).

``forge-doctor-data export --format handoff`` output validates against
``handoff-bundle``; other Forge tools use this in their own tests.

- **por que:** contratos de artefatos publicados (bundles de handoff, schemas)
- **quando usar:** verificar handoffs contra schema publicado

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

**para que:** Control-M intelligence: inspect workflows-as-code.

- **por que:** inteligência Control-M: inspeciona workflows-as-code
- **quando usar:** revisar jobs Control-M declarados

**Syntax**

```text
forge-doctor-data controlm
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `controlm inspect`

**para que:** Summarize the project's Control-M surface from the semantic model.

- **por que:** inteligência Control-M: inspeciona workflows-as-code
- **quando usar:** revisar jobs Control-M declarados

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

**para que:** Cross-domain access-style inspection.

- **por que:** inspeção de estilo de acesso cross-domain
- **quando usar:** perguntas de modelo de acesso a dados

**Syntax**

```text
forge-doctor-data data-model
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `data-model inspect`

**para que:** Breakdown of observed access styles across data domains.

- **por que:** inspeção de estilo de acesso cross-domain
- **quando usar:** perguntas de modelo de acesso a dados

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

**para que:** Databricks workspace/job/UC intelligence.

- **por que:** inteligência Databricks: workspace/job/UC
- **quando usar:** revisar definições Databricks com evidência

**Syntax**

```text
forge-doctor-data databricks
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `databricks findings`

- **por que:** inteligência Databricks: workspace/job/UC
- **quando usar:** revisar definições Databricks com evidência

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

**para que:** Jobs, clusters, warehouses, UC objects, pipelines, bundles.

- **por que:** inteligência Databricks: workspace/job/UC
- **quando usar:** revisar definições Databricks com evidência

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

**para que:** dbt intelligence: inspect the transformation model.

- **por que:** inteligência dbt: inspeciona o modelo de transformação
- **quando usar:** revisar modelos, testes e lineage dbt

**Syntax**

```text
forge-doctor-data dbt
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `dbt inspect`

**para que:** Print the dbt model: models, sources, tests, manifest coverage.

- **por que:** inteligência dbt: inspeciona o modelo de transformação
- **quando usar:** revisar modelos, testes e lineage dbt

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

**para que:** Delta Lake feature and ops intelligence.

- **por que:** inteligência Delta Lake: features e operações
- **quando usar:** revisar tabelas Delta e operações declaradas

**Syntax**

```text
forge-doctor-data delta
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `delta features`

**para que:** Detected Delta features mapped to protocol requirements.

- **por que:** inteligência Delta Lake: features e operações
- **quando usar:** revisar tabelas Delta e operações declaradas

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

- **por que:** inteligência Delta Lake: features e operações
- **quando usar:** revisar tabelas Delta e operações declaradas

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

**para que:** Tables, ops (merge/optimize/vacuum), features, protocol.

- **por que:** inteligência Delta Lake: features e operações
- **quando usar:** revisar tabelas Delta e operações declaradas

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

**para que:** Run only dependencies checks.

- **por que:** roda só checks de dependências
- **quando usar:** escopo de checks de dependências do projeto

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

**para que:** Fingerprint log errors against known signatures (deterministic, offline).

- **por que:** fingerprint de erros de log contra assinaturas conhecidas (offline)
- **quando usar:** classificar um erro de log sem chamar nada externo

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

**para que:** Diff findings: NEW in <new> vs <old>, or in a 'base...head' git range.

- **por que:** diff de findings: NEW em <novo> vs <velho>, ou range git base...head
- **quando usar:** comparar findings entre dois scans ou branches

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

**para que:** Run only docker checks.

- **por que:** roda só checks de docker
- **quando usar:** escopo de checks de Docker/imagem

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

**para que:** Self-check: config, plugins, cache dir, git, environment health.

- **por que:** self-check: config, plugins, cache, git, saúde do ambiente
- **quando usar:** primeira linha de diagnóstico da própria ferramenta

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

**para que:** DynamoDB intelligence.

- **por que:** inteligência DynamoDB
- **quando usar:** revisar tabelas/acesso DynamoDB com evidência

**Syntax**

```text
forge-doctor-data dynamodb
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `dynamodb access-patterns`

**para que:** List observed access operations per table.

- **por que:** inteligência DynamoDB
- **quando usar:** revisar tabelas/acesso DynamoDB com evidência

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

**para que:** Billing-mode inventory - structure only, no cost math.

- **por que:** inteligência DynamoDB
- **quando usar:** revisar tabelas/acesso DynamoDB com evidência

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

**para que:** Global-table modes (MREC/MRSC), regions, transaction semantics.

- **por que:** inteligência DynamoDB
- **quando usar:** revisar tabelas/acesso DynamoDB com evidência

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

**para que:** GSI/LSI inventory vs observed IndexName usage.

- **por que:** inteligência DynamoDB
- **quando usar:** revisar tabelas/acesso DynamoDB com evidência

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

**para que:** Summarize tables, keys, capacity mode, streams, global tables.

- **por que:** inteligência DynamoDB
- **quando usar:** revisar tabelas/acesso DynamoDB com evidência

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

**para que:** Stream configuration and detected consumers.

- **por que:** inteligência DynamoDB
- **quando usar:** revisar tabelas/acesso DynamoDB com evidência

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

**para que:** EMR deep intelligence (EC2/Serverless/EKS).

- **por que:** inteligência EMR profunda (EC2/Serverless/EKS)
- **quando usar:** revisar clusters/jobs EMR por superfície

**Syntax**

```text
forge-doctor-data emr
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `emr findings`

- **por que:** inteligência EMR profunda (EC2/Serverless/EKS)
- **quando usar:** revisar clusters/jobs EMR por superfície

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

**para que:** Clusters, serverless apps, EKS virtual clusters, releases, steps.

- **por que:** inteligência EMR profunda (EC2/Serverless/EKS)
- **quando usar:** revisar clusters/jobs EMR por superfície

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

**para que:** Explain what a check looks for, when it is OK, and how to fix it.

- **por que:** explica o que um check procura, quando é OK e como corrigir
- **quando usar:** entender um check antes de rodar ou de agir sobre o finding

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

**para que:** Emit a portable handoff bundle: findings + graph + capabilities + plans.

- **por que:** emite bundle portátil de handoff: findings+graph+capabilities+plans
- **quando usar:** transferir o resultado para outro host/forja

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

**para que:** Preview (or apply) deterministic safe fixes for findings.

- **por que:** preview (ou aplica) fixes determinísticos seguros para findings
- **quando usar:** corrigir findings com fix seguro — preview antes de aplicar

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

**para que:** Fleet/estate intelligence across many repos. Bare: Fleet/estate intelligence over a manifest of repositories.

- **por que:** inteligência de frota/estate sobre manifesto multi-repo
- **quando usar:** perguntas agregadas sobre muitos repos

**Syntax**

```text
forge-doctor-data fleet
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `fleet inspect`

**para que:** Estate census: repos, merged platform graph, cross-repo links.

- **por que:** inteligência de frota/estate sobre manifesto multi-repo
- **quando usar:** perguntas agregadas sobre muitos repos

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

**para que:** Portfolio view: platforms, workloads, duplication, complexity —
facts only, no health score.

- **por que:** inteligência de frota/estate sobre manifesto multi-repo
- **quando usar:** perguntas agregadas sobre muitos repos

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

**para que:** Deterministic estate queries over the merged fleet graph.

- **por que:** inteligência de frota/estate sobre manifesto multi-repo
- **quando usar:** perguntas agregadas sobre muitos repos

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

**para que:** Fleet-level regression aggregation: same regression family across
workloads/repos (e.g. after a platform upgrade).

- **por que:** inteligência de frota/estate sobre manifesto multi-repo
- **quando usar:** perguntas agregadas sobre muitos repos

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

**para que:** Estate census + per-repo findings roll-up (built-in checks only).

- **por que:** inteligência de frota/estate sobre manifesto multi-repo
- **quando usar:** perguntas agregadas sobre muitos repos

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

**para que:** Flink deep intelligence.

- **por que:** inteligência Flink profunda
- **quando usar:** revisar jobs/checkpoints Flink

**Syntax**

```text
forge-doctor-data flink
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `flink findings`

- **por que:** inteligência Flink profunda
- **quando usar:** revisar jobs/checkpoints Flink

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

**para que:** Jobs, sources, keyed state, windows, timers, checkpoints, sinks.

- **por que:** inteligência Flink profunda
- **quando usar:** revisar jobs/checkpoints Flink

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

**para que:** Run only git checks.

- **por que:** roda só checks de git
- **quando usar:** escopo de checks de repositório git

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

**para que:** Run only glue checks.

- **por que:** roda só checks de glue
- **quando usar:** escopo de checks AWS Glue

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

**para que:** Golden repositories - snapshot regression suites.

- **por que:** repositórios golden — suítes de regressão por snapshot
- **quando usar:** validar a ferramenta contra casos conhecidos

**Syntax**

```text
forge-doctor-data golden
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `golden list`

**para que:** List golden repositories.

- **por que:** repositórios golden — suítes de regressão por snapshot
- **quando usar:** validar a ferramenta contra casos conhecidos

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

**para que:** Diff current engine output against stored snapshots.

- **por que:** repositórios golden — suítes de regressão por snapshot
- **quando usar:** validar a ferramenta contra casos conhecidos

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

**para que:** Regenerate snapshots — review the diff before committing.

- **por que:** repositórios golden — suítes de regressão por snapshot
- **quando usar:** validar a ferramenta contra casos conhecidos

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

**para que:** Graph intelligence.

- **por que:** inteligência de grafo
- **quando usar:** perguntas de dependência/grafo da plataforma

**Syntax**

```text
forge-doctor-data graph
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `graph inspect`

**para que:** Summarize detected graph workloads, languages, and paradigms.

- **por que:** inteligência de grafo
- **quando usar:** perguntas de dependência/grafo da plataforma

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

**para que:** Project Intelligence Graph: jobs, datasets, infra, orchestrators.

- **por que:** inteligência de grafo
- **quando usar:** perguntas de dependência/grafo da plataforma

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

**para que:** Show the vertex/edge schema reconstructed from static evidence.

- **por que:** inteligência de grafo
- **quando usar:** perguntas de dependência/grafo da plataforma

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

**para que:** List traversal inventory with per-traversal shape summary.

- **por que:** inteligência de grafo
- **quando usar:** perguntas de dependência/grafo da plataforma

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

### `graph ui`

**para que:** Open the local Graph Studio explorer for this project's evidence graph.

- **por que:** inteligência de grafo
- **quando usar:** perguntas de dependência/grafo da plataforma

**Syntax**

```text
forge-doctor-data graph ui [path] [no_browser] [port]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |
| `no_browser` | no | — | Serve without opening a browser (SSH/remote). |
| `port` | no | — | Port to bind (default ephemeral). |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `graph view`

**para que:** Emit the ForgeGraphView/v1 document (Graph Studio contract).

- **por que:** inteligência de grafo
- **quando usar:** perguntas de dependência/grafo da plataforma

**Syntax**

```text
forge-doctor-data graph view [path]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `path` | no | — | Project root. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## history

### `history`

**para que:** Recorded scan snapshots: list, diff, trend. Bare: List recorded snapshots (scan --record).

- **por que:** snapshots gravados de scan: list, diff, trend
- **quando usar:** comparar scans ao longo do tempo

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

**para que:** Diff two snapshots: new/resolved findings, entity + capability + drift deltas.

- **por que:** snapshots gravados de scan: list, diff, trend
- **quando usar:** comparar scans ao longo do tempo

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

**para que:** Per-category finding counts + entity counts across the series.

- **por que:** snapshots gravados de scan: list, diff, trend
- **quando usar:** comparar scans ao longo do tempo

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

**para que:** Run only iac checks.

- **por que:** roda só checks de iac
- **quando usar:** escopo de checks de infraestrutura como código

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

**para que:** Iceberg intelligence: inspect, maintenance, compatibility.

- **por que:** inteligência Iceberg: inspeção, manutenção, compatibilidade
- **quando usar:** revisar tabelas Iceberg e sua saúde

**Syntax**

```text
forge-doctor-data iceberg
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `iceberg compatibility`

**para que:** Cross detected runtimes with the Iceberg compatibility pack.

- **por que:** inteligência Iceberg: inspeção, manutenção, compatibilidade
- **quando usar:** revisar tabelas Iceberg e sua saúde

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

**para que:** Static small-file risk posture (repartition/coalesce near writes).

- **por que:** inteligência Iceberg: inspeção, manutenção, compatibilidade
- **quando usar:** revisar tabelas Iceberg e sua saúde

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

**para que:** Summarize the project's Iceberg surface from the semantic model.

- **por que:** inteligência Iceberg: inspeção, manutenção, compatibilidade
- **quando usar:** revisar tabelas Iceberg e sua saúde

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

**para que:** Maintenance posture: which Iceberg housekeeping ops exist in code.

- **por que:** inteligência Iceberg: inspeção, manutenção, compatibilidade
- **quando usar:** revisar tabelas Iceberg e sua saúde

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

**para que:** Reconstruct every detected MERGE statement from the semantic model.

- **por que:** inteligência Iceberg: inspeção, manutenção, compatibilidade
- **quando usar:** revisar tabelas Iceberg e sua saúde

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

**para que:** Dependency-aware incident intelligence (offline).

- **por que:** inteligência de incidente com dependência (offline)
- **quando usar:** correlacionar evidência de incidente já exportada

**Syntax**

```text
forge-doctor-data incident
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `incident explain`

**para que:** Narrate one incident's evidence path, causes and unknowns.

- **por que:** inteligência de incidente com dependência (offline)
- **quando usar:** correlacionar evidência de incidente já exportada

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

**para que:** Group co-occurring regression episodes into incident windows.

- **por que:** inteligência de incidente com dependência (offline)
- **quando usar:** correlacionar evidência de incidente já exportada

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

**para que:** Quick project stats - files, languages, tooling - no checks run.

- **por que:** estatísticas rápidas do projeto — arquivos, linguagens, tooling; sem checks
- **quando usar:** visão rápida de um projeto desconhecido

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

**para que:** Scaffold a new Python project (pyproject, .gitignore, README, src/, tests/).

- **por que:** scaffold de projeto Python novo (pyproject, .gitignore, README, src/, tests/)
- **quando usar:** começar um projeto novo com estrutura padrão

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

**para que:** Domain inspection: `inspect <domain> [path]` (alias of `<domain> inspect`).

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

**Syntax**

```text
forge-doctor-data inspect
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `inspect airflow`

**para que:** Alias of `airflow inspect`. Summarize the project's Airflow surface from the semantic model.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `analytical inspect`. Print the analytical-engine model: tables, engines, schemas, observed.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `athena inspect`. Workgroups, catalogs, named queries, SQL ops, boto3 evidence.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `bigquery inspect`. Print the BigQuery model: datasets, relations, slots, exports.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `catalog inspect`. Print the declared catalog: datasets, owners, lineage, recipes.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `cloud inspect`. Print the abstraction view: services by kind, cloud, parity gaps.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `controlm inspect`. Summarize the project's Control-M surface from the semantic model.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `data-model inspect`. Breakdown of observed access styles across data domains.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `databricks inspect`. Jobs, clusters, warehouses, UC objects, pipelines, bundles.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `dbt inspect`. Print the dbt model: models, sources, tests, manifest coverage.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `delta inspect`. Tables, ops (merge/optimize/vacuum), features, protocol.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `dynamodb inspect`. Summarize tables, keys, capacity mode, streams, global tables.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `emr inspect`. Clusters, serverless apps, EKS virtual clusters, releases, steps.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `flink inspect`. Jobs, sources, keyed state, windows, timers, checkpoints, sinks.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `graph inspect`. Summarize detected graph workloads, languages, and paradigms.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `iceberg inspect`. Summarize the project's Iceberg surface from the semantic model.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `incident inspect`. Group co-occurring regression episodes into incident windows.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `kafka inspect`. MSK clusters, topics, consumer groups, options, security.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `kinesis inspect`. Streams, shards, consumers, EFO, retention, flink apps.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `lakeformation inspect`. Census: databases, tables, locations, tags, filters, links, shares.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `lambda inspect`. Functions, runtimes, triggers, destinations, idempotency evidence.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `neptune inspect`. Clusters, instances, endpoints, languages, product split.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `optimize inspect`. Multi-objective opportunities with guardrails + tradeoffs.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `parquet inspect`. Summarize the project's Parquet surface from the semantic model.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `quality inspect`. Print declared suites, coverage map, and gate wiring.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `redshift inspect`. Print the Redshift model: compute, relations, WLM, exports.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `search inspect`. Print the search model: indices/templates, policies, pipelines, domains.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `snowflake inspect`. Print the Snowflake model: warehouses, objects, exports, copies.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `stepfunctions inspect`. Summarize Step Functions definitions from the semantic model.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `streaming inspect`. Summarize streaming queries from the semantic model.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `terraform inspect`. Summarize the project's Terraform surface from the semantic model.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `trino inspect`. Print the Trino model: catalogs, coordinator flags, SQL refs.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `twin inspect`. Twin summary + invariant report. Exit 1 on hard violations.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Alias of `workspace inspect`. Build the WorkspaceModel: repos, merged platform graph, cross-repo links.

- **por que:** inspeção por domínio: `inspect <domain>` (alias de `<domain> inspect`)
- **quando usar:** inspecionar um domínio específico diretamente

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

**para que:** Install Forge Doctor Data into a project, workspace or the user home; manage the lifecycle (status, doctor, repair, update, uninstall).

- **por que:** instala Forge Doctor Data em projeto, workspace ou home; gerencia o ciclo de vida
- **quando usar:** ativar o doctor num escopo governado

**Syntax**

```text
forge-doctor-data install [scope] [host] [profile] [root] [yes] [dry_run] [components]
```

| argument/flag | required | default | description |
|---|---|---|---|
| `scope` | no | — | project|workspace|user. |
| `host` | no | — | claude|devin|codex|copilot|all. |
| `profile` | no | — | minimal|recommended|full. |
| `root` | no | — | Target root (default: VCS root or cwd). |
| `yes` | no | — | Explicit approval; without it only --dry-run is allowed. |
| `dry_run` | no | — | Plan only — writes nothing. |
| `components` | no | — | Optional components csv: skills,agents,mcp,tui,graph-studio. |

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `install doctor`

**para que:** Run installation health checks (ledger, MCP availability).

- **por que:** instala Forge Doctor Data em projeto, workspace ou home; gerencia o ciclo de vida
- **quando usar:** ativar o doctor num escopo governado

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

**para que:** Handshake the configured MCP server (PASS/BLOCKED/FAIL).

- **por que:** instala Forge Doctor Data em projeto, workspace ou home; gerencia o ciclo de vida
- **quando usar:** ativar o doctor num escopo governado

**Syntax**

```text
forge-doctor-data install mcp-verify
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `install repair`

**para que:** Restore missing managed assets; user-modified content is kept.

- **por que:** instala Forge Doctor Data em projeto, workspace ou home; gerencia o ciclo de vida
- **quando usar:** ativar o doctor num escopo governado

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

**para que:** Report drift/health of the resolved installation.

- **por que:** instala Forge Doctor Data em projeto, workspace ou home; gerencia o ciclo de vida
- **quando usar:** ativar o doctor num escopo governado

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

**para que:** Remove ledger-owned assets only; user content is preserved.

- **por que:** instala Forge Doctor Data em projeto, workspace ou home; gerencia o ciclo de vida
- **quando usar:** ativar o doctor num escopo governado

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

**para que:** Upgrade the bootstrapped runtime from its registered checkout.

- **por que:** instala Forge Doctor Data em projeto, workspace ou home; gerencia o ciclo de vida
- **quando usar:** ativar o doctor num escopo governado

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

**para que:** Kafka/MSK deep intelligence.

- **por que:** inteligência Kafka/MSK profunda
- **quando usar:** revisar tópicos/consumers Kafka

**Syntax**

```text
forge-doctor-data kafka
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `kafka findings`

- **por que:** inteligência Kafka/MSK profunda
- **quando usar:** revisar tópicos/consumers Kafka

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

**para que:** MSK clusters, topics, consumer groups, options, security.

- **por que:** inteligência Kafka/MSK profunda
- **quando usar:** revisar tópicos/consumers Kafka

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

**para que:** Kinesis deep intelligence.

- **por que:** inteligência Kinesis profunda
- **quando usar:** revisar streams/shards Kinesis

**Syntax**

```text
forge-doctor-data kinesis
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `kinesis findings`

- **por que:** inteligência Kinesis profunda
- **quando usar:** revisar streams/shards Kinesis

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

**para que:** Streams, shards, consumers, EFO, retention, flink apps.

- **por que:** inteligência Kinesis profunda
- **quando usar:** revisar streams/shards Kinesis

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

**para que:** Knowledge-pack provenance. Bare: List all bundled knowledge packs with provenance.

- **por que:** proveniência de knowledge packs
- **quando usar:** consultar fontes versionadas de conhecimento

**Syntax**

```text
forge-doctor-data knowledge
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `knowledge audit`

**para que:** Classify packs as fresh, stale, expired, invalid_source, or unverified.

- **por que:** proveniência de knowledge packs
- **quando usar:** consultar fontes versionadas de conhecimento

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

**para que:** Semantic pack diff: entries added/removed/changed (not text diff).

- **por que:** proveniência de knowledge packs
- **quando usar:** consultar fontes versionadas de conhecimento

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

**para que:** Show provenance detail for one domain's packs.

- **por que:** proveniência de knowledge packs
- **quando usar:** consultar fontes versionadas de conhecimento

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

**para que:** Alias for the default listing.

- **por que:** proveniência de knowledge packs
- **quando usar:** consultar fontes versionadas de conhecimento

**Syntax**

```text
forge-doctor-data knowledge list
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `knowledge new`

**para que:** Scaffold a new knowledge pack with provenance fields + examples.

- **por que:** proveniência de knowledge packs
- **quando usar:** consultar fontes versionadas de conhecimento

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

**para que:** Publish checklist: freshness fields valid, conformance clean.

- **por que:** proveniência de knowledge packs
- **quando usar:** consultar fontes versionadas de conhecimento

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

**para que:** Pack conformance suite: structure, regexes, examples, capabilities.

- **por que:** proveniência de knowledge packs
- **quando usar:** consultar fontes versionadas de conhecimento

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

**para que:** Validate structure + flag packs stale (>90d since verified_at).

- **por que:** proveniência de knowledge packs
- **quando usar:** consultar fontes versionadas de conhecimento

**Syntax**

```text
forge-doctor-data knowledge verify
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## lab

### `lab`

**para que:** Forge Lab - reproducible scenarios with ground truth.

- **por que:** Forge Lab — cenários reproduzíveis com ground truth
- **quando usar:** validar/criar cenários offline contra verdade conhecida

**Syntax**

```text
forge-doctor-data lab
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `lab experiment`

**para que:** Apply a named hypothesis to a scenario copy and compare findings.

With --before/--after, compares two exported artifact bundles on
declared metrics instead (ExperimentPlan v2: verdicts SUPPORTED /
NOT_SUPPORTED / INCONCLUSIVE / CONSTRAINT_VIOLATED).

Never mutates the fixture: the scenario is copied to a temp dir,
transformed, rescanned hermetically, and reported as
improved | regressed | neutral with reasons.

- **por que:** Forge Lab — cenários reproduzíveis com ground truth
- **quando usar:** validar/criar cenários offline contra verdade conhecida

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

**para que:** List discovered scenarios.

- **por que:** Forge Lab — cenários reproduzíveis com ground truth
- **quando usar:** validar/criar cenários offline contra verdade conhecida

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

**para que:** Precision/recall/FP rates and coverage per domain + total.

- **por que:** Forge Lab — cenários reproduzíveis com ground truth
- **quando usar:** validar/criar cenários offline contra verdade conhecida

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

**para que:** Alias for `lab run` over every scenario (summary view).

- **por que:** Forge Lab — cenários reproduzíveis com ground truth
- **quando usar:** validar/criar cenários offline contra verdade conhecida

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

**para que:** Run scenario(s) and compare engine output to ground truth.

- **por que:** Forge Lab — cenários reproduzíveis com ground truth
- **quando usar:** validar/criar cenários offline contra verdade conhecida

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

**para que:** Lake Formation governance intelligence.

- **por que:** inteligência de governança Lake Formation
- **quando usar:** revisar camadas de acesso Lake Formation

**Syntax**

```text
forge-doctor-data lakeformation
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `lakeformation compatibility`

**para que:** Engine x FGAC/FTA capability report (knowledge-pack driven).

- **por que:** inteligência de governança Lake Formation
- **quando usar:** revisar camadas de acesso Lake Formation

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

**para que:** Producer/consumer view: external accounts, RAM shares, links.

- **por que:** inteligência de governança Lake Formation
- **quando usar:** revisar camadas de acesso Lake Formation

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

**para que:** Run LF### checks against the project.

- **por que:** inteligência de governança Lake Formation
- **quando usar:** revisar camadas de acesso Lake Formation

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

**para que:** Governance graph view: principal -> resource edges.

- **por que:** inteligência de governança Lake Formation
- **quando usar:** revisar camadas de acesso Lake Formation

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

**para que:** Census: databases, tables, locations, tags, filters, links, shares.

- **por que:** inteligência de governança Lake Formation
- **quando usar:** revisar camadas de acesso Lake Formation

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

**para que:** Grant table: principal x permissions x resource.

- **por que:** inteligência de governança Lake Formation
- **quando usar:** revisar camadas de acesso Lake Formation

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

**para que:** Lambda function/trigger intelligence.

- **por que:** inteligência de funções Lambda e triggers
- **quando usar:** revisar funções Lambda e gatilhos declarados

**Syntax**

```text
forge-doctor-data lambda
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `lambda findings`

- **por que:** inteligência de funções Lambda e triggers
- **quando usar:** revisar funções Lambda e gatilhos declarados

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

**para que:** Functions, runtimes, triggers, destinations, idempotency evidence.

- **por que:** inteligência de funções Lambda e triggers
- **quando usar:** revisar funções Lambda e gatilhos declarados

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

**para que:** Static lineage: which jobs read/write which datasets.

- **por que:** lineage estático: quais jobs leem/escrevem quais datasets
- **quando usar:** mapear fluxo de dados entre jobs e datasets

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

**para que:** Start a stdio LSP server (requires the optional 'lsp' extra).

- **por que:** servidor LSP stdio (extra opcional 'lsp')
- **quando usar:** integrar o doctor a um editor via LSP

**Syntax**

```text
forge-doctor-data lsp
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## mcp

### `mcp`

**para que:** Start a zero-dep MCP (JSON-RPC stdio) server for agent integrations.

- **por que:** servidor MCP zero-dep (JSON-RPC stdio) para integrações de agente
- **quando usar:** servir o doctor via MCP a hosts

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

**para que:** Migration intelligence.

- **por que:** inteligência de migração
- **quando usar:** avaliar migrações entre plataformas/runtimes

**Syntax**

```text
forge-doctor-data migrate
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `migrate explain`

**para que:** Explain why each service mapped the way it did (spec 234).

Per concept: logical concept, mapping/lossiness, capability gaps the
target pack cannot satisfy, missing evidence, and the source-side
facts that anchored the mapping.

- **por que:** inteligência de migração
- **quando usar:** avaliar migrações entre plataformas/runtimes

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

**para que:** Glue migration report: knowledge changes + this project's real signals.

- **por que:** inteligência de migração
- **quando usar:** avaliar migrações entre plataformas/runtimes

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

**para que:** Enumerate migration plans; --from/--to build a cross-platform plan.

- **por que:** inteligência de migração
- **quando usar:** avaliar migrações entre plataformas/runtimes

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

**para que:** Neptune Database + Analytics intelligence.

- **por que:** inteligência Neptune Database + Analytics
- **quando usar:** revisar clusters/queries Neptune

**Syntax**

```text
forge-doctor-data neptune
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `neptune analyze-explain`

**para que:** Alias of `explain` (spec 179 names both entry points).

- **por que:** inteligência Neptune Database + Analytics
- **quando usar:** revisar clusters/queries Neptune

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

**para que:** Query-language vs graph-paradigm compatibility via registry.

- **por que:** inteligência Neptune Database + Analytics
- **quando usar:** revisar clusters/queries Neptune

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

**para que:** Analyze a user-supplied explain/profile file (offline).

- **por que:** inteligência Neptune Database + Analytics
- **quando usar:** revisar clusters/queries Neptune

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

**para que:** Bulk-loader usage and ingestion-relevant config.

- **por que:** inteligência Neptune Database + Analytics
- **quando usar:** revisar clusters/queries Neptune

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

**para que:** Clusters, instances, endpoints, languages, product split.

- **por que:** inteligência Neptune Database + Analytics
- **quando usar:** revisar clusters/queries Neptune

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

**para que:** Per-query shape inventory (language, selectivity, bounds).

- **por que:** inteligência Neptune Database + Analytics
- **quando usar:** revisar clusters/queries Neptune

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

**para que:** Graph schema facts (labels, endpoints) seen by Neptune queries.

- **por que:** inteligência Neptune Database + Analytics
- **quando usar:** revisar clusters/queries Neptune

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

**para que:** Canonical platform vocabulary (entity/rel kinds, planes, domains). Bare: Print the canonical vocabulary (entity kinds, rel kinds, evidence

- **por que:** vocabulário canônico da plataforma (entity/rel kinds, planes, domains)
- **quando usar:** conferir o vocabulário antes de depender dele

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

**para que:** Data-access patterns the ontology distinguishes.

- **por que:** vocabulário canônico da plataforma (entity/rel kinds, planes, domains)
- **quando usar:** conferir o vocabulário antes de depender dele

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

**para que:** Platform implementations mapped onto vendor-neutral kinds (spec 230).

- **por que:** vocabulário canônico da plataforma (entity/rel kinds, planes, domains)
- **quando usar:** conferir o vocabulário antes de depender dele

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

**para que:** Validate a project's platform graph against the ontology vocabulary.

Reports entities whose free-text producer domain is outside the
vocabulary; enum-constrained fields (kind, rel kind, evidence plane)
cannot drift by construction.

- **por que:** vocabulário canônico da plataforma (entity/rel kinds, planes, domains)
- **quando usar:** conferir o vocabulário antes de depender dele

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

**para que:** Workload intents and the platform kinds that can serve them.

- **por que:** vocabulário canônico da plataforma (entity/rel kinds, planes, domains)
- **quando usar:** conferir o vocabulário antes de depender dele

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

**para que:** Optimization candidates + multi-objective opportunities. Bare: Enumerate optimization candidates (v1) when no subcommand given.

- **por que:** candidatos de otimização + oportunidades multi-objetivo
- **quando usar:** depois do scan: priorizar otimizações com evidência

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

**para que:** Full detail for one opportunity: effects, tradeoffs, guardrails.

- **por que:** candidatos de otimização + oportunidades multi-objetivo
- **quando usar:** depois do scan: priorizar otimizações com evidência

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

**para que:** Multi-objective opportunities with guardrails + tradeoffs.

- **por que:** candidatos de otimização + oportunidades multi-objetivo
- **quando usar:** depois do scan: priorizar otimizações com evidência

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

**para que:** Parquet intelligence: inspect.

- **por que:** inteligência Parquet
- **quando usar:** revisar layout/datasets Parquet

**Syntax**

```text
forge-doctor-data parquet
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `parquet inspect`

**para que:** Summarize the project's Parquet surface from the semantic model.

- **por que:** inteligência Parquet
- **quando usar:** revisar layout/datasets Parquet

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

**para que:** Canonical platform graph.

- **por que:** grafo canônico da plataforma
- **quando usar:** consultar o grafo materializado da plataforma

**Syntax**

```text
forge-doctor-data platform
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `platform blast-radius`

**para que:** Entities impacted by a change to ``query`` (semantic direction).

- **por que:** grafo canônico da plataforma
- **quando usar:** consultar o grafo materializado da plataforma

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

**para que:** Cross-domain platform findings (PLAT### rules).

- **por que:** grafo canônico da plataforma
- **quando usar:** consultar o grafo materializado da plataforma

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

**para que:** Entity/relationship census of the canonical platform graph.

- **por que:** grafo canônico da plataforma
- **quando usar:** consultar o grafo materializado da plataforma

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

**para que:** Inspect and validate external plugins. Bare: List built-in categories and discovered external plugins.

- **por que:** inspeciona e valida plugins externos
- **quando usar:** verificar plugins instalados e conformidade

**Syntax**

```text
forge-doctor-data plugins
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `plugins doctor`

**para que:** Per-plugin health: entry point resolves, api_version supported.

- **por que:** inspeciona e valida plugins externos
- **quando usar:** verificar plugins instalados e conformidade

**Syntax**

```text
forge-doctor-data plugins doctor
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `plugins init`

**para que:** Scaffold a plugin package (pyproject + check + test) under dest/name.

- **por que:** inspeciona e valida plugins externos
- **quando usar:** verificar plugins instalados e conformidade

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

**para que:** Install a plugin via pipx inject (or pip), then validate loading.

- **por que:** inspeciona e valida plugins externos
- **quando usar:** verificar plugins instalados e conformidade

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

**para que:** List installed plugins with API version and load/trust status.

- **por que:** inspeciona e valida plugins externos
- **quando usar:** verificar plugins instalados e conformidade

**Syntax**

```text
forge-doctor-data plugins list
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `plugins lock`

**para que:** Pin every installed plugin's content digest to .forge-doctor-data/plugins.lock.

- **por que:** inspeciona e valida plugins externos
- **quando usar:** verificar plugins instalados e conformidade

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

**para que:** Fail when any installed plugin is incompatible or unloadable.

- **por que:** inspeciona e valida plugins externos
- **quando usar:** verificar plugins instalados e conformidade

**Syntax**

```text
forge-doctor-data plugins validate
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `plugins verify`

**para que:** Verify installed plugins against .forge-doctor-data/plugins.lock.

- **por que:** inspeciona e valida plugins externos
- **quando usar:** verificar plugins instalados e conformidade

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

**para que:** Organization policy packs.

- **por que:** packs de política de organização
- **quando usar:** avaliar políticas organizacionais declaradas

**Syntax**

```text
forge-doctor-data policy
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `policy eval`

**para que:** Evaluate policy packs and print violations (exit 1 on errors/violations).

- **por que:** packs de política de organização
- **quando usar:** avaliar políticas organizacionais declaradas

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

**para que:** List discovered policy packs and their rules.

- **por que:** packs de política de organização
- **quando usar:** avaliar políticas organizacionais declaradas

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

**para que:** Compliance report: packs, violations by rule, suppression audit.

- **por que:** packs de política de organização
- **quando usar:** avaliar políticas organizacionais declaradas

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

**para que:** Lint a policy pack file: schema, duplicate ids, regexes, severities.

- **por que:** packs de política de organização
- **quando usar:** avaliar políticas organizacionais declaradas

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

**para que:** Project self-inspection: generated status and doc-drift checks.

- **por que:** auto-inspeção do projeto: status gerado e checks de doc-drift
- **quando usar:** verificar o próprio projeto e drift de documentação

**Syntax**

```text
forge-doctor-data project
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `project status`

**para que:** Deterministic project status from source registries.

Same inputs → same bytes: commands, checks, contracts, MCP tools,
knowledge domains, and Loop Factory state are all read from their
source of truth, sorted, and rendered without timestamps.

- **por que:** auto-inspeção do projeto: status gerado e checks de doc-drift
- **quando usar:** verificar o próprio projeto e drift de documentação

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

**para que:** Run only python checks.

- **por que:** roda só checks de python
- **quando usar:** escopo de checks de código Python

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

**para que:** Data quality: Deequ/GX/SodaCL/dbt suites, coverage, gate wiring.

- **por que:** qualidade de dado: Deequ/GX/SodaCL/dbt suites, cobertura, gate wiring
- **quando usar:** revisar onde e como o dado é validado

**Syntax**

```text
forge-doctor-data quality
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `quality inspect`

**para que:** Print declared suites, coverage map, and gate wiring.

- **por que:** qualidade de dado: Deequ/GX/SodaCL/dbt suites, cobertura, gate wiring
- **quando usar:** revisar onde e como o dado é validado

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

**para que:** Redshift intelligence: inspect the vendor model.

- **por que:** inteligência Redshift: inspeciona o modelo do vendor
- **quando usar:** revisar clusters/queries Redshift

**Syntax**

```text
forge-doctor-data redshift
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `redshift inspect`

**para que:** Print the Redshift model: compute, relations, WLM, exports.

- **por que:** inteligência Redshift: inspeciona o modelo do vendor
- **quando usar:** revisar clusters/queries Redshift

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

**para que:** End-to-end SLO & critical-path intelligence.

- **por que:** inteligência de SLO e caminho crítico end-to-end
- **quando usar:** avaliar confiabilidade com evidência

**Syntax**

```text
forge-doctor-data reliability
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `reliability path`

**para que:** Critical paths over data-flow edges with per-segment coverage.

- **por que:** inteligência de SLO e caminho crítico end-to-end
- **quando usar:** avaliar confiabilidade com evidência

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

**para que:** SLO budgets + SLO001-006 findings over critical paths.

- **por que:** inteligência de SLO e caminho crítico end-to-end
- **quando usar:** avaliar confiabilidade com evidência

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

**para que:** Print deterministic remediation plans for findings / root causes.

- **por que:** planos de remediação determinísticos para findings/root causes
- **quando usar:** obter o plano de correção de um finding

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

**para que:** Run only repository checks.

- **por que:** roda só checks de repository
- **quando usar:** escopo de checks do repositório

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

**para que:** Correlate scan findings with runtime evidence into causal clusters.

- **por que:** correlaciona findings de scan com evidência de runtime em clusters causais
- **quando usar:** priorizar pela causa, não pela ordem de emissão

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

**para que:** Offline runtime evidence (exported artifacts).

- **por que:** evidência de runtime offline (artefatos exportados)
- **quando usar:** analisar evidência de runtime exportada

**Syntax**

```text
forge-doctor-data runtime
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `runtime baseline`

**para que:** Robust baselines (median/p95/MAD) per fingerprint or recorded series.

- **por que:** evidência de runtime offline (artefatos exportados)
- **quando usar:** analisar evidência de runtime exportada

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

**para que:** Capacity/saturation signals + trends over recorded history (CAP001-007).

Threshold provenance is config > platform pack > baseline — an
unthresholded dimension reports UNKNOWN, never a global rule.

- **por que:** evidência de runtime offline (artefatos exportados)
- **quando usar:** analisar evidência de runtime exportada

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

**para que:** Correlate recorded change events with regression episodes.

Evidence-gated: a correlation is reported only when at least two
evidence legs hold (temporal proximity, entity overlap, graph path,
metric relevance).  Language stays 'correlated with' — never cause.

- **por que:** evidência de runtime offline (artefatos exportados)
- **quando usar:** analisar evidência de runtime exportada

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

**para que:** Derive technical cost drivers + COST findings (never prices).

- **por que:** evidência de runtime offline (artefatos exportados)
- **quando usar:** analisar evidência de runtime exportada

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

**para que:** Match the artifact's errors against known error signatures.

- **por que:** evidência de runtime offline (artefatos exportados)
- **quando usar:** analisar evidência de runtime exportada

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

**para que:** Normalize an exported artifact into QueryExecution spines.

- **por que:** evidência de runtime offline (artefatos exportados)
- **quando usar:** analisar evidência de runtime exportada

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

**para que:** Record an artifact batch and/or list recorded history series.

With ``artifact``, the normalized executions are appended as one
compact JSONL snapshot under ``.forge-doctor-data/execution-history/``
(metrics + fingerprints only — never raw logs or SQL).  Without an
artifact, the stored series are listed.

- **por que:** evidência de runtime offline (artefatos exportados)
- **quando usar:** analisar evidência de runtime exportada

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

**para que:** Normalize one artifact into runtime facts (offline).

- **por que:** evidência de runtime offline (artefatos exportados)
- **quando usar:** analisar evidência de runtime exportada

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

**para que:** Derive performance signals + PERF findings from an artifact.

- **por que:** evidência de runtime offline (artefatos exportados)
- **quando usar:** analisar evidência de runtime exportada

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

**para que:** Baseline-aware regression detection (PERFREG001-009).

Compares each series' latest window against its own historical
baseline — a single slow run reports as a candidate (INFO), only
persistent breaches warn.

- **por que:** evidência de runtime offline (artefatos exportados)
- **quando usar:** analisar evidência de runtime exportada

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

**para que:** Reliability models, delivery semantics, objectives + REL findings.

- **por que:** evidência de runtime offline (artefatos exportados)
- **quando usar:** analisar evidência de runtime exportada

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

**para que:** Per-series trend direction for one metric (rising/falling/stable).

- **por que:** evidência de runtime offline (artefatos exportados)
- **quando usar:** analisar evidência de runtime exportada

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

**para que:** Emit a CycloneDX 1.5 SBOM: deps, plugins, knowledge packs, images.

- **por que:** emite SBOM CycloneDX 1.5: deps, plugins, knowledge packs, imagens
- **quando usar:** inventário de suprimentos para auditoria/supply chain

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

**para que:** Scan a project for data-engineering problems.

- **por que:** scaneia um projeto atrás de problemas de engenharia de dados
- **quando usar:** primeira passada num repo — produz findings

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

**para que:** Schema extraction and diffing.

- **por que:** extração e diff de schema
- **quando usar:** extrair ou comparar schemas

**Syntax**

```text
forge-doctor-data schema
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `schema contracts`

**para que:** Dump the JSON Schemas for Forge Doctor Data's public artifacts.

- **por que:** extração e diff de schema
- **quando usar:** extrair ou comparar schemas

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

**para que:** Diff two schema files, or all schema files across a git range.

- **por que:** extração e diff de schema
- **quando usar:** extrair ou comparar schemas

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

**para que:** Search platforms: OpenSearch/Elasticsearch indices, policies, domains.

- **por que:** plataformas de busca: índices, políticas, domínios OpenSearch/Elasticsearch
- **quando usar:** revisar serviços de busca detectados

**Syntax**

```text
forge-doctor-data search
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `search inspect`

**para que:** Print the search model: indices/templates, policies, pipelines, domains.

- **por que:** plataformas de busca: índices, políticas, domínios OpenSearch/Elasticsearch
- **quando usar:** revisar serviços de busca detectados

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

**para que:** Snowflake intelligence: inspect the vendor model.

- **por que:** inteligência Snowflake: inspeciona o modelo do vendor
- **quando usar:** revisar warehouses/queries Snowflake

**Syntax**

```text
forge-doctor-data snowflake
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `snowflake inspect`

**para que:** Print the Snowflake model: warehouses, objects, exports, copies.

- **por que:** inteligência Snowflake: inspeciona o modelo do vendor
- **quando usar:** revisar warehouses/queries Snowflake

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

**para que:** Spark checks and runtime diagnosis. Bare: Run only spark checks (default) or a runtime subcommand.

- **por que:** checks Spark e diagnóstico de runtime
- **quando usar:** escopo de checks Spark ou diagnóstico de runtime Spark

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

**para que:** Analyze a Spark event log (JSONL) for runtime problems.

- **por que:** checks Spark e diagnóstico de runtime
- **quando usar:** escopo de checks Spark ou diagnóstico de runtime Spark

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

**para que:** Fingerprint a Spark log against error packs and runtime signatures.

- **por que:** checks Spark e diagnóstico de runtime
- **quando usar:** escopo de checks Spark ou diagnóstico de runtime Spark

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

**para que:** Scan a Spark physical plan for pathological operators.

- **por que:** checks Spark e diagnóstico de runtime
- **quando usar:** escopo de checks Spark ou diagnóstico de runtime Spark

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

**para que:** Step Functions intelligence.

- **por que:** inteligência Step Functions
- **quando usar:** revisar state machines e execuções

**Syntax**

```text
forge-doctor-data stepfunctions
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `stepfunctions inspect`

**para que:** Summarize Step Functions definitions from the semantic model.

- **por que:** inteligência Step Functions
- **quando usar:** revisar state machines e execuções

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

**para que:** Streaming intelligence.

- **por que:** inteligência de streaming
- **quando usar:** revisar plataformas de streaming detectadas

**Syntax**

```text
forge-doctor-data streaming
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `streaming diagnose`

**para que:** Deterministic runtime diagnostics over a progress batch series.

- **por que:** inteligência de streaming
- **quando usar:** revisar plataformas de streaming detectadas

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

**para que:** Summarize streaming queries from the semantic model.

- **por que:** inteligência de streaming
- **quando usar:** revisar plataformas de streaming detectadas

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

**para que:** Summarize a Structured Streaming progress artifact (offline).

- **por que:** inteligência de streaming
- **quando usar:** revisar plataformas de streaming detectadas

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

**para que:** Derived delivery semantics per streaming query.

- **por que:** inteligência de streaming
- **quando usar:** revisar plataformas de streaming detectadas

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

**para que:** Audit configured suppressions: ACTIVE / EXPIRED / UNUSED.

- **por que:** audita suppressions configuradas: ACTIVE/EXPIRED/UNUSED
- **quando usar:** verificar o que está suprimido e por quê

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

**para que:** Terraform intelligence: inspect.

- **por que:** inteligência Terraform
- **quando usar:** revisar HCL/plan de plataformas de dados

**Syntax**

```text
forge-doctor-data terraform
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `terraform inspect`

**para que:** Summarize the project's Terraform surface from the semantic model.

- **por que:** inteligência Terraform
- **quando usar:** revisar HCL/plan de plataformas de dados

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

**para que:** Explain ONE finding: evidence, enclosing symbol, receiver chain.

- **por que:** explica UM finding: evidência, símbolo, cadeia de receiver
- **quando usar:** entender um finding específico a fundo

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

**para que:** Trino intelligence: inspect catalogs, coordinator, lineage.

- **por que:** inteligência Trino: catálogos, coordinator, lineage
- **quando usar:** revisar clusters/queries Trino

**Syntax**

```text
forge-doctor-data trino
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `trino inspect`

**para que:** Print the Trino model: catalogs, coordinator flags, SQL refs.

- **por que:** inteligência Trino: catálogos, coordinator, lineage
- **quando usar:** revisar clusters/queries Trino

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

**para que:** Formal digital twin: validated platform snapshot.

- **por que:** digital twin formal: snapshot validado da plataforma
- **quando usar:** materializar um twin validado para análise

**Syntax**

```text
forge-doctor-data twin
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

### `twin diff`

**para que:** Diff two twin-state snapshots: entities, rels, capabilities, drift.

- **por que:** digital twin formal: snapshot validado da plataforma
- **quando usar:** materializar um twin validado para análise

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

**para que:** Show one entity across all five states.

- **por que:** digital twin formal: snapshot validado da plataforma
- **quando usar:** materializar um twin validado para análise

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

**para que:** Emit the deterministic twin snapshot artifact.

- **por que:** digital twin formal: snapshot validado da plataforma
- **quando usar:** materializar um twin validado para análise

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

**para que:** List state-tagged facts the twin collected.

- **por que:** digital twin formal: snapshot validado da plataforma
- **quando usar:** materializar um twin validado para análise

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

**para que:** Twin summary + invariant report. Exit 1 on hard violations.

- **por que:** digital twin formal: snapshot validado da plataforma
- **quando usar:** materializar um twin validado para análise

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

**para que:** Reconcile the five states: every (entity, property) divergence.

- **por que:** digital twin formal: snapshot validado da plataforma
- **quando usar:** materializar um twin validado para análise

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

**para que:** Persist a five-state twin snapshot into the project history dir.

- **por que:** digital twin formal: snapshot validado da plataforma
- **quando usar:** materializar um twin validado para análise

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

**para que:** Print the installed Forge Doctor Data version.

- **por que:** imprime a versão instalada do Forge Doctor Data
- **quando usar:** confirmar qual build está rodando

**Syntax**

```text
forge-doctor-data version
```

<!-- keep:start -->
_free notes — errors, examples, next steps (hand-written, preserved)_
<!-- keep:end -->

## what-if

### `what-if`

**para que:** Evaluate a hypothetical change without executing it. Bare: Evaluate --change target=value specs against the project.

- **por que:** avalia uma mudança hipotética sem executá-la
- **quando usar:** ensaiar impacto de mudança sem mutar nada

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

**para que:** Discover and orchestrate sub-projects. Bare: Discover sub-projects (pyproject.toml) under a workspace root.

- **por que:** descobre e orquestra sub-projetos
- **quando usar:** operar multi-projeto num escopo declarado

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

**para que:** Per-subproject finding diff across a git range.

- **por que:** descobre e orquestra sub-projetos
- **quando usar:** operar multi-projeto num escopo declarado

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

**para que:** Build the WorkspaceModel: repos, merged platform graph, cross-repo links.

- **por que:** descobre e orquestra sub-projetos
- **quando usar:** operar multi-projeto num escopo declarado

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

**para que:** Scan every nested project and aggregate results with a project column.

- **por que:** descobre e orquestra sub-projetos
- **quando usar:** operar multi-projeto num escopo declarado

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
