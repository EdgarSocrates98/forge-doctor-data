"""Spec 272: release-candidate artifact pipeline (dry-run, no publish)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import release_candidate as rc  # noqa: E402


def _fake_dist(tmp_path: Path, version: str = "0.9.0") -> Path:
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / f"forge_doctor_data-{version}-py3-none-any.whl").write_bytes(b"wheel-bytes")
    (dist / f"forge_doctor_data-{version}.tar.gz").write_bytes(b"sdist-bytes")
    return dist


def test_artifact_entries_digests_and_sizes(tmp_path: Path) -> None:
    dist = _fake_dist(tmp_path)
    (dist / "unrelated.txt").write_text("noise")  # must be excluded
    entries = rc.artifact_entries(dist)
    assert [e["file"] for e in entries] == [
        "forge_doctor_data-0.9.0-py3-none-any.whl",
        "forge_doctor_data-0.9.0.tar.gz",
    ]
    assert all(len(e["sha256"]) == 64 and e["bytes"] > 0 for e in entries)


def test_sha256sums_format(tmp_path: Path) -> None:
    dist = _fake_dist(tmp_path)
    out = rc.write_sha256sums(dist, rc.artifact_entries(dist))
    lines = out.read_text().strip().splitlines()
    assert len(lines) == 2
    assert all("  forge_doctor_data-" in ln for ln in lines)


def test_export_schemas_covers_both_families(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    dist.mkdir()
    files = rc.export_schemas(dist)
    assert len(files) == 20
    assert any(f.startswith("schemas/forge-contracts-1/") for f in files)
    assert any(f.startswith("schemas/legacy/") for f in files)
    for rel in files:
        assert (dist / rel).is_file()
        json.loads((dist / rel).read_text())  # valid JSON


def test_manifest_deterministic_and_complete(tmp_path: Path) -> None:
    dist = _fake_dist(tmp_path)
    entries = rc.artifact_entries(dist)
    m1 = rc.build_release_manifest(ROOT, dist, "0.9.0", entries, ["schemas/x.json"])
    m2 = rc.build_release_manifest(ROOT, dist, "0.9.0", entries, ["schemas/x.json"])
    assert json.dumps(m1, sort_keys=True) == json.dumps(m2, sort_keys=True)
    assert m1["kind"] == "forge-doctor-data/release-manifest"
    assert m1["contracts"]["forge-contracts"] == "forge-contracts/1"
    assert m1["generated"]["source_date_epoch"] is None


def test_manifest_honors_source_date_epoch(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1700000000")
    dist = _fake_dist(tmp_path)
    m = rc.build_release_manifest(ROOT, dist, "0.9.0", [], [])
    assert m["generated"]["source_date_epoch"] == 1700000000


def test_provenance_subjects_match_artifacts(tmp_path: Path) -> None:
    dist = _fake_dist(tmp_path)
    entries = rc.artifact_entries(dist)
    prov = rc.build_provenance(ROOT, entries)
    assert prov["_type"] == rc.PROVENANCE_TYPE
    assert prov["predicateType"] == rc.PROVENANCE_PREDICATE
    assert {s["name"] for s in prov["subject"]} == {e["file"] for e in entries}


def test_run_refuses_empty_dist(tmp_path: Path) -> None:
    dist = tmp_path / "empty"
    dist.mkdir()
    with pytest.raises(ValueError, match="no distribution artifacts"):
        rc.run(ROOT, dist, build=False, allow_dirty=True)


def test_run_refuses_mismatched_versions(tmp_path: Path) -> None:
    """A stale wheel next to current ones must fail verify, not publish."""
    dist = _fake_dist(tmp_path)
    (dist / "forge_doctor_data-0.7.0-py3-none-any.whl").write_bytes(b"old")
    with pytest.raises(ValueError, match="artifact versions"):
        rc.run(ROOT, dist, build=False, allow_dirty=True)


def test_run_refuses_dirty_tree(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Phase 8.4: uncommitted state never enters release artifacts."""
    dist = _fake_dist(tmp_path)
    monkeypatch.setattr(rc, "_git", lambda *a, **k: " M modified.py")
    with pytest.raises(ValueError, match="working tree is dirty"):
        rc.run(ROOT, dist, build=False)


def test_run_allows_dirty_tree_with_override(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The override is explicit — a local dry run, not a silent default."""
    dist = _fake_dist(tmp_path)
    monkeypatch.setattr(rc, "_git", lambda *a, **k: " M modified.py")
    outputs = rc.run(ROOT, dist, build=False, allow_dirty=True)
    assert outputs["manifest"].is_file()
    assert outputs["provenance"].is_file()


def test_artifact_kinds_requires_wheel_and_sdist(tmp_path: Path) -> None:
    """Phase 8.5: a lone wheel means the sdist is missing — fail."""
    wheel_only = tmp_path / "dist-wheel"
    wheel_only.mkdir()
    (wheel_only / "forge_doctor_data-0.9.0-py3-none-any.whl").write_bytes(b"w")
    with pytest.raises(ValueError, match="no sdist"):
        rc._check_artifact_kinds(rc.artifact_entries(wheel_only))
    sdist_only = tmp_path / "dist-sdist"
    sdist_only.mkdir()
    (sdist_only / "forge_doctor_data-0.9.0.tar.gz").write_bytes(b"s")
    with pytest.raises(ValueError, match="no wheel"):
        rc._check_artifact_kinds(rc.artifact_entries(sdist_only))


def test_verify_digests_catches_tampered_artifact(tmp_path: Path) -> None:
    """Phase 8.3: SHA256SUMS must describe the bytes on disk."""
    dist = _fake_dist(tmp_path)
    sums = rc.write_sha256sums(dist, rc.artifact_entries(dist))
    rc._verify_digests(dist, sums)  # clean state passes
    (dist / "forge_doctor_data-0.9.0-py3-none-any.whl").write_bytes(b"tampered")
    with pytest.raises(ValueError, match="SHA256SUMS mismatch"):
        rc._verify_digests(dist, sums)


def test_build_env_derives_epoch_from_commit(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.delenv("SOURCE_DATE_EPOCH", raising=False)
    env = rc._build_env(ROOT)
    if env.get("SOURCE_DATE_EPOCH"):  # inside a git checkout: derived
        assert env["SOURCE_DATE_EPOCH"].isdigit()
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "123")
    assert rc._build_env(ROOT)["SOURCE_DATE_EPOCH"] == "123"
