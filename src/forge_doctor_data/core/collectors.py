"""Offline evidence-collector contracts.

Collectors are adapters that produce normalized bundles. They are deliberately
separate from ``scan``; a future AWS collector can depend on cloud SDKs while
the core engine stays local and deterministic.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, cast

COLLECTOR_SCHEMA = "forge-doctor-data/evidence-bundle@1"


@dataclass(frozen=True)
class EvidenceRecord:
    source: str
    kind: str
    subject: str
    attributes: tuple[tuple[str, str], ...] = ()
    observed_at: str | None = None
    provenance: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "source": self.source,
            "kind": self.kind,
            "subject": self.subject,
            "attributes": dict(sorted(self.attributes)),
            "observed_at": self.observed_at,
            "provenance": list(sorted(self.provenance)),
        }


@dataclass(frozen=True)
class EvidenceBundle:
    collector: str
    collector_version: str
    records: tuple[EvidenceRecord, ...] = ()
    schema: str = COLLECTOR_SCHEMA
    metadata: tuple[tuple[str, str], ...] = ()

    def to_dict(self) -> dict[str, object]:
        records = sorted(
            (record.to_dict() for record in self.records),
            key=lambda row: (str(row["source"]), str(row["kind"]), str(row["subject"])),
        )
        return {
            "schema": self.schema,
            "collector": self.collector,
            "collector_version": self.collector_version,
            "metadata": dict(sorted(self.metadata)),
            "records": records,
        }


class EvidenceCollector(Protocol):
    """Collector interface implemented by optional cloud adapters."""

    name: str
    version: str

    def collect(self, root: Path) -> EvidenceBundle:
        """Collect external evidence; never called by offline ``scan``."""


def validate_bundle(payload: object) -> list[str]:
    """Validate normalized bundle shape without a JSON-schema dependency."""
    issues: list[str] = []
    if not isinstance(payload, dict):
        return ["bundle must be an object"]
    if payload.get("schema") != COLLECTOR_SCHEMA:
        issues.append(f"schema must be {COLLECTOR_SCHEMA}")
    for field_name in ("collector", "collector_version"):
        if not isinstance(payload.get(field_name), str) or not payload[field_name]:
            issues.append(f"{field_name} must be a non-empty string")
    records = payload.get("records")
    if not isinstance(records, list):
        return [*issues, "records must be an array"]
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            issues.append(f"records[{index}] must be an object")
            continue
        for field_name in ("source", "kind", "subject"):
            if not isinstance(record.get(field_name), str) or not record[field_name]:
                issues.append(f"records[{index}].{field_name} must be a non-empty string")
        if not isinstance(record.get("attributes", {}), dict):
            issues.append(f"records[{index}].attributes must be an object")
        if not isinstance(record.get("provenance", []), list):
            issues.append(f"records[{index}].provenance must be an array")
    return issues


def load_bundle(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    issues = validate_bundle(payload)
    if issues:
        raise ValueError("; ".join(issues))
    return cast(dict[str, object], payload)
