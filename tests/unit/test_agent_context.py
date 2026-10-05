from __future__ import annotations

import json
from pathlib import Path

from forge_doctor_data.core.agent_context import context, delta, evidence, manifest


def test_manifest_is_compact_and_reference_first(tmp_path: Path) -> None:
    (tmp_path / "job.py").write_text("df.collect()\n", encoding="utf-8")

    payload = manifest(tmp_path)

    assert payload["contract"] == "agent-context"
    assert isinstance(payload["domains"], list)
    assert isinstance(payload["evidence_refs"], list)
    assert any(str(ref).startswith("finding:") for ref in payload["evidence_refs"])


def test_context_respects_budget_and_keeps_summary(tmp_path: Path) -> None:
    (tmp_path / "job.py").write_text("df.collect()\n", encoding="utf-8")

    payload = context(tmp_path, budget=400)

    assert payload["summary"]
    assert payload["truncated"] is True
    assert len(json.dumps(payload, separators=(",", ":"))) <= 400 * 4


def test_delta_compares_fingerprints(tmp_path: Path) -> None:
    (tmp_path / "job.py").write_text("df.collect()\n", encoding="utf-8")
    previous = {"findings": [{"fingerprint": "old"}]}
    previous_path = tmp_path / "previous.json"
    previous_path.write_text(json.dumps(previous), encoding="utf-8")

    payload = delta(tmp_path, previous_path)

    assert payload["removed"] == ["old"]
    assert payload["added"]


def test_evidence_resolves_entity(tmp_path: Path) -> None:
    (tmp_path / "main.tf").write_text(
        'resource "aws_s3_bucket" "data" {\n  bucket = "data"\n}\n',
        encoding="utf-8",
    )
    graph_manifest = manifest(tmp_path)
    entity_ref = next(
        ref for ref in graph_manifest["evidence_refs"] if str(ref).startswith("entity:")
    )

    payload = evidence(str(entity_ref), tmp_path)

    assert payload["kind"] == "entity"
    assert payload["value"]["id"] == str(entity_ref).removeprefix("entity:")
