"""Pluggable execution-history storage with JSONL as the portable default."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Protocol

from forge_doctor_data.core.execution_history import (
    SNAPSHOT_FORMAT,
    ExecutionSample,
)


class ExecutionStore(Protocol):
    """Minimal store contract shared by JSONL and SQLite backends."""

    def append(self, samples: list[ExecutionSample]) -> None: ...

    def iter_samples(self) -> list[ExecutionSample]: ...

    def export_jsonl(self, target: Path) -> Path: ...


def _sample_row(sample: ExecutionSample) -> str:
    return json.dumps({"sample": sample.to_dict()}, sort_keys=True, ensure_ascii=False)


class JsonlStore:
    """Append-only JSONL store for portable audit artifacts."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def append(self, samples: list[ExecutionSample]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        new_file = not self.path.exists()
        with self.path.open("a", encoding="utf-8") as fh:
            if new_file:
                fh.write(json.dumps({"format": SNAPSHOT_FORMAT, "samples": 0}) + "\n")
            for sample in sorted(samples, key=lambda row: (row.timestamp or 0, row.execution_id)):
                fh.write(_sample_row(sample) + "\n")

    def iter_samples(self) -> list[ExecutionSample]:
        if not self.path.is_file():
            return []
        rows: list[ExecutionSample] = []
        for line in self.path.read_text(encoding="utf-8").splitlines()[1:]:
            payload = json.loads(line)
            if isinstance(payload.get("sample"), dict):
                rows.append(ExecutionSample.from_dict(payload["sample"]))
        return rows

    def export_jsonl(self, target: Path) -> Path:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            self.path.read_text(encoding="utf-8") if self.path.exists() else "",
            encoding="utf-8",
        )
        return target


class SQLiteStore:
    """Stdlib SQLite store for indexed local history; no server required."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS samples ("
                "id INTEGER PRIMARY KEY, timestamp REAL, execution_id TEXT NOT NULL, "
                "payload TEXT NOT NULL)"
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_samples_execution_id ON samples(execution_id)"
            )

    def append(self, samples: list[ExecutionSample]) -> None:
        with sqlite3.connect(self.path) as connection:
            connection.executemany(
                "INSERT INTO samples(timestamp, execution_id, payload) VALUES (?, ?, ?)",
                [
                    (
                        sample.timestamp,
                        sample.execution_id,
                        json.dumps(sample.to_dict(), sort_keys=True),
                    )
                    for sample in samples
                ],
            )

    def iter_samples(self) -> list[ExecutionSample]:
        with sqlite3.connect(self.path) as connection:
            rows = connection.execute(
                "SELECT payload FROM samples ORDER BY timestamp IS NULL, timestamp, "
                "execution_id, id"
            ).fetchall()
        return [ExecutionSample.from_dict(json.loads(row[0])) for row in rows]

    def export_jsonl(self, target: Path) -> Path:
        JsonlStore(target).append(self.iter_samples())
        return target
