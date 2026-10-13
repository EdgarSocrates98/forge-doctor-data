from __future__ import annotations

from pathlib import Path

from forge_doctor_data.core.execution_history import ExecutionSample, TimestampQuality
from forge_doctor_data.core.execution_store import JsonlStore, SQLiteStore


def sample(execution_id: str) -> ExecutionSample:
    return ExecutionSample(
        timestamp=1.0,
        timestamp_quality=TimestampQuality.EPOCH_ASSUMED_UTC,
        execution_id=execution_id,
        fingerprint="fp",
        engine="spark",
        duration_ms=10.0,
    )


def test_jsonl_store_round_trip_and_export(tmp_path: Path) -> None:
    store = JsonlStore(tmp_path / "history.jsonl")
    store.append([sample("b"), sample("a")])

    assert [row.execution_id for row in store.iter_samples()] == ["a", "b"]
    exported = store.export_jsonl(tmp_path / "export.jsonl")
    assert exported.read_text(encoding="utf-8") == store.path.read_text(encoding="utf-8")


def test_sqlite_store_round_trip_and_jsonl_export(tmp_path: Path) -> None:
    store = SQLiteStore(tmp_path / "history.sqlite")
    store.append([sample("b"), sample("a")])

    assert [row.execution_id for row in store.iter_samples()] == ["a", "b"]
    exported = store.export_jsonl(tmp_path / "export.jsonl")
    assert '"sample"' in exported.read_text(encoding="utf-8")
