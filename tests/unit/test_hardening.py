"""RC hardening §12-18: storage bounds, pack integrity, output consistency,
token economy, error normalization, filesystem + path safety.

Every public surface must answer bad input deterministically, never write
outside its declared store, and never pretend completeness it cannot prove.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest

from forge_doctor_data.core import knowledge
from forge_doctor_data.core.execution_history import (
    HistoryRetention,
    compact_history,
    iter_samples,
    iter_snapshots,
    prune_history,
    read_snapshot,
    record_executions,
)
from forge_doctor_data.core.execution_model import ExecutionStatus, QueryExecution
from forge_doctor_data.core.history import (
    HistoryError,
    load_snapshot,
    resolve_snapshot,
)

# -- §12 history/storage: bounded reads, lazy iteration, corrupt handling -----


def _exec(eid: str, start_ms: float = 1000.0) -> QueryExecution:
    return QueryExecution(
        execution_id=eid,
        engine="spark",
        query_fingerprint=f"fp-{eid}",
        start_time=start_ms,
        duration_ms=42.0,
        status=ExecutionStatus.COMPLETED,
    )


def test_record_and_read_snapshot_roundtrip(tmp_path: Path) -> None:
    record_executions(tmp_path, [_exec("b", 2000.0), _exec("a", 1000.0)])
    paths = list(iter_snapshots(tmp_path))
    assert len(paths) == 1
    samples = list(read_snapshot(paths[0]))
    assert [s.execution_id for s in samples] == ["a", "b"]  # sorted by ts


def test_iter_snapshots_deterministic_order(tmp_path: Path) -> None:
    for i in range(3):
        record_executions(tmp_path, [_exec(f"e{i}")], label=f"s{i}")
    names = [p.name for p in iter_snapshots(tmp_path)]
    assert names == sorted(names)


def test_iter_samples_is_lazy_past_corruption(tmp_path: Path) -> None:
    """Bounded reads: a corrupt later snapshot must not poison earlier reads."""
    record_executions(tmp_path, [_exec("ok")], label="good")
    record_executions(tmp_path, [_exec("later")], label="zzz")  # sorts after
    last = sorted(iter_snapshots(tmp_path))[-1]
    last.write_text("garbage not json\n", encoding="utf-8")
    stream = iter_samples(tmp_path)
    assert next(stream).execution_id == "ok"  # first snapshot streams fine
    with pytest.raises(ValueError):
        next(stream)  # corrupt file fails deterministically when reached


def test_read_snapshot_corrupt_header_raises_valueerror(tmp_path: Path) -> None:
    bad = tmp_path / "snap.jsonl"
    bad.write_text('{"not_header": true}\n', encoding="utf-8")
    with pytest.raises(ValueError, match=r"not a"):
        list(read_snapshot(bad))


def test_read_snapshot_corrupt_row_raises_valueerror(tmp_path: Path) -> None:
    snap = record_executions(tmp_path, [_exec("ok")])
    lines = snap.read_text(encoding="utf-8").splitlines()
    snap.write_text("\n".join([*lines, "{corrupt row\n"]), encoding="utf-8")
    with pytest.raises(ValueError, match=r"corrupt|unreadable"):
        list(read_snapshot(snap))


def test_experiment_snapshots_excluded_from_production(tmp_path: Path) -> None:
    record_executions(tmp_path, [_exec("prod")])
    record_executions(tmp_path, [_exec("exp")], kind="experiment")
    prod = [p.name for p in iter_snapshots(tmp_path, kind="production")]
    exp = [p.name for p in iter_snapshots(tmp_path, kind="experiment")]
    assert all(not n.startswith("exp-") for n in prod)
    assert all(n.startswith("exp-") for n in exp)


def test_prune_history_respects_keep_days(tmp_path: Path) -> None:
    old = record_executions(tmp_path, [_exec("old")], label="a-old")
    new = record_executions(tmp_path, [_exec("new")], label="z-new")
    stale = os.path.getmtime(new) - 90 * 86_400
    os.utime(old, (stale, stale))
    removed = prune_history(tmp_path, HistoryRetention(keep_days=30))
    assert removed == [old]
    assert list(iter_snapshots(tmp_path)) == [new]


def test_compact_history_writes_daily_aggregates(tmp_path: Path) -> None:
    now_ms = datetime.now(UTC).timestamp() * 1000
    record_executions(tmp_path, [_exec("recent", now_ms)], label="z-recent")
    old_path = record_executions(tmp_path, [_exec("ancient")], label="a-old")
    lines = old_path.read_text(encoding="utf-8").splitlines()
    row = json.loads(lines[1])
    row["sample"]["timestamp"] = 1_000.0  # ancient epoch ms
    old_path.write_text("\n".join([lines[0], json.dumps(row)]) + "\n", encoding="utf-8")
    result = compact_history(tmp_path, HistoryRetention(compact_after=1))
    assert result["compacted_samples"] == 1
    assert result["aggregate_records"] == 1
    aggs = [p for p in iter_snapshots(tmp_path) if p.name.startswith("agg-")]
    assert aggs
    payload = json.loads(aggs[0].read_text(encoding="utf-8").splitlines()[0])
    assert payload["aggregate"]["kind"] == "aggregate"


def test_history_snapshot_lifecycle(tmp_path: Path) -> None:
    snap_dir = tmp_path / ".forge-doctor-data" / "history"
    snap_dir.mkdir(parents=True)
    path = snap_dir / "20260101-000000.json"
    path.write_text(
        json.dumps(
            {
                "format": "forge-doctor-data/history@1",
                "created": "2026-01-01T00:00:00+00:00",
                "summary": {"total": 1},
                "findings": [{"key": "k", "check_id": "GLUE001"}],
                "entities": {"ids": ["e1"]},
            }
        ),
        encoding="utf-8",
    )
    snap = load_snapshot(path)
    assert snap.path == path
    assert snap.findings == ({"key": "k", "check_id": "GLUE001"},)
    assert resolve_snapshot(tmp_path, "0") == path
    assert resolve_snapshot(tmp_path, path.stem) == path


# -- §13 knowledge packs: dependency/staleness/provenance honesty -------------


def test_load_pack_missing_returns_empty() -> None:
    assert knowledge.load_pack("no-such-domain") == {}


def test_load_pack_rejects_traversal() -> None:
    assert knowledge.load_pack("..") == {}
    assert knowledge.load_pack("../cli") == {}
    assert knowledge.load_pack("glue", "../versions") == {}
    assert knowledge.load_pack("a/b") == {}


def test_load_pack_ref_rejects_traversal() -> None:
    assert knowledge.load_pack_ref("../outside") is None
    assert knowledge.load_pack_ref("..\\windows") is None


def test_audit_pack_statuses(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    today = date(2026, 1, 1)
    packs = {
        ("fresh", "versions"): {
            "schema_version": 2,
            "pack_version": "1",
            "verified_at": str(today),
            "sources": ["https://example.com"],
        },
        ("stale", "versions"): {
            "schema_version": 2,
            "pack_version": "1",
            "verified_at": str(today - timedelta(days=knowledge.STALE_DAYS + 10)),
            "sources": ["https://example.com"],
        },
        ("expired", "versions"): {
            "schema_version": 2,
            "pack_version": "1",
            "verified_at": str(today),
            "expires_at": str(today - timedelta(days=1)),
            "sources": ["https://example.com"],
        },
        ("badsrc", "versions"): {
            "schema_version": 2,
            "pack_version": "1",
            "verified_at": str(today),
            "sources": ["notaurl"],
        },
        ("unver", "versions"): {
            "schema_version": 2,
            "pack_version": "1",
            "sources": ["https://example.com"],
        },
    }
    monkeypatch.setattr(knowledge, "list_packs", lambda: [(d, n, p) for (d, n), p in packs.items()])
    monkeypatch.setattr(knowledge, "verify_pack", lambda d, n, today=None: [])
    rows = {r["domain"]: r for r in knowledge.audit_packs(today)}
    assert rows["fresh"]["status"] == "fresh"
    assert rows["stale"]["status"] == "stale"
    assert rows["expired"]["status"] == "expired"
    assert rows["badsrc"]["status"] == "invalid_source"
    assert rows["unver"]["status"] == "unverified"


def test_verify_pack_flags_stale_and_malformed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    today = date(2026, 1, 1)
    monkeypatch.setattr(
        knowledge,
        "load_pack",
        lambda domain, name="versions": {
            "schema_version": 2,
            "pack_version": "1",
            "verified_at": "not-a-date",
            "sources": ["https://example.com"],
        },
    )
    issues = knowledge.verify_pack("x", "versions", today)
    assert any("malformed verified_at" in i for i in issues)
    monkeypatch.setattr(
        knowledge,
        "load_pack",
        lambda domain, name="versions": {
            "schema_version": 2,
            "pack_version": "1",
            "verified_at": str(today - timedelta(days=knowledge.STALE_DAYS + 1)),
            "sources": ["https://example.com"],
        },
    )
    assert any("older than" in i for i in knowledge.verify_pack("x", "versions", today))


def test_verify_pack_missing_is_unreadable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(knowledge, "load_pack", lambda *a, **k: {})
    assert knowledge.verify_pack("ghost", "versions") == ["ghost/versions: missing or unreadable"]


def test_verify_dependencies_unknown_target_flagged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A compatibility target absent from the sibling versions pack is an
    honest dependency issue, not silently accepted."""
    packs = {
        ("glue", "compatibility"): {"targets": {"9.9": {"changes": []}}},
        ("glue", "versions"): {"versions": {"4.0": {}, "5.0": {}, "6.0": {}}},
    }
    monkeypatch.setattr(
        knowledge,
        "load_pack",
        lambda domain, name="versions": packs.get((domain, name), {}),
    )
    issues = knowledge.verify_pack_dependencies("glue", "compatibility")
    assert any("9.9" in i and "not in versions pack" in i for i in issues)


def test_verify_dependencies_unknown_runtime_flagged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    packs = {
        ("iceberg", "compatibility"): {"runtimes": {"glue": {"9.9": {"spark": "x"}}}},
        ("glue", "versions"): {"versions": {"4.0": {}, "5.0": {}}},
    }
    monkeypatch.setattr(
        knowledge,
        "load_pack",
        lambda domain, name="versions": packs.get((domain, name), {}),
    )
    issues = knowledge.verify_pack_dependencies("iceberg", "compatibility")
    assert any("runtimes.glue.9.9" in i for i in issues)


# -- §14 output consistency: same scan, same facts on every surface -----------


def _finding_rows(payload_results) -> set[tuple]:
    return {
        (str(r["check_id"]), str(r["severity"]), str(r.get("file")), r.get("line"))
        for r in payload_results
    }


def test_same_scan_same_findings_across_surfaces(tmp_path: Path) -> None:
    """CLI JSON / public API / handoff bundle agree semantically."""
    (tmp_path / "main.tf").write_text(
        'resource "aws_glue_job" "j" {\n  name = "j"\n  glue_version = "4.0"\n}\n',
        encoding="utf-8",
    )
    from forge_doctor_data import api
    from forge_doctor_data.core.handoff import build_handoff_bundle
    from forge_doctor_data.core.service import ScanRequest, ScanService
    from forge_doctor_data.output.json_renderer import result_to_dict

    outcome = ScanService().run(ScanRequest(path=tmp_path, cache=False))
    report = outcome.report
    ctx = outcome.ctx

    api_rows = _finding_rows(result_to_dict(r) for r in report.results)
    bundle = build_handoff_bundle(report, ctx)
    bundle_rows = _finding_rows(bundle["results"])
    assert api_rows == bundle_rows
    assert bundle["summary"]["errors"] == report.summary.errors
    assert bundle["summary"]["warnings"] == report.summary.warnings

    report2 = api.scan(tmp_path).results
    api_rows2 = _finding_rows(result_to_dict(r) for r in report2)
    assert api_rows == api_rows2


# -- §15 token economy: bounded handoff preserves value, states truncation ----


def test_bounded_respects_item_limits() -> None:
    from forge_doctor_data.contracts.models import Finding, HandoffBundle

    bundle = HandoffBundle(
        findings=tuple(Finding(check_id=f"C{i}", severity="info") for i in range(10)),
    )
    cut = bundle.bounded(findings=3)
    assert len(cut.findings) == 3


def test_bounded_records_truncation_as_unknown_fact() -> None:
    from forge_doctor_data.contracts.models import Entity, Finding, HandoffBundle

    bundle = HandoffBundle(
        findings=tuple(Finding(check_id=f"C{i}") for i in range(5)),
        entities=tuple(Entity(id=f"e{i}") for i in range(7)),
    )
    cut = bundle.bounded(findings=2, entities=3)
    truncated = {u.subject for u in cut.unknowns if u.kind == "truncated"}
    assert truncated == {"findings", "entities"}
    reasons = {u.subject: u.reason for u in cut.unknowns}
    assert "2 of 5" in reasons["findings"]
    assert "3 of 7" in reasons["entities"]


def test_bounded_keeps_highest_value_findings() -> None:
    """Truncation must keep errors over info regardless of check-id order."""
    from forge_doctor_data.contracts.models import Finding, HandoffBundle

    bundle = HandoffBundle(
        findings=(
            Finding(check_id="AAA001", severity="info"),
            Finding(check_id="ZZZ001", severity="error"),
            Finding(check_id="MMM001", severity="warning"),
        ),
    )
    cut = bundle.bounded(findings=1)
    assert [f.check_id for f in cut.findings] == ["ZZZ001"]


def test_bounded_zero_items_allowed() -> None:
    from forge_doctor_data.contracts.models import Finding, HandoffBundle

    bundle = HandoffBundle(findings=(Finding(check_id="A"),))
    cut = bundle.bounded(findings=0)
    assert cut.findings == ()
    assert any(u.kind == "truncated" for u in cut.unknowns)


def test_forger_bounded_request(tmp_path: Path) -> None:
    from forge_doctor_data.core.forger import accept_request

    (tmp_path / "main.tf").write_text(
        'resource "aws_glue_job" "j" {\n  name = "j"\n}\n', encoding="utf-8"
    )
    bundle = accept_request(
        {"kind": "scan", "path": str(tmp_path), "options": {"bounded": {"findings": 1}}}
    )
    assert len(bundle.findings) <= 1
    assert bundle.extensions["x-forge-data"]["bounded"] is True


def test_agent_context_respects_byte_budget(tmp_path: Path) -> None:
    from forge_doctor_data.core import agent_context

    for i in range(30):
        (tmp_path / f"f{i}.py").write_text(f"import os\nprint({i})\n", encoding="utf-8")
    payload = agent_context.context(tmp_path, budget=200)
    assert len(json.dumps(payload, separators=(",", ":"))) <= 200 * 4
    assert payload.get("truncated") is True


# -- §16 error handling: deterministic on every public surface ----------------


def test_scan_missing_path_is_deterministic_error(tmp_path: Path) -> None:
    from forge_doctor_data import api
    from forge_doctor_data.core.service import ScanRequestError

    with pytest.raises(ScanRequestError, match="not a directory"):
        api.scan(tmp_path / "does-not-exist")


def test_scan_file_path_is_deterministic_error(tmp_path: Path) -> None:
    from forge_doctor_data import api
    from forge_doctor_data.core.service import ScanRequestError

    f = tmp_path / "a-file.txt"
    f.write_text("x", encoding="utf-8")
    with pytest.raises(ScanRequestError, match="not a directory"):
        api.scan(f)


def test_baseline_corrupt_json_is_baseline_error(tmp_path: Path) -> None:
    from forge_doctor_data.core.baseline import BaselineError, load_baseline_items

    bad = tmp_path / "baseline.json"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(BaselineError, match="not valid JSON"):
        load_baseline_items(bad)


def test_baseline_missing_is_baseline_error(tmp_path: Path) -> None:
    from forge_doctor_data.core.baseline import BaselineError, load_baseline_items

    with pytest.raises(BaselineError, match="not found"):
        load_baseline_items(tmp_path / "missing.json")


def test_baseline_bad_schema_is_baseline_error(tmp_path: Path) -> None:
    from forge_doctor_data.core.baseline import BaselineError, load_baseline_items

    bad = tmp_path / "baseline.json"
    bad.write_text('{"items": "not-a-list"}', encoding="utf-8")
    with pytest.raises(BaselineError):
        load_baseline_items(bad)


def test_load_snapshot_corrupt_is_history_error(tmp_path: Path) -> None:
    bad = tmp_path / "snap.json"
    bad.write_text("{broken", encoding="utf-8")
    with pytest.raises(HistoryError, match="cannot read snapshot"):
        load_snapshot(bad)


def test_forger_request_malformed_inputs() -> None:
    from forge_doctor_data.core.forger import ForgerRequestError, accept_request

    with pytest.raises(ForgerRequestError, match="JSON object"):
        accept_request(["not", "a", "dict"])
    with pytest.raises(ForgerRequestError, match="unsupported request kind"):
        accept_request({"kind": "explode"})
    with pytest.raises(ForgerRequestError, match="non-empty string"):
        accept_request({"kind": "scan", "path": ""})


def test_history_resolve_ref_traversal_is_error(tmp_path: Path) -> None:
    with pytest.raises(HistoryError, match="no snapshot"):
        resolve_snapshot(tmp_path, "../outside.json")
    with pytest.raises(HistoryError, match="no snapshot"):
        resolve_snapshot(tmp_path, "..\\outside")


# -- §17 filesystem safety: a scan must not write outside its declared store --


def _tree_hash(root: Path, exclude: tuple[str, ...] = ()) -> str:
    h = hashlib.sha256()
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root).as_posix()
        if any(part in exclude for part in p.relative_to(root).parts):
            continue
        if p.is_file():
            h.update(rel.encode())
            h.update(p.read_bytes())
    return h.hexdigest()


def test_scan_without_cache_writes_nothing(tmp_path: Path) -> None:
    (tmp_path / "main.tf").write_text(
        'resource "aws_glue_job" "j" {\n  name = "j"\n}\n', encoding="utf-8"
    )
    before = _tree_hash(tmp_path)
    from forge_doctor_data.core.service import ScanRequest, ScanService

    ScanService().run(ScanRequest(path=tmp_path, cache=False))
    assert _tree_hash(tmp_path) == before


def test_cached_scan_only_writes_declared_store(tmp_path: Path) -> None:
    (tmp_path / "main.tf").write_text(
        'resource "aws_glue_job" "j" {\n  name = "j"\n}\n', encoding="utf-8"
    )
    from forge_doctor_data.core.service import ScanRequest, ScanService

    ScanService().run(ScanRequest(path=tmp_path, cache=True))
    outside = _tree_hash(tmp_path, exclude=(".forge-doctor-data",))
    ScanService().run(ScanRequest(path=tmp_path, cache=True))
    # Whatever the cache persists, nothing outside the declared store changes.
    assert _tree_hash(tmp_path, exclude=(".forge-doctor-data",)) == outside


# -- §18 path safety on the remaining public surfaces --------------------------


def test_context_read_text_never_leaves_root(tmp_path: Path) -> None:
    from forge_doctor_data.core.context import ProjectContext

    outside = tmp_path.parent / "outside-secret.txt"
    outside.write_text("SECRET", encoding="utf-8")
    ctx = ProjectContext(root=tmp_path)
    assert ctx.read_text(Path("../outside-secret.txt")) is None
    assert ctx.read_text(Path("..\\outside-secret.txt")) is None
