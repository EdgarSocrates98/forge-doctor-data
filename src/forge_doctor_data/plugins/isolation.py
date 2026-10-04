"""Optional subprocess execution for external checks.

This is process isolation: plugin crashes and output are contained, but the
child is not an OS security sandbox. Operators still need least privilege.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from importlib.metadata import EntryPoint, entry_points
from pathlib import Path
from typing import Any

from forge_doctor_data.core.models import CheckResult, Confidence, EvidenceKind, Severity
from forge_doctor_data.plugins.protocol import Check, PluginDescriptor

ENTRY_POINT_GROUP = "forge_doctor_data.checks"


def _entry_point(name: str, distribution: str | None = None) -> EntryPoint:
    candidates = [ep for ep in entry_points(group=ENTRY_POINT_GROUP) if ep.name == name]
    if distribution:
        candidates = [
            ep
            for ep in candidates
            if getattr(getattr(ep, "dist", None), "name", None) == distribution
        ]
    if not candidates:
        raise ValueError(f"plugin entry point not found: {name}")
    return candidates[0]


def _resolved_checks(ep: EntryPoint) -> list[Check]:
    loaded = ep.load()
    loaded = loaded() if isinstance(loaded, type) else loaded
    if isinstance(loaded, PluginDescriptor):
        candidates = loaded.checks
    elif isinstance(loaded, Check):
        candidates = (loaded,)
    elif callable(loaded):
        produced = loaded()
        candidates = produced.checks if isinstance(produced, PluginDescriptor) else (produced,)
    else:
        candidates = (loaded,)
    checks: list[Check] = []
    for candidate in candidates:
        candidate = candidate() if isinstance(candidate, type) else candidate
        if not isinstance(candidate, Check):
            raise TypeError(f"{ep.name}: {candidate!r} is not a Check")
        checks.append(candidate)
    return checks


def _describe(name: str, distribution: str | None) -> list[dict[str, str]]:
    ep = _entry_point(name, distribution)
    checks = _resolved_checks(ep)
    return [
        {
            "id": check.id,
            "title": check.title,
            "category": check.category,
            "why": getattr(check, "why", ""),
            "when_ok": getattr(check, "when_ok", ""),
            "fix": getattr(check, "fix", ""),
        }
        for check in checks
    ]


def _result_to_dict(result: CheckResult) -> dict[str, object]:
    from forge_doctor_data.output.json_renderer import result_to_dict

    return result_to_dict(result)


def _run(name: str, distribution: str | None, check_id: str, root: Path) -> list[dict[str, object]]:
    from forge_doctor_data.core.context import ProjectContext, ScanOptions

    ep = _entry_point(name, distribution)
    check = next(
        (candidate for candidate in _resolved_checks(ep) if candidate.id == check_id), None
    )
    if check is None:
        raise ValueError(f"plugin {name} does not expose {check_id}")
    results = check.run(ProjectContext(root=root, options=ScanOptions(use_cache=False)))
    return [_result_to_dict(result) for result in results]


def _worker(argv: list[str]) -> int:
    command, name, distribution = argv[0], argv[1], argv[2] or None
    if command == "describe":
        payload: object = _describe(name, distribution)
    elif command == "run":
        check_id, root = argv[3], Path(argv[4])
        payload = _run(name, distribution, check_id, root)
    else:
        raise ValueError(f"unknown isolation worker command: {command}")
    print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    return 0


def _invoke(args: list[str], *, timeout_seconds: float, max_output_bytes: int) -> object:
    result = subprocess.run(
        [sys.executable, "-m", "forge_doctor_data.plugins.isolation", *args],
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        check=False,
    )
    if len(result.stdout.encode("utf-8")) > max_output_bytes:
        raise RuntimeError("isolated plugin stdout exceeded configured limit")
    if result.returncode != 0:
        detail = result.stderr.strip() or f"exit code {result.returncode}"
        raise RuntimeError(f"isolated plugin failed: {detail}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"isolated plugin returned invalid JSON: {exc}") from exc


def describe_entry_point(
    name: str,
    distribution: str | None,
    *,
    timeout_seconds: float,
    max_output_bytes: int,
) -> list[dict[str, str]]:
    payload = _invoke(
        ["describe", name, distribution or ""],
        timeout_seconds=timeout_seconds,
        max_output_bytes=max_output_bytes,
    )
    if not isinstance(payload, list):
        raise RuntimeError("isolated plugin description must be an array")
    return [row for row in payload if isinstance(row, dict)]


def _result_from_dict(row: dict[str, Any]) -> CheckResult:
    file_value = row.get("file")
    confidence = row.get("confidence")
    evidence_kind = row.get("evidence_kind")
    return CheckResult(
        check_id=str(row.get("check_id") or "PLUGIN000"),
        title=str(row.get("title") or "Plugin finding"),
        severity=Severity.parse(str(row.get("severity") or "error")),
        category=str(row.get("category") or "plugin"),
        message=str(row.get("message") or ""),
        file=Path(str(file_value)) if file_value else None,
        line=row.get("line") if isinstance(row.get("line"), int) else None,
        recommendation=(
            str(row["recommendation"]) if row.get("recommendation") is not None else None
        ),
        confidence=Confidence.parse(str(confidence)) if confidence else None,
        evidence=str(row["evidence"]) if row.get("evidence") is not None else None,
        evidence_kind=EvidenceKind.parse(str(evidence_kind)) if evidence_kind else None,
        tags=tuple(str(tag) for tag in row.get("tags", []) if isinstance(tag, str)),
        docs_uri=str(row["docs_uri"]) if row.get("docs_uri") is not None else None,
        source=str(row["source"]) if row.get("source") is not None else None,
        fixable=row.get("fixable") if isinstance(row.get("fixable"), bool) else None,
        fingerprint=str(row["fingerprint"]) if row.get("fingerprint") else None,
        symbol=str(row["symbol"]) if row.get("symbol") is not None else None,
    )


@dataclass
class IsolatedCheck:
    """Proxy whose plugin code runs only inside a child process."""

    entry_point: str
    distribution: str | None
    id: str
    title: str
    category: str
    why: str = ""
    when_ok: str = ""
    fix: str = ""
    timeout_seconds: float = 30.0
    max_output_bytes: int = 1_000_000

    def run(self, ctx: Any) -> list[CheckResult]:
        payload = _invoke(
            ["run", self.entry_point, self.distribution or "", self.id, str(ctx.root)],
            timeout_seconds=self.timeout_seconds,
            max_output_bytes=self.max_output_bytes,
        )
        if not isinstance(payload, list):
            raise RuntimeError("isolated plugin results must be an array")
        return [_result_from_dict(row) for row in payload if isinstance(row, dict)]


if __name__ == "__main__":
    raise SystemExit(_worker(sys.argv[1:]))
