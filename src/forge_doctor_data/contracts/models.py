"""Shared wire models for the Forge ecosystem (P16).

Dependency-free, JSON-native frozen dataclasses. These are *contract*
types - the shapes consumers (The Forger, Spark Forge, API Forge,
Claude, Codex, Devin) rely on - not engine internals. Fields are
``str | int | bool | None | dict`` only, so ``to_dict`` output is
already the JSON document.

Naming matches the published JSON Schemas (``core.schemas.SCHEMAS``):
``finding``, ``platform-graph`` entities/relationships, ``evidence``,
``capability-report``, ``remediation-plan``, ``handoff-bundle``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from forge_doctor_data.contracts.version import CURRENT

CONTRACT_VERSION = CURRENT

Json = dict[str, Any]


def _drop_none(d: Json) -> Json:
    return {k: v for k, v in d.items() if v is not None}


@dataclass(frozen=True)
class ContractModel:
    """Base: deterministic JSON (de)serialization for every contract."""

    contract_version: str = field(default=str(CURRENT))

    def to_dict(self) -> Json:  # pragma: no cover - overridden
        raise NotImplementedError

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, ensure_ascii=False)


@dataclass(frozen=True)
class Finding(ContractModel):
    """One diagnostic finding - mirrors the ``finding`` JSON schema."""

    check_id: str = ""
    title: str = ""
    severity: str = "info"  # error | warning | info | pass
    category: str = ""
    message: str = ""
    fingerprint: str | None = None
    file: str | None = None
    line: int | None = None
    column: int | None = None
    end_line: int | None = None
    end_column: int | None = None
    recommendation: str | None = None
    confidence: str | None = None
    evidence: str | None = None
    evidence_kind: str | None = None
    source: str | None = None
    fixable: bool | None = None
    tags: tuple[str, ...] = ()

    def to_dict(self) -> Json:
        return _drop_none(
            {
                "contract_version": self.contract_version,
                "check_id": self.check_id,
                "title": self.title,
                "severity": self.severity,
                "category": self.category,
                "message": self.message,
                "fingerprint": self.fingerprint,
                "file": self.file,
                "line": self.line,
                "column": self.column,
                "end_line": self.end_line,
                "end_column": self.end_column,
                "recommendation": self.recommendation,
                "confidence": self.confidence,
                "evidence": self.evidence,
                "evidence_kind": self.evidence_kind,
                "source": self.source,
                "fixable": self.fixable,
                "tags": list(self.tags),
            }
        )

    @staticmethod
    def from_dict(d: Json) -> Finding:
        return Finding(
            contract_version=d.get("contract_version", str(CURRENT)),
            check_id=d["check_id"],
            title=d["title"],
            severity=d["severity"],
            category=d["category"],
            message=d["message"],
            fingerprint=d.get("fingerprint"),
            file=d.get("file"),
            line=d.get("line"),
            column=d.get("column"),
            end_line=d.get("end_line"),
            end_column=d.get("end_column"),
            recommendation=d.get("recommendation"),
            confidence=d.get("confidence"),
            evidence=d.get("evidence"),
            evidence_kind=d.get("evidence_kind"),
            source=d.get("source"),
            fixable=d.get("fixable"),
            tags=tuple(d.get("tags", ())),
        )


@dataclass(frozen=True)
class Entity(ContractModel):
    """One platform-graph node - canonical ``{kind}:{domain}:{identifier}``."""

    id: str = ""
    kind: str = ""
    domain: str = ""
    identifier: str = ""
    name: str = ""
    file: str | None = None
    line: int | None = None
    attrs: Json = field(default_factory=dict)

    def to_dict(self) -> Json:
        return _drop_none(
            {
                "contract_version": self.contract_version,
                "id": self.id,
                "kind": self.kind,
                "domain": self.domain,
                "identifier": self.identifier,
                "name": self.name,
                "file": self.file,
                "line": self.line,
                "attrs": dict(self.attrs),
            }
        )

    @staticmethod
    def from_dict(d: Json) -> Entity:
        return Entity(
            contract_version=d.get("contract_version", str(CURRENT)),
            id=d["id"],
            kind=d["kind"],
            domain=d["domain"],
            identifier=d["identifier"],
            name=d.get("name", ""),
            file=d.get("file"),
            line=d.get("line"),
            attrs=dict(d.get("attrs", {})),
        )


@dataclass(frozen=True)
class Relationship(ContractModel):
    """Typed src→dst edge between entity ids."""

    src: str = ""
    dst: str = ""
    kind: str = ""
    evidence_kind: str | None = None
    attrs: Json = field(default_factory=dict)

    def to_dict(self) -> Json:
        return _drop_none(
            {
                "contract_version": self.contract_version,
                "src": self.src,
                "dst": self.dst,
                "kind": self.kind,
                "evidence_kind": self.evidence_kind,
                "attrs": dict(self.attrs),
            }
        )

    @staticmethod
    def from_dict(d: Json) -> Relationship:
        return Relationship(
            contract_version=d.get("contract_version", str(CURRENT)),
            src=d["src"],
            dst=d["dst"],
            kind=d["kind"],
            evidence_kind=d.get("evidence_kind"),
            attrs=dict(d.get("attrs", {})),
        )


@dataclass(frozen=True)
class Evidence(ContractModel):
    """A lazy-detail pointer consumers can resolve later."""

    ref: str = ""
    kind: str = ""
    source: str = ""
    detail: str | None = None

    def to_dict(self) -> Json:
        return _drop_none(
            {
                "contract_version": self.contract_version,
                "ref": self.ref,
                "kind": self.kind,
                "source": self.source,
                "detail": self.detail,
            }
        )

    @staticmethod
    def from_dict(d: Json) -> Evidence:
        return Evidence(
            contract_version=d.get("contract_version", str(CURRENT)),
            ref=d["ref"],
            kind=d["kind"],
            source=d["source"],
            detail=d.get("detail"),
        )


@dataclass(frozen=True)
class Capability(ContractModel):
    """One capability assessment - mirrors ``capability-report`` entries."""

    id: str = ""
    domain: str = ""
    status: str = ""  # e.g. supported | partial | unsupported | unknown
    confidence: str | None = None
    evidence_refs: tuple[str, ...] = ()

    def to_dict(self) -> Json:
        return _drop_none(
            {
                "contract_version": self.contract_version,
                "id": self.id,
                "domain": self.domain,
                "status": self.status,
                "confidence": self.confidence,
                "evidence_refs": list(self.evidence_refs),
            }
        )

    @staticmethod
    def from_dict(d: Json) -> Capability:
        return Capability(
            contract_version=d.get("contract_version", str(CURRENT)),
            id=d["id"],
            domain=d["domain"],
            status=d["status"],
            confidence=d.get("confidence"),
            evidence_refs=tuple(d.get("evidence_refs", ())),
        )


@dataclass(frozen=True)
class MigrationPlan(ContractModel):
    """A deterministic migration path - mirrors ``remediation-plan`` plans."""

    id: str = ""
    source: str = ""
    target: str = ""
    kind: str = ""  # platform_upgrade | cross_platform | format_change
    readiness: str | None = None
    steps: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()

    def to_dict(self) -> Json:
        return _drop_none(
            {
                "contract_version": self.contract_version,
                "id": self.id,
                "source": self.source,
                "target": self.target,
                "kind": self.kind,
                "readiness": self.readiness,
                "steps": list(self.steps),
                "risks": list(self.risks),
            }
        )

    @staticmethod
    def from_dict(d: Json) -> MigrationPlan:
        return MigrationPlan(
            contract_version=d.get("contract_version", str(CURRENT)),
            id=d["id"],
            source=d["source"],
            target=d["target"],
            kind=d["kind"],
            readiness=d.get("readiness"),
            steps=tuple(d.get("steps", ())),
            risks=tuple(d.get("risks", ())),
        )


def _version_str(value: object) -> str:
    """Wire ``contract_version`` may be ``forge-contracts/1`` or the
    integer ``1`` used by the handoff-bundle schema - both normalize
    to the canonical string form."""
    if isinstance(value, int):
        return f"forge-contracts/{value}"
    return str(value) if value else str(CURRENT)


@dataclass(frozen=True)
class RemediationPlan(ContractModel):
    """Deterministic fix actions bound to finding fingerprints."""

    id: str = ""
    check_id: str = ""
    problem: str = ""
    targets: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    requires_approval: bool = False

    def to_dict(self) -> Json:
        return _drop_none(
            {
                "contract_version": self.contract_version,
                "id": self.id,
                "check_id": self.check_id,
                "problem": self.problem,
                "targets": list(self.targets),
                "actions": list(self.actions),
                "risks": list(self.risks),
                "requires_approval": self.requires_approval,
            }
        )

    @staticmethod
    def from_dict(d: Json) -> RemediationPlan:
        # Wire actions are objects ({id, description,...}); the contract
        # surface is their descriptions.
        actions = tuple(
            a.get("description", "") if isinstance(a, dict) else str(a)
            for a in d.get("actions", ())
        )
        return RemediationPlan(
            contract_version=_version_str(d.get("contract_version")),
            id=d.get("id", ""),
            check_id=d.get("check_id", ""),
            problem=d.get("problem", ""),
            targets=tuple(d.get("targets", ())),
            actions=actions,
            risks=tuple(d.get("risks", ())),
            requires_approval=bool(d.get("requires_approval", False)),
        )


@dataclass(frozen=True)
class HandoffBundle(ContractModel):
    """Portable scan output for downstream Forge tools (``handoff-bundle``)."""

    tool: str = "forge-doctor-data"
    tool_version: str = ""
    project: Json = field(default_factory=dict)
    summary: Json = field(default_factory=dict)
    findings: tuple[Finding, ...] = ()
    entities: tuple[Entity, ...] = ()
    relationships: tuple[Relationship, ...] = ()
    capabilities: tuple[Capability, ...] = ()
    plans: tuple[RemediationPlan, ...] = ()

    def to_dict(self) -> Json:
        return {
            "contract_version": self.contract_version,
            "tool": {"name": self.tool, "version": self.tool_version},
            "project": self.project,
            "summary": self.summary,
            "findings": [f.to_dict() for f in self.findings],
            "entities": [e.to_dict() for e in self.entities],
            "relationships": [r.to_dict() for r in self.relationships],
            "capabilities": [c.to_dict() for c in self.capabilities],
            "plans": [p.to_dict() for p in self.plans],
        }

    @staticmethod
    def from_dict(d: Json) -> HandoffBundle:
        """Deserialize the emitted wire shape (``handoff-bundle`` schema).

        The bundle nests entities/relationships under ``graph``, findings
        under ``results``, and capabilities as ``{platform: {cap: status}}``;
        top-level keys are also accepted for forward compatibility.
        """
        tool = d.get("tool", {})
        graph = d.get("graph", {})
        capabilities = d.get("capabilities", ())
        if isinstance(capabilities, dict):
            caps = tuple(
                Capability(id=cap, domain=platform, status=str(status))
                for platform, entries in sorted(capabilities.items())
                for cap, status in sorted(entries.items())
            )
        else:
            caps = tuple(Capability.from_dict(c) for c in capabilities)
        return HandoffBundle(
            contract_version=_version_str(d.get("contract_version")),
            tool=tool.get("name", "forge-doctor-data"),
            tool_version=tool.get("version", ""),
            project=dict(d.get("project", {})),
            summary=dict(d.get("summary", {})),
            findings=tuple(Finding.from_dict(f) for f in d.get("results", d.get("findings", ()))),
            entities=tuple(
                Entity.from_dict(e) for e in graph.get("entities", d.get("entities", ()))
            ),
            relationships=tuple(
                Relationship.from_dict(r)
                for r in graph.get("relationships", d.get("relationships", ()))
            ),
            capabilities=caps,
            plans=tuple(RemediationPlan.from_dict(p) for p in d.get("plans", ())),
        )


@dataclass(frozen=True)
class DiagnosticManifest(ContractModel):
    """Summary-first manifest - the agent-context contract entry point."""

    tool: str = "forge-doctor-data"
    tool_version: str = ""
    domains: tuple[str, ...] = ()
    entity_count: int = 0
    finding_count: int = 0
    risks: tuple[Json, ...] = ()
    capabilities: tuple[Capability, ...] = ()
    evidence_refs: tuple[str, ...] = ()

    def to_dict(self) -> Json:
        return {
            "contract_version": self.contract_version,
            "tool": {"name": self.tool, "version": self.tool_version},
            "domains": list(self.domains),
            "entity_count": self.entity_count,
            "finding_count": self.finding_count,
            "risks": [dict(r) for r in self.risks],
            "capabilities": [c.to_dict() for c in self.capabilities],
            "evidence_refs": list(self.evidence_refs),
        }

    @staticmethod
    def from_dict(d: Json) -> DiagnosticManifest:
        tool = d.get("tool", {})
        return DiagnosticManifest(
            contract_version=d.get("contract_version", str(CURRENT)),
            tool=tool.get("name", "forge-doctor-data"),
            tool_version=tool.get("version", ""),
            domains=tuple(d.get("domains", ())),
            entity_count=int(d.get("entity_count", 0)),
            finding_count=int(d.get("finding_count", 0)),
            risks=tuple(dict(r) for r in d.get("risks", ())),
            capabilities=tuple(Capability.from_dict(c) for c in d.get("capabilities", ())),
            evidence_refs=tuple(d.get("evidence_refs", ())),
        )
