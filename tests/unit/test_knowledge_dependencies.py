"""Spec §13: knowledge-pack supply-chain dependency validation.

``verify_pack_dependencies`` checks referential integrity across packs:
compatibility targets must exist in the sibling versions pack, runtime
version keys must exist in the referenced engine's versions pack, and a
pack's ``domain`` field must anchor to directory or filename.
"""

from __future__ import annotations

import forge_doctor_data.core.knowledge as knowledge
from forge_doctor_data.core.knowledge import (
    list_packs,
    verify_pack,
    verify_pack_dependencies,
)


def _fake_loader(packs: dict[tuple[str, str], dict]):
    def _load(domain: str, name: str = "versions") -> dict:
        return packs.get((domain, name), {})

    return _load


def test_bundled_packs_have_no_dependency_issues() -> None:
    """The shipped knowledge tree must satisfy all dependency rules."""
    issues = [i for d, n, _ in list_packs() for i in verify_pack_dependencies(d, n)]
    assert issues == [], issues


def test_domain_field_must_anchor_to_dir_or_filename(monkeypatch) -> None:
    packs = {
        ("glue", "versions"): {"domain": "glue", "versions": {"5.0": {}}},
        ("capabilities", "glue"): {"domain": "glue"},
        ("capabilities", "spark"): {"domain": "wrong-domain"},
    }
    monkeypatch.setattr(knowledge, "load_pack", _fake_loader(packs))
    assert verify_pack_dependencies("capabilities", "glue") == []
    issues = verify_pack_dependencies("capabilities", "spark")
    assert any("wrong-domain" in i for i in issues)


def test_compatibility_targets_must_exist_in_versions(monkeypatch) -> None:
    packs = {
        ("glue", "versions"): {"domain": "glue", "versions": {"5.0": {}, "6.0": {}}},
        ("glue", "compatibility"): {
            "domain": "glue",
            "targets": {"5.0": {}, "9.9": {}},
        },
    }
    monkeypatch.setattr(knowledge, "load_pack", _fake_loader(packs))
    issues = verify_pack_dependencies("glue", "compatibility")
    assert issues == ["glue/compatibility: target '9.9' not in versions pack"]


def test_runtime_keys_checked_against_engine_versions(monkeypatch) -> None:
    packs = {
        ("iceberg", "compatibility"): {
            "domain": "iceberg",
            "runtimes": {"glue": {"4.0": {}, "9.9": {}}, "emr": {"7.x": {}}},
        },
        ("glue", "versions"): {"domain": "glue", "versions": {"4.0": {}}},
        # no emr/versions pack -> emr keys are uncheckable, must NOT flag
    }
    monkeypatch.setattr(knowledge, "load_pack", _fake_loader(packs))
    issues = verify_pack_dependencies("iceberg", "compatibility")
    assert issues == ["iceberg/compatibility: runtimes.glue.9.9 not in glue/versions"]


def test_malformed_version_key_flagged(monkeypatch) -> None:
    packs = {
        ("glue", "versions"): {
            "domain": "glue",
            "versions": {"5.0": {}, "latest": {}},
        },
    }
    monkeypatch.setattr(knowledge, "load_pack", _fake_loader(packs))
    issues = verify_pack_dependencies("glue", "versions")
    assert any("'latest'" in i for i in issues)


def test_dependency_issues_surface_in_verify_pack(monkeypatch) -> None:
    """Dependency integrity is part of the same gate, not a side channel."""
    packs = {
        ("glue", "compatibility"): {
            "domain": "glue",
            "schema_version": 2,
            "pack_version": "2026.1",
            "verified_at": "2026-01-01",
            "sources": ["https://example.com"],
            "targets": {"9.9": {}},
        },
        ("glue", "versions"): {"domain": "glue", "versions": {"5.0": {}}},
    }
    monkeypatch.setattr(knowledge, "load_pack", _fake_loader(packs))
    issues = verify_pack("glue", "compatibility")
    assert any("target '9.9'" in i for i in issues)


def test_missing_pack_returns_no_dependency_issues() -> None:
    assert verify_pack_dependencies("nonexistent-domain", "nonexistent") == []
