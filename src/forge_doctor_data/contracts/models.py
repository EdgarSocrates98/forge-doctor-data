"""Shared wire models for the Forge ecosystem (P16).

Dependency-free, JSON-native frozen dataclasses. These are *contract*
types - the shapes consumers (The Forger, Spark Forge, API Forge,
Claude, Codex, Devin) rely on - not engine internals. Fields are
``str | int | bool | None | dict`` only, so ``to_dict`` output is
already the JSON document.

Naming matches the published JSON Schemas (``core.schemas.SCHEMAS``):
``finding``, ``platform-graph`` entities/relationships, ``evidence``,
``capability-report``, ``remediation-plan``, ``handoff-bundle``.

Null/extension semantics (frozen by spec 266):
- required scalars: a missing key *or* an explicit ``null`` raises
  ``ValueError`` - ``null`` is not a value and must never be conflated
  with one.
- collections: missing key, explicit ``null`` and ``[]`` all mean "no
  items" - never a crash, never a silent scalar.
- optional scalars: missing or ``null`` decodes to ``None`` and emits
  absent - the wire distinguishes "unknown" from "empty string".
- ``x-*`` keys are domain extensions: ``from_dict`` captures them into
  ``extensions`` and ``to_dict`` re-emits them, so forward payloads
  survive a round trip through an older reader.
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


def _required(d: Json, key: str) -> Any:
    """Required field: missing key and explicit ``null`` are both errors."""
    if key not in d:
        raise ValueError(f"missing required field: {key!r}")
    value = d[key]
    if value is None:
        raise ValueError(f"required field {key!r} is explicitly null")
    return value


def _req_str(d: Json, key: str) -> str:
    return str(_required(d, key))


def _opt_str(d: Json, key: str) -> str | None:
    value = d.get(key)
    return None if value is None else str(value)


def _opt_int(d: Json, key: str) -> int | None:
    value = d.get(key)
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"field {key!r} must be an integer or null, got {value!r}")
    return value


def _opt_bool(d: Json, key: str) -> bool | None:
    value = d.get(key)
    if value is None:
        return None
    return bool(value)


def _list(d: Json, key: str) -> tuple[Any, ...]:
    """Collection field: missing, ``null`` and ``[]`` all decode to ``()``."""
    value = d.get(key)
    if value is None:
        return ()
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"field {key!r} must be an array, got {value!r}")
    return tuple(value)


def _str_list(d: Json, key: str) -> tuple[str, ...]:
    return tuple(str(v) for v in _list(d, key))


def _obj(d: Json, key: str) -> Json:
    value = d.get(key)
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValueError(f"field {key!r} must be an object, got {value!r}")
    return dict(value)


def _extensions(d: Json) -> Json:
    """``x-*`` extension keys survive a parse so forward payloads round-trip."""
    return {k: v for k, v in d.items() if isinstance(k, str) and k.startswith("x-")}


def _version_str(value: object) -> str:
    """Wire ``contract_version`` may be ``forge-contracts/1`` or the
    integer ``1`` used by the handoff-bundle schema - both normalize
    to the canonical string form."""
    if isinstance(value, int):
        return f"forge-contracts/{value}"
    return str(value) if value else str(CURRENT)


@dataclass(frozen=True)
class ContractModel:
    """Base: deterministic JSON (de)serialization for every contract."""

    contract_version: str = field(default=str(CURRENT))
    extensions: Json = field(default_factory=dict)

    def to_dict(self) -> Json:  # pragma: no cover - overridden
        raise NotImplementedError

    @staticmethod
    def from_dict(d: Json) -> ContractModel:  # pragma: no cover - overridden
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
                **self.extensions,
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
            contract_version=_version_str(d.get("contract_version")),
            extensions=_extensions(d),
            check_id=_req_str(d, "check_id"),
            title=_req_str(d, "title"),
            severity=_req_str(d, "severity"),
            category=_req_str(d, "category"),
            message=_req_str(d, "message"),
            fingerprint=_opt_str(d, "fingerprint"),
            file=_opt_str(d, "file"),
            line=_opt_int(d, "line"),
            column=_opt_int(d, "column"),
            end_line=_opt_int(d, "end_line"),
            end_column=_opt_int(d, "end_column"),
            recommendation=_opt_str(d, "recommendation"),
            confidence=_opt_str(d, "confidence"),
            evidence=_opt_str(d, "evidence"),
            evidence_kind=_opt_str(d, "evidence_kind"),
            source=_opt_str(d, "source"),
            fixable=_opt_bool(d, "fixable"),
            tags=_str_list(d, "tags"),
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
                **self.extensions,
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
            contract_version=_version_str(d.get("contract_version")),
            extensions=_extensions(d),
            id=_req_str(d, "id"),
            kind=_req_str(d, "kind"),
            domain=_req_str(d, "domain"),
            identifier=str(d.get("identifier") or ""),
            name=str(d.get("name") or ""),
            file=_opt_str(d, "file"),
            line=_opt_int(d, "line"),
            attrs=_obj(d, "attrs"),
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
                **self.extensions,
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
            contract_version=_version_str(d.get("contract_version")),
            extensions=_extensions(d),
            src=_req_str(d, "src"),
            dst=_req_str(d, "dst"),
            kind=_req_str(d, "kind"),
            evidence_kind=_opt_str(d, "evidence_kind"),
            attrs=_obj(d, "attrs"),
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
                **self.extensions,
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
            contract_version=_version_str(d.get("contract_version")),
            extensions=_extensions(d),
            ref=_req_str(d, "ref"),
            kind=_req_str(d, "kind"),
            source=_req_str(d, "source"),
            detail=_opt_str(d, "detail"),
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
                **self.extensions,
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
            contract_version=_version_str(d.get("contract_version")),
            extensions=_extensions(d),
            id=_req_str(d, "id"),
            domain=_req_str(d, "domain"),
            status=_req_str(d, "status"),
            confidence=_opt_str(d, "confidence"),
            evidence_refs=_str_list(d, "evidence_refs"),
        )


@dataclass(frozen=True)
class UnknownFact(ContractModel):
    """An honest UNKNOWN: something the producer could not determine.

    Cross-doctor consumers must be able to see *what* is unknown and
    *why* - a silent empty list hides gaps, a fabricated value hides
    them worse. ``reason`` is required precisely so an UNKNOWN always
    carries its excuse.
    """

    subject: str = ""  # entity/capability id, path, or artifact the fact is about
    kind: str = ""  # class of unknown: entity | capability | evidence | metric | ...
    reason: str = ""  # why it is unknown: missing artifact, pack gap, ...
    source: str | None = None  # which check/pack surfaced the UNKNOWN
    detail: str | None = None  # extra context for the consumer

    def to_dict(self) -> Json:
        return _drop_none(
            {
                **self.extensions,
                "contract_version": self.contract_version,
                "subject": self.subject,
                "kind": self.kind,
                "reason": self.reason,
                "source": self.source,
                "detail": self.detail,
            }
        )

    @staticmethod
    def from_dict(d: Json) -> UnknownFact:
        return UnknownFact(
            contract_version=_version_str(d.get("contract_version")),
            extensions=_extensions(d),
            subject=_req_str(d, "subject"),
            kind=_req_str(d, "kind"),
            reason=_req_str(d, "reason"),
            source=_opt_str(d, "source"),
            detail=_opt_str(d, "detail"),
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
                **self.extensions,
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
            contract_version=_version_str(d.get("contract_version")),
            extensions=_extensions(d),
            id=_req_str(d, "id"),
            source=_req_str(d, "source"),
            target=_req_str(d, "target"),
            kind=_req_str(d, "kind"),
            readiness=_opt_str(d, "readiness"),
            steps=_str_list(d, "steps"),
            risks=_str_list(d, "risks"),
        )


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
                **self.extensions,
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
            a.get("description", "") if isinstance(a, dict) else str(a) for a in _list(d, "actions")
        )
        return RemediationPlan(
            contract_version=_version_str(d.get("contract_version")),
            extensions=_extensions(d),
            id=_req_str(d, "id"),
            check_id=_req_str(d, "check_id"),
            problem=_req_str(d, "problem"),
            targets=_str_list(d, "targets"),
            actions=actions,
            risks=_str_list(d, "risks"),
            requires_approval=bool(d.get("requires_approval") or False),
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
    unknowns: tuple[UnknownFact, ...] = ()

    def to_dict(self) -> Json:
        return {
            **self.extensions,
            "contract_version": self.contract_version,
            "tool": {"name": self.tool, "version": self.tool_version},
            "project": self.project,
            "summary": self.summary,
            "findings": [f.to_dict() for f in self.findings],
            "entities": [e.to_dict() for e in self.entities],
            "relationships": [r.to_dict() for r in self.relationships],
            "capabilities": [c.to_dict() for c in self.capabilities],
            "plans": [p.to_dict() for p in self.plans],
            "unknowns": [u.to_dict() for u in self.unknowns],
        }

    def bounded(
        self,
        *,
        findings: int | None = None,
        entities: int | None = None,
        relationships: int | None = None,
        capabilities: int | None = None,
        plans: int | None = None,
        unknowns: int | None = None,
    ) -> HandoffBundle:
        """Context-bounded bundle (spec 266 §7): keep the first N items of
        each family and record the truncation as ``UnknownFact`` entries -
        a bounded handoff states what it dropped instead of pretending
        completeness. Findings are kept severity-first (error > warning >
        info > pass) so truncation preserves the highest-value context;
        the kept set is re-emitted in bundle order."""

        def cut(items: tuple[Any, ...], limit: int | None, family: str) -> tuple[Any, ...]:
            if limit is None or len(items) <= limit:
                return items
            return items[:limit]

        def cut_findings(items: tuple[Any, ...], limit: int | None) -> tuple[Any, ...]:
            if limit is None or len(items) <= limit:
                return items
            rank = {"error": 0, "warning": 1, "info": 2}
            keep = sorted(
                range(len(items)),
                key=lambda i: (rank.get(getattr(items[i], "severity", "info"), 3), i),
            )[:limit]
            return tuple(items[i] for i in sorted(keep))

        notes = list(self.unknowns[:unknowns] if unknowns is not None else self.unknowns)
        for family, items, limit in (
            ("findings", self.findings, findings),
            ("entities", self.entities, entities),
            ("relationships", self.relationships, relationships),
            ("capabilities", self.capabilities, capabilities),
            ("plans", self.plans, plans),
        ):
            if limit is not None and len(items) > limit:
                notes.append(
                    UnknownFact(
                        subject=family,
                        kind="truncated",
                        reason=f"bounded to {limit} of {len(items)}",
                        source="forge-doctor-data",
                    )
                )
        return HandoffBundle(
            contract_version=self.contract_version,
            extensions=dict(self.extensions),
            tool=self.tool,
            tool_version=self.tool_version,
            project=dict(self.project),
            summary=dict(self.summary),
            findings=cut_findings(self.findings, findings),
            entities=cut(self.entities, entities, "entities"),
            relationships=cut(self.relationships, relationships, "relationships"),
            capabilities=cut(self.capabilities, capabilities, "capabilities"),
            plans=cut(self.plans, plans, "plans"),
            unknowns=tuple(notes),
        )

    @staticmethod
    def from_dict(d: Json) -> HandoffBundle:
        """Deserialize the emitted wire shape (``handoff-bundle`` schema).

        The bundle nests entities/relationships under ``graph``, findings
        under ``results``, and capabilities as ``{platform: {cap: status}}``;
        top-level keys are also accepted for forward compatibility.
        """
        tool = d.get("tool", {})
        graph = d.get("graph", {})
        capabilities = d.get("capabilities") or ()
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
            extensions=_extensions(d),
            tool=tool.get("name", "forge-doctor-data"),
            tool_version=tool.get("version", ""),
            project=dict(d.get("project") or {}),
            summary=dict(d.get("summary") or {}),
            findings=tuple(
                Finding.from_dict(f) for f in d.get("results") or d.get("findings") or ()
            ),
            entities=tuple(
                Entity.from_dict(e) for e in graph.get("entities") or d.get("entities") or ()
            ),
            relationships=tuple(
                Relationship.from_dict(r)
                for r in graph.get("relationships") or d.get("relationships") or ()
            ),
            capabilities=caps,
            plans=tuple(RemediationPlan.from_dict(p) for p in d.get("plans") or ()),
            unknowns=tuple(UnknownFact.from_dict(u) for u in d.get("unknowns") or ()),
        )


@dataclass(frozen=True)
class DiagnosticManifest(ContractModel):
    """Summary-first manifest - the agent-context contract entry point."""

    tool: str = "forge-doctor-data"
    tool_version: str = ""
    domains: tuple[str, ...] = ()
    entity_count: int = 0
    finding_count: int = 0
    unknown_count: int = 0
    risks: tuple[Json, ...] = ()
    capabilities: tuple[Capability, ...] = ()
    evidence_refs: tuple[str, ...] = ()

    def to_dict(self) -> Json:
        return {
            **self.extensions,
            "contract_version": self.contract_version,
            "tool": {"name": self.tool, "version": self.tool_version},
            "domains": list(self.domains),
            "entity_count": self.entity_count,
            "finding_count": self.finding_count,
            "unknown_count": self.unknown_count,
            "risks": [dict(r) for r in self.risks],
            "capabilities": [c.to_dict() for c in self.capabilities],
            "evidence_refs": list(self.evidence_refs),
        }

    @staticmethod
    def from_dict(d: Json) -> DiagnosticManifest:
        tool = d.get("tool", {})
        return DiagnosticManifest(
            contract_version=_version_str(d.get("contract_version")),
            extensions=_extensions(d),
            tool=tool.get("name", "forge-doctor-data"),
            tool_version=tool.get("version", ""),
            domains=_str_list(d, "domains"),
            entity_count=int(d.get("entity_count") or 0),
            finding_count=int(d.get("finding_count") or 0),
            unknown_count=int(d.get("unknown_count") or 0),
            risks=tuple(dict(r) for r in _list(d, "risks")),
            capabilities=tuple(Capability.from_dict(c) for c in _list(d, "capabilities")),
            evidence_refs=_str_list(d, "evidence_refs"),
        )
