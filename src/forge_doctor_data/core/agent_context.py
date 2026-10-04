"""Deterministic, budget-aware context for downstream agents.

The engine remains a sensor: this module only projects existing evidence into
small JSON payloads. It never calls a model, network, or cloud service.
"""

from __future__ import annotations

import json
from pathlib import Path

from forge_doctor_data import __version__
from forge_doctor_data.core.context import ProjectContext
from forge_doctor_data.core.models import ScanReport, Severity
from forge_doctor_data.core.platform_graph import DataPlatformGraph

CONTEXT_CONTRACT = "agent-context"
CONTEXT_VERSION = 1


def _scan(path: Path) -> tuple[ScanReport, DataPlatformGraph]:
    from forge_doctor_data.analyzers.platform_graph_builder import build_platform_graph
    from forge_doctor_data.api import scan

    resolved = path.resolve()
    ctx = ProjectContext(root=resolved)
    return scan(resolved), build_platform_graph(ctx)


def _finding_rows(report: ScanReport) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for result in report.results:
        if result.severity not in (Severity.WARNING, Severity.ERROR, Severity.INFO):
            continue
        rows.append(
            {
                "id": result.check_id,
                "severity": result.severity.value,
                "location": (
                    f"{result.file.as_posix()}:{result.line}"
                    if result.file is not None and result.line is not None
                    else (result.file.as_posix() if result.file is not None else None)
                ),
                "fingerprint": result.fingerprint,
                "evidence_ref": f"finding:{result.fingerprint}",
            }
        )
    return sorted(
        rows,
        key=lambda row: (str(row["severity"]), str(row["id"]), str(row["fingerprint"])),
    )


def _entity_rows(graph: DataPlatformGraph) -> list[dict[str, object]]:
    return [
        {"id": row["id"], "kind": row["kind"], "domain": row["domain"]}
        for row in graph.to_dict()["entities"]
    ]


def _capability_rows(graph: DataPlatformGraph) -> list[dict[str, str]]:
    from forge_doctor_data.core.capabilities import CapabilityContext, capability_registry

    registry = capability_registry()
    rows: list[dict[str, str]] = []
    domains = sorted({entity.domain for entity in graph.entities()})
    for domain in domains:
        for capability in registry.capabilities_for(domain):
            result = registry.evaluate(capability, CapabilityContext(platform=domain))
            rows.append(
                {
                    "platform": domain,
                    "capability": capability,
                    "status": result.status.value,
                }
            )
    return rows


def manifest(path: str | Path = ".") -> dict[str, object]:
    """Return compact references and summary facts for a project."""
    report, graph = _scan(Path(path))
    entities = _entity_rows(graph)
    findings = _finding_rows(report)
    return {
        "contract": CONTEXT_CONTRACT,
        "contract_version": CONTEXT_VERSION,
        "tool": {"name": "forge-doctor-data", "version": __version__},
        "project": report.project.name,
        "summary": {
            "passed": report.summary.passed,
            "info": report.summary.info,
            "warnings": report.summary.warnings,
            "errors": report.summary.errors,
        },
        "domains": sorted({str(row["domain"]) for row in entities}),
        "entities": [str(row["id"]) for row in entities],
        "risks": findings,
        "capabilities": _capability_rows(graph),
        "evidence_refs": [
            *(str(row["evidence_ref"]) for row in findings),
            *(f"entity:{row['id']}" for row in entities),
        ],
    }


def _trim_to_budget(payload: dict[str, object], budget: int) -> dict[str, object]:
    if budget <= 0:
        raise ValueError("budget must be greater than zero")
    max_chars = budget * 4
    if len(json.dumps(payload, separators=(",", ":"), ensure_ascii=False)) <= max_chars:
        return payload
    trimmed = dict(payload)
    details = trimmed.get("details")
    if isinstance(details, dict):
        for key in ("relationships", "entities", "findings"):
            value = details.get(key)
            if isinstance(value, list):
                while (
                    value
                    and len(json.dumps(trimmed, separators=(",", ":"), ensure_ascii=False))
                    > max_chars
                ):
                    value.pop()
    for key in ("details", "relationships", "entities", "capabilities", "risks"):
        value = trimmed.get(key)
        if isinstance(value, list):
            while (
                value
                and len(json.dumps(trimmed, separators=(",", ":"), ensure_ascii=False)) > max_chars
            ):
                value.pop()
    trimmed["truncated"] = True
    return trimmed


def context(path: str | Path = ".", budget: int = 8000) -> dict[str, object]:
    """Return summary-first context with references and lazy detail."""
    report, graph = _scan(Path(path))
    findings = _finding_rows(report)
    payload: dict[str, object] = {
        **manifest(path),
        "details": {
            "findings": findings,
            "entities": _entity_rows(graph),
            "relationships": graph.to_dict()["relationships"],
        },
        "budget_tokens": budget,
    }
    return _trim_to_budget(payload, budget)


def _fingerprints(payload: object) -> set[str]:
    if not isinstance(payload, dict):
        return set()
    rows = payload.get("findings", payload.get("results", []))
    if isinstance(payload.get("details"), dict):
        rows = payload["details"].get("findings", rows)
    if not isinstance(rows, list):
        return set()
    return {
        str(row.get("fingerprint"))
        for row in rows
        if isinstance(row, dict) and row.get("fingerprint")
    }


def delta(path: str | Path = ".", since: str | Path | None = None) -> dict[str, object]:
    """Compare current finding fingerprints with a previous context/report."""
    current = context(path)
    previous: object = {}
    if since is not None:
        previous = json.loads(Path(since).read_text(encoding="utf-8"))
    now = _fingerprints(current)
    old = _fingerprints(previous)
    return {
        "contract": CONTEXT_CONTRACT,
        "contract_version": CONTEXT_VERSION,
        "project": Path(path).resolve().name,
        "added": sorted(now - old),
        "removed": sorted(old - now),
        "unchanged": sorted(now & old),
    }


def evidence(reference: str, path: str | Path = ".") -> dict[str, object]:
    """Resolve one finding/entity reference without dumping the full project."""
    report, graph = _scan(Path(path))
    if reference.startswith("finding:"):
        fingerprint = reference.removeprefix("finding:")
        for row in _finding_rows(report):
            if row["fingerprint"] == fingerprint:
                return {"reference": reference, "kind": "finding", "value": row}
    if reference.startswith("entity:"):
        entity_id = reference.removeprefix("entity:")
        for row in graph.to_dict()["entities"]:
            if row["id"] == entity_id:
                relationships = [
                    rel
                    for rel in graph.to_dict()["relationships"]
                    if rel["src"] == entity_id or rel["dst"] == entity_id
                ]
                return {
                    "reference": reference,
                    "kind": "entity",
                    "value": row,
                    "relationships": relationships,
                }
    raise ValueError(f"unknown evidence reference: {reference}")
