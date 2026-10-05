# forge-contracts — the shared wire vocabulary

`forge_doctor_data.contracts` is the boundary every Forge product speaks
across. This document is the manifesto: what is universal, what is
domain-specific, what is wire-stable, and what is extension-only. The
rules below are pinned by tests — drift is a test failure, not a
review opinion.

## What is universal

Exactly ten model types form the frozen vocabulary. Nothing may be added
or removed without a major contract version bump:

| Type | Meaning |
|------|---------|
| `Entity` | A platform-graph node (`{kind}:{domain}:{identifier}`) |
| `Relationship` | A directed edge between two entities |
| `Evidence` | A reference to the artifact that backs a claim |
| `Finding` | One diagnostic result (id, severity, location, fingerprint) |
| `Capability` | A platform feature verdict (`supported`/`conditional`/`unsupported`/`unknown`) |
| `UnknownFact` | An honest gap: what could not be determined and why |
| `MigrationPlan` | A deterministic path between platform states |
| `RemediationPlan` | Fix actions bound to finding fingerprints |
| `HandoffBundle` | The portable scan output downstream tools consume |
| `DiagnosticManifest` | Summary-first entry point for agent contexts |

These types are *vocabulary*, not behavior: they carry data about a
platform, never producer logic. `from_dict`/`to_dict` is the only
contract a consumer needs.

## What is domain-specific

Domain knowledge lives in **data**, not in the contract shape. A
`Finding.category` may hold `spark` or `glue`; the `Finding` type itself
must never. `tests/unit/test_contract_boundaries.py` scans every
contract source file and rejects a forbidden-term list — currently
Spark, Iceberg, Kafka, Airflow, Glue, DynamoDB, Neptune, Snowflake,
BigQuery, Redshift, Databricks, Terraform, Athena, EMR, Flink, Trino,
dbt, Lambda, OpenAPI, GraphQL, `RequestExecution`, `QueryExecution`.
Adding a domain concept to a contract module fails the suite.

Equally, the package may not import the engine: any
`forge_doctor_data.*` import outside `forge_doctor_data.contracts` is a
test failure, and contract classes may not subclass engine types.

## What is wire-stable

Contract versions are `family/major` (`forge-contracts/1`). Two payloads
are wire-compatible when family *and* major match:

- additive fields never bump major;
- removed/renamed fields or changed value types always do;
- check ids and canonical entity ids are stable identifiers.

`contracts.version` exposes the negotiation window as first-class
constants — `CURRENT`, `SUPPORTED`, `SUPPORTED_MIN`, `SUPPORTED_MAX` —
plus two explicit operations:

- `negotiate(offered)` returns the common version or `None` when
  disjoint (never a silent partial decode);
- `within_range(offered)` is the forward-compat check: a newer
  supported-line reader inside `[min, max]` is still acceptable.

Every emitted payload carries `contract_version`; every decoder
normalizes it (`forge-contracts/1` and integer `1` both decode).

## What is extension-only

Producers may attach `x-*` keys — `x-forge-data`, `x-forge-api`,
`x-forge-<product>` — to any contract payload. The rules:

- **must not alter base semantics**: a payload stripped of `x-*` keys
  decodes to the same model as one that never carried them;
- **must survive round-trip when possible**: `from_dict` captures all
  `x-*` keys into `extensions` and `to_dict` re-emits them, so a
  forwarding product does not destroy data it does not understand;
- **consumers may ignore safely**: `x-*` keys are advisory metadata;
  nothing in the base contract depends on their presence.

`core/forger.py` shows the mechanism doing real work: a bounded scan
response stamps `x-forge-data` with the request kind and applied limits
alongside the `UnknownFact` truncation records.

## Conformance test kit

Another repository can validate `forge-contracts/1` payloads without
importing engine internals:

1. **Schema layer** — `forge_doctor_data.contracts.schemas.FORGE_CONTRACT_SCHEMAS`
   is the published JSON Schema set. Decode with any validator;
   `forge-doctor-data schema contracts` and
   `schema contracts <kind>` dump the same documents.
2. **Model layer** — `contracts` alone (models + schemas + version)
   decodes and re-encodes payloads with strict null semantics;
   `test_contracts_decode_without_engine_modules` proves no
   `core`/`checks`/`analyzers` module loads in the process.
3. **CLI** — `forge-doctor-data contracts conformance <payload>` runs
   both layers with kind auto-detection; canonical fixtures ship inside
   `contracts/fixtures/` for cross-repo replay.

The mutation gate (`tests/unit/test_contract_mutations.py`) kills every
single-field mutation of a valid payload — the kit refuses malformed
input deterministically, by contract version and by shape.
