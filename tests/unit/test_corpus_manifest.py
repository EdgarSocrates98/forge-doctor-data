"""Corpus manifest: entries match vendored dirs; real-oss entries carry
full upstream provenance with per-file integrity hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

_GOLDEN = Path(__file__).resolve().parents[2] / "golden"
_MANIFEST = json.loads((_GOLDEN / "manifest.json").read_text(encoding="utf-8"))
_ORIGINS = {"synthetic", "real-oss", "adversarial"}
_REQUIRED_FIELDS = {
    "name",
    "origin",
    "upstream_repository",
    "upstream_url",
    "commit_sha",
    "license",
    "domain",
    "shape",
    "reason",
    "expected_behavior",
    "vendored_files",
    "date_added",
}


def test_manifest_covers_every_golden_dir() -> None:
    on_disk = {p.name for p in _GOLDEN.iterdir() if p.is_dir()}
    in_manifest = {e["name"] for e in _MANIFEST["entries"]}
    assert on_disk == in_manifest


def test_every_entry_declares_full_schema() -> None:
    for entry in _MANIFEST["entries"]:
        missing = _REQUIRED_FIELDS - set(entry)
        assert not missing, f"{entry['name']}: missing fields {missing}"
        assert entry["origin"] in _ORIGINS, f"{entry['name']}: bad origin"
        assert isinstance(entry["domain"], list) and entry["domain"], (
            f"{entry['name']}: domain must be a non-empty list"
        )
        assert entry["shape"] and entry["reason"] and entry["expected_behavior"]
        assert entry["date_added"]


def test_real_oss_entries_have_provenance() -> None:
    for entry in _MANIFEST["entries"]:
        if entry["origin"] != "real-oss":
            continue
        assert entry["upstream_url"].startswith("https://github.com/"), entry["name"]
        assert entry["upstream_repository"], f"{entry['name']}: no upstream_repository"
        assert len(entry["commit_sha"]) == 40, f"{entry['name']}: commit not pinned to sha"
        int(entry["commit_sha"], 16)  # must be hex
        assert entry["license"], f"{entry['name']}: no license"
        assert (_GOLDEN / entry["name"] / "repo" / "LICENSE").is_file(), (
            f"{entry['name']}: no vendored LICENSE"
        )


def test_synthetic_entries_have_no_upstream() -> None:
    for entry in _MANIFEST["entries"]:
        if entry["origin"] != "synthetic":
            continue
        assert entry["upstream_repository"] is None
        assert entry["upstream_url"] is None
        assert entry["commit_sha"] is None
        assert entry["license"] is None


def test_vendored_files_match_recorded_hashes() -> None:
    """Every file recorded in vendored_files exists under repo/ and its
    sha256 matches - the provenance record is tamper-evident."""
    for entry in _MANIFEST["entries"]:
        repo = _GOLDEN / entry["name"] / "repo"
        recorded = {f["path"]: f for f in entry["vendored_files"]}
        on_disk = {p.relative_to(repo).as_posix() for p in repo.rglob("*") if p.is_file()}
        assert set(recorded) == on_disk, (
            f"{entry['name']}: vendored_files drift "
            f"(missing={sorted(on_disk - set(recorded))}, "
            f"extra={sorted(set(recorded) - on_disk)})"
        )
        for path, record in recorded.items():
            blob = (repo / path).read_bytes()
            assert hashlib.sha256(blob).hexdigest() == record["sha256"], (
                f"{entry['name']}:{path} sha256 mismatch"
            )
            assert len(blob) == record["bytes"]
            assert record["upstream_path"]


def test_every_entry_has_repo_and_expected() -> None:
    for entry in _MANIFEST["entries"]:
        root = _GOLDEN / entry["name"]
        assert (root / "repo").is_dir()
        assert (root / "expected").is_dir()


def test_real_oss_entries_have_ground_truth() -> None:
    for entry in _MANIFEST["entries"]:
        if entry["origin"] != "real-oss":
            continue
        gt = json.loads((_GOLDEN / entry["name"] / "ground_truth.json").read_text(encoding="utf-8"))
        for key in (
            "expected_findings",
            "forbidden_findings",
            "expected_entities",
            "expected_edges",
            "expected_unknowns",
        ):
            assert key in gt, f"{entry['name']}: ground_truth missing {key}"
