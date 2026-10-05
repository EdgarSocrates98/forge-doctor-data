# Forge Ecosystem Contracts

Forge Doctor Data is the deterministic evidence engine of the Forge family.
Downstream tools (Spark Forge, API Forge, and future members) consume its
outputs without rescanning. This page is the interop contract.

## Guarantees

- **Deterministic** — identical project state produces byte-identical
  output. Bundles carry no timestamps or random ordering; entities,
  relationships, findings, and plans are sorted.
- **Stable ids** — `check_id` and `fingerprint` are stable identities:
  `check_id` never depends on message text, `fingerprint` is a semantic
  per-occurrence key (id|file|symbol|anchor) safe for joins and diffs.
- **Evidence, not guesses** — findings declare `evidence_kind`
  (`static`/`config`/`observed_metadata`/`runtime`/`derived`); capability
  statuses are `supported|unsupported|conditional|unknown`. `unknown` is
  honest, never fabricated.
- **Versioned** — `schema_version` follows the public SCHEMA_VERSION;
  the bundle also carries `contract` + `contract_version` for the bundle
  shape itself. Additive fields bump MINOR; removed/renamed fields bump
  MAJOR. Breaking changes require a new contract version.

## The contracts

`forge-doctor-data contracts list` lists them; `forge-doctor-data schema
contracts <name>` dumps the JSON Schema (draft 2020-12).

| name | artifact |
|---|---|
| `scan-report` | `scan --format json` — full scan report |
| `finding` | one result row (CheckResult serialization) |
| `evidence` | `runtime inspect --json` — normalized runtime model |
| `platform-graph` | `DataPlatformGraph.to_dict()` — entities + relationships |
| `capability-report` | `capabilities list --json` — platform → cap → status |
| `remediation-plan` | `remediate --json` — one remediation plan |
| `policy-pack` | org policy pack file |
| `lab-expected` | Forge Lab `expected.json` ground truth |
| `golden-snapshot` | golden-repo snapshot files |
| `handoff-bundle` | `export --format handoff` — the cross-tool bundle |

## The handoff bundle

```bash
forge-doctor-data export . --format handoff -o bundle.json
forge-doctor-data contracts verify bundle.json
```

Shape (stable keys, deterministic ordering):

```json
{
  "contract": "handoff-bundle",
  "contract_version": 1,
  "schema_version": "3.0",
  "tool": {"name": "forge-doctor-data", "version": "…"},
  "project": {"name": "…", "root": "…"},
  "summary": {"passed": 0, "info": 0, "warnings": 0, "errors": 0},
  "results": [ …findings sorted by (check_id, fingerprint)… ],
  "graph": {"entities": […], "relationships": […]},
  "capabilities": {"platform": {"CAPABILITY": "status"}},
  "plans": [ …remediation plans sorted by id… ]
}
```

A downstream tool receives entities, findings, capabilities, unknowns
(absence is honest — fields are present but may be empty), and
remediation candidates without rescanning.

## Verifying bundles

`forge-doctor-data contracts verify <bundle> [--contract <name>]` validates
an artifact against the published contract — `<bundle>` may be a file
path or `-` for stdin (the default when omitted). The validator covers
`type`/`required`/`properties`/`items`/`enum`/`const`/`oneOf`/
`additionalProperties`/`pattern` — a subset sufficient for the published
contracts, offline, with no `jsonschema` dependency. Exit 1 on
violations. Other Forge tools should call this in their own conformance
tests.

## Boundaries

- Contracts describe what the engine already emits — no new runtime
  behavior is invented for the contract's sake.

## Shared contract models (P16)

`forge_doctor_data.contracts` is the dependency-free, JSON-native model
layer downstream tools program against: `Entity`, `Relationship`,
`Evidence`, `Finding`, `Capability`, `UnknownFact`, `MigrationPlan`,
`RemediationPlan`, `HandoffBundle`, `DiagnosticManifest`, and
`ContractVersion` negotiation (`forge-contracts/1`). The engine
converts via `core/contract_adapters.py` — dependency direction is
always engine → contracts. These models are the seed of a standalone
`forge-contracts` distribution; extracting a separate package is a
publish-time decision, not an engine change (imports stay
`forge_doctor_data.contracts` today).

## forge-contracts/1 conformance (spec 267)

The published JSON Schemas live in `forge_doctor_data.contracts.schemas`
(pure data — any implementation can validate against them), canonical
fixtures ship in the wheel under `contracts/fixtures/`, and
`forge-doctor-data contracts conformance <file|-> [--kind K] [--fixtures]
[--json]` runs the two-layer check: schema shape + strict model decode +
version negotiation, with kind auto-detection. `contracts schema [kind]`
dumps a schema.

## The Forger boundary

`core/forger.py::accept_request` is the single request surface:
`{"kind": "scan", "path": ..., "options": {"bounded": {...}}}` in,
`HandoffBundle` out. `REQUEST_KINDS` is exactly `("scan",)` — Doctor
Data never routes, schedules, fans out, or calls another Doctor;
orchestration is The Forger's job. `options.bounded` produces a
context-economy bundle (`HandoffBundle.bounded()` records truncation as
honest `UnknownFact`s) and the emission is stamped with an
`x-forge-data` extension block. Pinned by `test_forger_boundary.py`,
including a subprocess proof that a consumer parses the bundle with
zero engine imports.
