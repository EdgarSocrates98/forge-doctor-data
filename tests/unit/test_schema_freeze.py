"""Phase 8.6: schema freeze gate — drift needs explicit approval."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import schema_freeze as sf  # noqa: E402


def test_committed_freeze_matches_current_schemas() -> None:
    """The checked-in freeze file equals the live schema set — CI gate."""
    assert sf.check() == []


def test_digest_is_order_and_whitespace_stable() -> None:
    a = {"type": "object", "required": ["a", "b"], "properties": {"a": {"type": "string"}}}
    b = {"properties": {"a": {"type": "string"}}, "required": ["a", "b"], "type": "object"}
    assert sf._canonical_digest("x", a) == sf._canonical_digest("x", b)


def test_current_digests_cover_both_families() -> None:
    digests = sf.current_digests()
    assert any(k.startswith("forge-contracts-1/") for k in digests)
    assert any(k.startswith("legacy/") for k in digests)
    assert len(digests) == 20


def test_check_flags_content_drift(tmp_path: Path) -> None:
    frozen = tmp_path / "freeze.json"
    drifted = {
        k: ("0" * 64 if i == 0 else v) for i, (k, v) in enumerate(sf.current_digests().items())
    }
    frozen.write_text(
        json.dumps({"kind": sf.FREEZE_KIND, "schema_version": "1", "schemas": drifted})
    )
    drift = sf.check(frozen)
    assert len(drift) == 1
    assert "content changed" in drift[0]


def test_check_flags_added_schema(tmp_path: Path) -> None:
    frozen = tmp_path / "freeze.json"
    schemas = sf.current_digests()
    schemas.pop(next(iter(schemas)))
    frozen.write_text(json.dumps({"kind": sf.FREEZE_KIND, "schemas": schemas}))
    assert any("added" in d for d in sf.check(frozen))


def test_check_flags_removed_schema(tmp_path: Path) -> None:
    frozen = tmp_path / "freeze.json"
    schemas = {**sf.current_digests(), "forge-contracts-1/ghost": "0" * 64}
    frozen.write_text(json.dumps({"kind": sf.FREEZE_KIND, "schemas": schemas}))
    assert any("removed" in d for d in sf.check(frozen))


def test_update_requires_approval(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="--approve"):
        sf.update(tmp_path / "freeze.json", "")


def test_update_writes_auditable_record(tmp_path: Path) -> None:
    frozen = tmp_path / "freeze.json"
    payload = sf.update(frozen, "reviewer — intentional field addition")
    assert payload["approved"] == "reviewer — intentional field addition"
    assert payload["kind"] == sf.FREEZE_KIND
    assert len(payload["schemas"]) == 20
    assert sf.check(frozen) == []


def test_corrupt_freeze_file_is_deterministic_error(tmp_path: Path) -> None:
    bad = tmp_path / "freeze.json"
    bad.write_text("{nope")
    with pytest.raises(ValueError, match="cannot read freeze"):
        sf.check(bad)
    bad.write_text('{"kind": "other"}')
    with pytest.raises(ValueError, match="not a"):
        sf.check(bad)
