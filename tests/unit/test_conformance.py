"""Spec 267: cross-doctor conformance for ``forge-contracts/1`` payloads.

Two-layer validation (published JSON Schema + strict model decode), kind
auto-detection, bundled canonical fixtures, the ``contracts conformance``
CLI, and the no-engine-import boundary other products rely on.
"""

from __future__ import annotations

import json
import subprocess
import sys

import pytest
from typer.testing import CliRunner

from forge_doctor_data.cli import app
from forge_doctor_data.contracts import models as m
from forge_doctor_data.contracts.schemas import FORGE_CONTRACT_SCHEMAS
from forge_doctor_data.core.conformance import (
    CONTRACT_KINDS,
    check_conformance,
    check_fixtures,
    detect_kind,
    load_fixture,
)

runner = CliRunner()


# --- published schemas -------------------------------------------------------


def test_every_kind_has_a_schema_and_model() -> None:
    assert set(FORGE_CONTRACT_SCHEMAS) == set(CONTRACT_KINDS)
    for name, schema in FORGE_CONTRACT_SCHEMAS.items():
        assert f"/forge-contracts/1/{name}.json" in schema["$id"]


# --- bundled canonical fixtures -----------------------------------------------


def test_bundled_fixtures_are_all_conformant() -> None:
    results = check_fixtures()
    assert set(results) == set(CONTRACT_KINDS)
    for name, result in results.items():
        assert result.valid, f"{name}: {result.errors}"


@pytest.mark.parametrize("kind", sorted(CONTRACT_KINDS))
def test_fixture_round_trips_through_model(kind: str) -> None:
    payload = load_fixture(kind)
    model = CONTRACT_KINDS[kind].from_dict(payload)
    assert model.to_dict() == payload


@pytest.mark.parametrize("kind", sorted(CONTRACT_KINDS))
def test_fixture_kind_autodetected(kind: str) -> None:
    assert detect_kind(load_fixture(kind)) == kind


# --- check_conformance ---------------------------------------------------------


def test_valid_finding_passes() -> None:
    result = check_conformance(
        {
            "check_id": "FD-X-1",
            "title": "t",
            "severity": "warning",
            "category": "quality",
            "message": "m",
        }
    )
    assert result.valid, result.errors
    assert result.kind == "finding"
    assert result.negotiated_version == "forge-contracts/1"


def test_missing_required_key_fails() -> None:
    result = check_conformance({"check_id": "FD-X-1", "title": "t"}, kind="finding")
    assert not result.valid
    assert any("severity" in e for e in result.errors)


def test_wrong_type_fails() -> None:
    result = check_conformance(
        {
            "check_id": "FD-X-1",
            "title": "t",
            "severity": "warning",
            "category": "quality",
            "message": 42,
        }
    )
    assert not result.valid


def test_unknown_severity_fails() -> None:
    result = check_conformance(
        {
            "check_id": "FD-X-1",
            "title": "t",
            "severity": "blocker",
            "category": "quality",
            "message": "m",
        }
    )
    assert not result.valid


def test_non_object_payload_fails() -> None:
    result = check_conformance([1, 2, 3])
    assert not result.valid
    assert result.kind is None


def test_undetectable_kind_fails() -> None:
    result = check_conformance({"foo": "bar"})
    assert not result.valid
    assert any("kind" in e for e in result.errors)


def test_unknown_kind_fails() -> None:
    result = check_conformance({}, kind="nonsense")
    assert not result.valid


def test_unsupported_contract_version_fails() -> None:
    result = check_conformance(
        {
            "contract_version": "forge-contracts/99",
            "check_id": "FD-X-1",
            "title": "t",
            "severity": "warning",
            "category": "quality",
            "message": "m",
        }
    )
    assert not result.valid
    assert any("version" in e for e in result.errors)


def test_x_extension_keys_tolerated() -> None:
    result = check_conformance(
        {
            "check_id": "FD-X-1",
            "title": "t",
            "severity": "info",
            "category": "quality",
            "message": "m",
            "x-forge-data": {"scan_id": "abc"},
        }
    )
    assert result.valid, result.errors


# --- boundary: consumers never need engine imports (C.5) -----------------------


def test_contracts_import_pulls_no_engine_modules() -> None:
    """``import forge_doctor_data.contracts`` must not load engine internals."""
    code = (
        "import sys; import forge_doctor_data.contracts; "
        "bad=[m for m in sys.modules if m.startswith('forge_doctor_data.') "
        "and not m.startswith('forge_doctor_data.contracts')]; "
        "sys.exit(1 if bad else 0)"
    )
    proc = subprocess.run([sys.executable, "-c", code], capture_output=True)
    assert proc.returncode == 0


def test_handoff_consumer_needs_only_contracts() -> None:
    """Parse a HandoffBundle in a subprocess with only the contracts surface."""
    payload = json.dumps(load_fixture("handoff"))
    code = (
        "import json, sys; from forge_doctor_data.contracts import HandoffBundle; "
        f"h = HandoffBundle.from_dict(json.loads({payload!r})); "
        "assert h.findings and h.entities; "
        "print(len(h.findings))"
    )
    proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == "1"


# --- CLI -----------------------------------------------------------------------


def test_cli_conformance_valid_fixture_via_file(tmp_path) -> None:
    path = tmp_path / "finding.json"
    path.write_text(json.dumps(load_fixture("finding")), encoding="utf-8")
    result = runner.invoke(app, ["contracts", "conformance", str(path)])
    assert result.exit_code == 0, result.output
    assert "finding" in result.output


def test_cli_conformance_invalid_fails() -> None:
    result = runner.invoke(
        app,
        ["contracts", "conformance", "-", "--kind", "entity"],
        input=json.dumps({"id": "e1"}),
    )
    assert result.exit_code == 1


def test_cli_conformance_json_verdict() -> None:
    result = runner.invoke(
        app,
        ["contracts", "conformance", "-", "--json"],
        input=json.dumps(load_fixture("capability")),
    )
    assert result.exit_code == 0
    verdict = json.loads(result.output)
    assert verdict["valid"] is True
    assert verdict["kind"] == "capability"


def test_cli_conformance_fixtures() -> None:
    result = runner.invoke(app, ["contracts", "conformance", "--fixtures"])
    assert result.exit_code == 0, result.output


def test_cli_conformance_unknown_kind_option() -> None:
    result = runner.invoke(app, ["contracts", "conformance", "-", "--kind", "bogus"], input="{}")
    assert result.exit_code != 0


def test_cli_schema_dump() -> None:
    result = runner.invoke(app, ["contracts", "schema", "finding"])
    assert result.exit_code == 0
    schema = json.loads(result.output)
    assert schema["$id"].endswith("/forge-contracts/1/finding.json")


def test_cli_schema_list() -> None:
    result = runner.invoke(app, ["contracts", "schema"])
    assert result.exit_code == 0
    for kind in CONTRACT_KINDS:
        assert kind in result.output


def test_model_classes_exported_surface() -> None:
    """Regression: CONTRACT_KINDS maps to the frozen vocabulary classes."""
    assert CONTRACT_KINDS["handoff"] is m.HandoffBundle
    assert CONTRACT_KINDS["unknown-fact"] is m.UnknownFact
