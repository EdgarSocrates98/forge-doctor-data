"""Cross-doctor conformance checking for ``forge-contracts/1`` payloads (spec 267).

Two-layer check so any Forge product can validate a payload the same way:

1. **Schema layer** - the published JSON Schemas in
   ``contracts.schemas.FORGE_CONTRACT_SCHEMAS`` (shape, required keys, types).
2. **Model layer** - ``ContractModel.from_dict()`` (strict null semantics,
   normalized decode) plus version negotiation.

The ``contracts`` package itself stays dependency-free: this module is the
engine-side tool that other products can invoke via
``forge-doctor-data contracts conformance``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from forge_doctor_data.contracts import models as contract_models
from forge_doctor_data.contracts.schemas import FORGE_CONTRACT_SCHEMAS
from forge_doctor_data.contracts.version import negotiate
from forge_doctor_data.core.contract_check import validate

CONTRACT_KINDS: dict[str, type[contract_models.ContractModel]] = {
    "entity": contract_models.Entity,
    "relationship": contract_models.Relationship,
    "evidence": contract_models.Evidence,
    "finding": contract_models.Finding,
    "capability": contract_models.Capability,
    "unknown-fact": contract_models.UnknownFact,
    "migration-plan": contract_models.MigrationPlan,
    "remediation-plan": contract_models.RemediationPlan,
    "handoff": contract_models.HandoffBundle,
    "diagnostic-manifest": contract_models.DiagnosticManifest,
}

# Kind-detection fingerprints, ordered most-specific first. Each entry is the
# set of keys that must ALL be present to identify the payload.
_FINGERPRINTS: tuple[tuple[str, frozenset[str]], ...] = (
    ("remediation-plan", frozenset({"id", "check_id", "problem"})),
    ("finding", frozenset({"check_id", "title", "severity", "category", "message"})),
    ("migration-plan", frozenset({"id", "source", "target", "kind"})),
    ("unknown-fact", frozenset({"subject", "kind", "reason"})),
    ("relationship", frozenset({"src", "dst", "kind"})),
    ("evidence", frozenset({"ref", "kind", "source"})),
    ("capability", frozenset({"id", "domain", "status"})),
    ("entity", frozenset({"id", "kind", "domain"})),
    ("handoff", frozenset({"tool", "project", "summary"})),
    ("diagnostic-manifest", frozenset({"tool", "domains"})),
)


@dataclass(frozen=True)
class ConformanceResult:
    """Verdict for one payload against ``forge-contracts/1``."""

    kind: str | None
    valid: bool
    errors: tuple[str, ...] = ()
    negotiated_version: str | None = None
    warnings: tuple[str, ...] = field(default=())

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract": "forge-contracts/1",
            "kind": self.kind,
            "valid": self.valid,
            "negotiated_version": self.negotiated_version,
            "errors": sorted(self.errors),
            "warnings": sorted(self.warnings),
        }


def detect_kind(payload: Any) -> str | None:
    """Best-effort kind detection from the payload's required-key fingerprint."""
    if not isinstance(payload, dict):
        return None
    keys = set(payload)
    for kind, fingerprint in _FINGERPRINTS:
        if fingerprint <= keys:
            return kind
    return None


def check_conformance(payload: Any, kind: str | None = None) -> ConformanceResult:
    """Validate ``payload`` against ``forge-contracts/1`` (schema + model)."""
    if not isinstance(payload, dict):
        return ConformanceResult(
            kind=None,
            valid=False,
            errors=(f"payload is {type(payload).__name__}, expected object",),
        )

    detected = kind or detect_kind(payload)
    if detected is None:
        return ConformanceResult(
            kind=None,
            valid=False,
            errors=(f"cannot determine contract kind (valid: {', '.join(CONTRACT_KINDS)})",),
        )
    if detected not in CONTRACT_KINDS:
        return ConformanceResult(
            kind=detected,
            valid=False,
            errors=(f"unknown kind {detected!r} (valid: {', '.join(CONTRACT_KINDS)})",),
        )

    errors: list[str] = []
    warnings: list[str] = []

    errors.extend(validate(payload, FORGE_CONTRACT_SCHEMAS[detected]))

    try:
        CONTRACT_KINDS[detected].from_dict(payload)
    except (ValueError, TypeError, AttributeError) as exc:
        errors.append(f"model parse: {exc}")

    negotiated: str | None = None
    raw_version = payload.get("contract_version", "forge-contracts/1")
    if raw_version is not None:
        try:
            version = negotiate(str(raw_version))
            if version is None:
                errors.append(f"version: {raw_version!r} is outside the supported window")
            else:
                negotiated = str(version)
        except ValueError as exc:
            errors.append(f"version: {exc}")

    return ConformanceResult(
        kind=detected,
        valid=not errors,
        errors=tuple(sorted(set(errors))),
        negotiated_version=negotiated,
        warnings=tuple(warnings),
    )


def _fixtures_dir() -> Any:
    import importlib.resources as res

    return res.files("forge_doctor_data.contracts").joinpath("fixtures")


def load_fixture(name: str) -> dict[str, Any]:
    """Read a bundled canonical fixture via importlib.resources."""
    fixture = _fixtures_dir().joinpath(f"{name}.json")
    return json.loads(fixture.read_text(encoding="utf-8"))  # type: ignore[no-any-return]


def check_fixtures() -> dict[str, ConformanceResult]:
    """Conformance-check every bundled fixture (self-test)."""
    results: dict[str, ConformanceResult] = {}
    for entry in _fixtures_dir().iterdir():
        if not entry.name.endswith(".json"):
            continue
        name = entry.name[: -len(".json")]
        results[name] = check_conformance(json.loads(entry.read_text(encoding="utf-8")), name)
    return results
