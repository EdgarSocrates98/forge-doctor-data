"""Optional subprocess execution for external checks.

This is process isolation: plugin crashes and output are contained, but the
child is not an OS security sandbox. Operators still need least privilege.

Trust contract: this module re-verifies nothing. The worker ``ep.load()``s
whatever entry point its argv names - the *caller* must gate identities
before invoking (``discovery._ep_trusted`` decides which names may reach a
worker). Invoking the worker directly bypasses the trust gate by design;
that is an operator action with the operator's own privileges, not an
engine path.
"""

from __future__ import annotations

import json
import subprocess
import sys
import threading
from dataclasses import dataclass, replace
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
    if len(argv) < 3:
        raise SystemExit(
            "usage: python -m forge_doctor_data.plugins.isolation "
            "<describe|run> <entry_point> <distribution> [args]"
        )
    command, name, distribution = argv[0], argv[1], argv[2] or None
    if command == "describe":
        payload: object = _describe(name, distribution)
    elif command == "run":
        if len(argv) < 5:
            raise SystemExit("usage: ... run <entry_point> <distribution> <check_id> <root>")
        check_id, root = argv[3], Path(argv[4])
        payload = _run(name, distribution, check_id, root)
    else:
        raise ValueError(f"unknown isolation worker command: {command}")
    print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    return 0


def _capped_drain(stream: Any, limit: int) -> tuple[str, bool]:
    """Read ``stream`` to EOF storing at most ``limit`` bytes.

    The stream is always drained - a child that overflows keeps writing
    into the pipe (no deadlock) while the parent's memory stays bounded.
    Returns ``(text, overflowed)``.
    """
    chunks: list[str] = []
    stored = 0
    total = 0
    while True:
        chunk = stream.read(65_536)
        if not chunk:
            break
        size = len(chunk.encode("utf-8", "replace"))
        total += size
        if stored < limit:
            keep = min(size, limit - stored)
            chunks.append(chunk.encode("utf-8", "replace")[:keep].decode("utf-8", "replace"))
            stored += keep
    return "".join(chunks), total > limit


def _run_child(cmd: list[str], *, timeout_seconds: float, max_output_bytes: int) -> tuple[str, str]:
    """Spawn ``cmd``, drain stdout/stderr with hard byte caps, enforce the
    timeout. Returns ``(stdout, stderr)`` or raises ``RuntimeError``."""
    proc = subprocess.Popen(  # argv list, no shell
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    drained: dict[str, tuple[str, bool]] = {}
    threads = [
        threading.Thread(
            target=lambda: drained.__setitem__("out", _capped_drain(proc.stdout, max_output_bytes)),
            daemon=True,
        ),
        threading.Thread(
            target=lambda: drained.__setitem__("err", _capped_drain(proc.stderr, max_output_bytes)),
            daemon=True,
        ),
    ]
    for thread in threads:
        thread.start()
    try:
        proc.wait(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        raise RuntimeError(
            f"isolated plugin exceeded timeout {timeout_seconds}s - killed"
        ) from None
    for thread in threads:
        thread.join(timeout=10)
    out, out_over = drained.get("out", ("", False))
    err, err_over = drained.get("err", ("", False))
    if out_over or err_over:
        raise RuntimeError("isolated plugin output exceeded configured limit")
    if proc.returncode != 0:
        detail = err.strip() or f"exit code {proc.returncode}"
        raise RuntimeError(f"isolated plugin failed: {detail}")
    return out, err


def _invoke(args: list[str], *, timeout_seconds: float, max_output_bytes: int) -> object:
    out, _err = _run_child(
        [sys.executable, "-m", "forge_doctor_data.plugins.isolation", *args],
        timeout_seconds=timeout_seconds,
        max_output_bytes=max_output_bytes,
    )
    try:
        return json.loads(out)
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
    return [
        row
        for row in payload
        if isinstance(row, dict) and isinstance(row.get("id"), str) and row["id"]
    ]


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
        results: list[CheckResult] = []
        for row in payload:
            if not isinstance(row, dict):
                continue
            result = _result_from_dict(row)
            if result.file is not None and not _inside_root(result.file, ctx.root):
                # A finding's file is a claim, not a read - but claims
                # outside the scanned tree are dropped, not forwarded.
                result = replace(result, file=None)
            results.append(result)
        return results


def _inside_root(file: Path, root: Path) -> bool:
    try:
        resolved = file.resolve() if file.is_absolute() else (Path(root) / file).resolve()
    except OSError:
        return False
    root_resolved = Path(root).resolve()
    return resolved == root_resolved or root_resolved in resolved.parents


if __name__ == "__main__":
    raise SystemExit(_worker(sys.argv[1:]))
