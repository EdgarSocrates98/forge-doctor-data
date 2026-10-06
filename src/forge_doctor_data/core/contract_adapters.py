"""Engine → contract conversion (P16).

Contracts live in ``forge_doctor_data.contracts`` (dependency-free,
JSON-native). This module is the one place engine types are translated
into wire models - the dependency points engine → contracts, never
backwards, so contract consumers stay decoupled from internals.
"""

from __future__ import annotations

from forge_doctor_data.contracts import (
    Capability,
    DiagnosticManifest,
)
from forge_doctor_data.contracts import (
    Entity as ContractEntity,
)
from forge_doctor_data.contracts import (
    Finding as ContractFinding,
)
from forge_doctor_data.contracts import (
    Relationship as ContractRelationship,
)
from forge_doctor_data.core.capabilities import CapabilityResult
from forge_doctor_data.core.models import CheckResult, ScanReport
from forge_doctor_data.core.platform_graph import Entity, Relationship


def finding_contract(result: CheckResult) -> ContractFinding:
    """Wire ``Finding`` for one ``CheckResult``."""
    return ContractFinding(
        check_id=result.check_id,
        title=result.title,
        severity=result.severity.value,
        category=result.category,
        message=result.message,
        fingerprint=result.fingerprint,
        file=result.file.as_posix() if result.file is not None else None,
        line=result.line,
        column=result.column,
        end_line=result.end_line,
        end_column=result.end_column,
        recommendation=result.recommendation,
        confidence=result.confidence.value if result.confidence else None,
        evidence=result.evidence,
        evidence_kind=result.evidence_kind.value if result.evidence_kind else None,
        source=result.source,
        fixable=result.fixable,
        tags=result.tags,
    )


def entity_contract(entity: Entity) -> ContractEntity:
    return ContractEntity(
        id=entity.id,
        kind=entity.kind.value,
        domain=entity.domain,
        identifier=entity.identifier,
        name=entity.name,
        file=entity.file.as_posix() if entity.file is not None else None,
        line=entity.line,
        attrs=dict(entity.attrs),
    )


def relationship_contract(rel: Relationship) -> ContractRelationship:
    return ContractRelationship(
        src=rel.src,
        dst=rel.dst,
        kind=rel.kind.value,
        evidence_kind=rel.evidence_kind.value if rel.evidence_kind else None,
        attrs=dict(rel.attrs),
    )


def report_manifest(report: ScanReport, tool_version: str = "") -> DiagnosticManifest:
    """Summary-first ``DiagnosticManifest`` for a finished scan."""
    findings = [r for r in report.results if r.severity.value != "pass"]
    domains = sorted({r.category for r in findings})
    risks = [
        {
            "id": r.check_id,
            "severity": r.severity.value,
            "file": r.file.as_posix() if r.file else None,
            "fingerprint": r.fingerprint,
        }
        for r in findings
        if r.severity.value == "error"
    ]
    return DiagnosticManifest(
        tool_version=tool_version,
        domains=tuple(domains),
        finding_count=len(findings),
        risks=tuple(risks),
        evidence_refs=tuple(f.fingerprint for f in findings if f.fingerprint is not None),
    )


def capability_contract(result: CapabilityResult) -> Capability:
    """Wire ``Capability`` for one ``CapabilityResult``."""
    return Capability(
        id=result.capability,
        domain=result.platform,
        status=result.status.value,
        evidence_refs=(result.entry_id,) if result.entry_id else (),
    )
