"""Spec-256 corpus manifest: entries match vendored dirs; real entries
carry upstream provenance."""

from __future__ import annotations

import json
from pathlib import Path

_GOLDEN = Path(__file__).resolve().parents[2] / "golden"
_MANIFEST = json.loads((_GOLDEN / "manifest.json").read_text(encoding="utf-8"))


def test_manifest_covers_every_golden_dir() -> None:
    on_disk = {p.name for p in _GOLDEN.iterdir() if p.is_dir()}
    in_manifest = {e["name"] for e in _MANIFEST["entries"]}
    assert on_disk == in_manifest


def test_real_entries_have_provenance() -> None:
    for entry in _MANIFEST["entries"]:
        if entry["origin"] != "real":
            continue
        assert entry["url"] and entry["commit"] and entry["license"], (
            f"real entry {entry['name']} missing provenance"
        )


def test_every_entry_has_repo_and_expected() -> None:
    for entry in _MANIFEST["entries"]:
        root = _GOLDEN / entry["name"]
        assert (root / "repo").is_dir()
        assert (root / "expected").is_dir()
