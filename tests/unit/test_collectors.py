from __future__ import annotations

from pathlib import Path

from forge_doctor_data.core.collectors import (
    COLLECTOR_SCHEMA,
    EvidenceBundle,
    EvidenceRecord,
    load_bundle,
    validate_bundle,
)


def test_evidence_bundle_is_deterministic(tmp_path: Path) -> None:
    bundle = EvidenceBundle(
        collector="test",
        collector_version="1",
        records=(
            EvidenceRecord(
                source="aws",
                kind="job",
                subject="orders",
                attributes=(("region", "sa-east-1"),),
            ),
        ),
    )
    path = tmp_path / "bundle.json"
    path.write_text(__import__("json").dumps(bundle.to_dict()), encoding="utf-8")

    loaded = load_bundle(path)

    assert loaded["schema"] == COLLECTOR_SCHEMA
    assert validate_bundle(loaded) == []


def test_invalid_bundle_reports_contract_issues() -> None:
    issues = validate_bundle({"schema": "wrong", "records": [{}]})

    assert any("schema" in issue for issue in issues)
    assert any("collector" in issue for issue in issues)
    assert any("source" in issue for issue in issues)
