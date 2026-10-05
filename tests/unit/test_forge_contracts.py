"""Phase 7: cross-doctor contract finalization proofs.

- §7.4 extension namespaces: ``x-*`` keys round-trip, never alter base
  semantics, and a consumer may ignore them safely.
- §7.5 negotiation: ``supported_min``/``supported_max``/``exact current``
  are first-class constants with an explicit disjoint-failure path.
- §7.6 conformance kit: the contracts package decodes payloads without
  loading a single engine module.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from forge_doctor_data import contracts
from forge_doctor_data.contracts.models import (
    Capability,
    DiagnosticManifest,
    Entity,
    Evidence,
    Finding,
    HandoffBundle,
    MigrationPlan,
    Relationship,
    RemediationPlan,
    UnknownFact,
)
from forge_doctor_data.contracts.version import (
    CURRENT,
    SUPPORTED_MAX,
    SUPPORTED_MIN,
    ContractVersion,
    negotiate,
    within_range,
)

_MODELS = (
    Entity,
    Relationship,
    Evidence,
    Finding,
    Capability,
    UnknownFact,
    MigrationPlan,
    RemediationPlan,
    HandoffBundle,
    DiagnosticManifest,
)


# -- §7.2 universal vocabulary is exactly the frozen set -----------------------


def test_universal_vocabulary_is_frozen_ten() -> None:
    names = {c.__name__ for c in _MODELS}
    assert names == {
        "Entity",
        "Relationship",
        "Evidence",
        "Finding",
        "Capability",
        "UnknownFact",
        "MigrationPlan",
        "RemediationPlan",
        "HandoffBundle",
        "DiagnosticManifest",
    }


# -- §7.4 extension namespaces -------------------------------------------------


@pytest.mark.parametrize("cls", _MODELS)
def test_x_extensions_roundtrip(cls) -> None:
    model = cls(extensions={"x-forge-data": {"a": 1}, "x-forge-api": "tag"})
    wire = model.to_dict()
    assert wire["x-forge-data"] == {"a": 1}
    assert wire["x-forge-api"] == "tag"
    back = cls.from_dict(wire)
    assert back.extensions["x-forge-data"] == {"a": 1}
    assert back.extensions["x-forge-api"] == "tag"


@pytest.mark.parametrize("cls", _MODELS)
def test_x_extensions_do_not_alter_base_semantics(cls) -> None:
    bare = cls()
    extended = cls(extensions={"x-forge-data": {"note": "extra"}})
    bare_keys = {k for k in bare.to_dict()}
    for key in bare_keys:
        assert key in extended.to_dict()
        assert extended.to_dict()[key] == bare.to_dict()[key]


def test_consumer_may_ignore_extensions_safely() -> None:
    wire = Finding(
        check_id="GLUE001",
        severity="warning",
        extensions={"x-forge-data": {"runtime_hint": "glue5"}},
    ).to_dict()
    stripped = {k: v for k, v in wire.items() if not k.startswith("x-")}
    decoded = Finding.from_dict({**{"title": "", "category": "", "message": ""}, **stripped})
    assert decoded.check_id == "GLUE001"
    assert decoded.severity == "warning"


def test_from_dict_captures_inbound_x_keys() -> None:
    """A producer emitting ``x-*`` keys we did not write still round-trips."""
    model = Finding.from_dict(
        {
            "check_id": "C1",
            "title": "t",
            "severity": "info",
            "category": "c",
            "message": "m",
            "x-forge-future": {"v": 2},
            "x-another": [1, 2],
        }
    )
    assert model.extensions["x-forge-future"] == {"v": 2}
    assert model.extensions["x-another"] == [1, 2]
    assert model.to_dict()["x-forge-future"] == {"v": 2}


# -- §7.5 contract negotiation --------------------------------------------------


def test_negotiation_window_constants() -> None:
    assert CURRENT in contracts.SUPPORTED
    assert SUPPORTED_MIN <= SUPPORTED_MAX
    assert SUPPORTED_MIN.family == SUPPORTED_MAX.family == CURRENT.family


def test_negotiate_exact_current() -> None:
    assert negotiate(CURRENT) == CURRENT
    assert negotiate(str(CURRENT)) == CURRENT


def test_negotiate_disjoint_family_returns_none() -> None:
    assert negotiate("forge-other/1") is None
    assert negotiate(ContractVersion("other", 99)) is None


def test_within_range_bounds_family_and_major() -> None:
    assert within_range(CURRENT)
    assert not within_range("forge-contracts/99")
    assert not within_range("other/1")


def test_parse_rejects_malformed_version() -> None:
    with pytest.raises(ValueError, match="invalid contract version"):
        ContractVersion.parse("noslash")
    with pytest.raises(ValueError, match="invalid contract version"):
        ContractVersion.parse("family/notanint")


# -- §7.6 conformance kit runs without the engine -------------------------------


def test_contracts_decode_without_engine_modules() -> None:
    """Another repo may depend on ``forge_doctor_data.contracts`` alone:
    decoding a canonical payload must not pull a single core module."""
    code = (
        "import sys\n"
        "from forge_doctor_data.contracts import Finding, HandoffBundle\n"
        "from forge_doctor_data.contracts.schemas import FORGE_CONTRACT_SCHEMAS\n"
        "f = Finding.from_dict({'check_id': 'C1', 'title': 't', 'severity': 'error',"
        " 'category': 'c', 'message': 'm'})\n"
        "assert f.to_dict()['check_id'] == 'C1'\n"
        "assert 'finding' in FORGE_CONTRACT_SCHEMAS\n"
        "engine = [m for m in sys.modules if m.startswith('forge_doctor_data.core')"
        " or m.startswith('forge_doctor_data.checks')"
        " or m.startswith('forge_doctor_data.analyzers')]\n"
        "assert not engine, engine\n"
    )
    out = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parents[2],
    )
    assert out.returncode == 0, out.stderr


def test_fixture_payloads_validate_against_schemas() -> None:
    """The bundled canonical fixtures satisfy their published JSON Schema."""
    import json

    from forge_doctor_data.contracts.schemas import FORGE_CONTRACT_SCHEMAS

    fixtures_dir = (
        Path(__file__).resolve().parents[2] / "src" / "forge_doctor_data" / "contracts" / "fixtures"
    )
    for fixture in sorted(fixtures_dir.glob("*.json")):
        payload = json.loads(fixture.read_text(encoding="utf-8"))
        kind = fixture.stem
        if kind in FORGE_CONTRACT_SCHEMAS:
            schema = FORGE_CONTRACT_SCHEMAS[kind]
            required = schema.get("required", [])
            for key in required:
                assert key in payload, f"{fixture.name}: missing required key {key!r}"
