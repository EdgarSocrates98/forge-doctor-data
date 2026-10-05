"""Spec 270: mutation + failure-injection suite for the contract path.

The metamorphic suite (``test_mutations.py``) proves the engine *detects*
detrimental change; this suite proves the forge-contracts/1 *gate* kills
every single-field mutation of a valid payload - a mutation the gate
accepts is a conformance hole, not a test tweak.

Kill rate is asserted at 100% and the count is reported, so the file
itself is the critical-path proof artifact.
"""

from __future__ import annotations

import json

import pytest
from typer.testing import CliRunner

from forge_doctor_data.cli import app
from forge_doctor_data.contracts.schemas import FORGE_CONTRACT_SCHEMAS
from forge_doctor_data.core.conformance import CONTRACT_KINDS, check_conformance, load_fixture

runner = CliRunner()


def _required_keys(kind: str) -> list[str]:
    return list(FORGE_CONTRACT_SCHEMAS[kind].get("required", []))


def _required_string_fields(kind: str) -> list[str]:
    props = FORGE_CONTRACT_SCHEMAS[kind].get("properties", {})
    return [k for k in _required_keys(kind) if props.get(k, {}).get("type") == "string"]


def _mutations(fixture: dict, kind: str) -> list[tuple[str, dict]]:
    """Every single-field corruption of a valid fixture."""
    out: list[tuple[str, dict]] = []
    for key in _required_keys(kind):
        deleted = {k: v for k, v in fixture.items() if k != key}
        out.append((f"delete:{key}", deleted))
        nulled = dict(fixture, **{key: None})
        out.append((f"null:{key}", nulled))
    for key in _required_string_fields(kind):
        out.append((f"type-int:{key}", dict(fixture, **{key: 42})))
        out.append((f"type-list:{key}", dict(fixture, **{key: []})))
    return out


@pytest.mark.parametrize("kind", sorted(CONTRACT_KINDS))
def test_every_required_field_mutation_is_killed(kind: str) -> None:
    fixture = load_fixture(kind)
    assert check_conformance(fixture, kind).valid  # control: unmutated passes
    killed, survived = 0, []
    for label, mutant in _mutations(fixture, kind):
        if check_conformance(mutant, kind).valid:
            survived.append(label)
        else:
            killed += 1
    assert not survived, f"{kind}: mutations the gate accepted: {survived}"
    assert killed >= len(_required_keys(kind)) * 2


def test_mutation_kill_count_reported() -> None:
    """The suite is meaningful: it applies a non-trivial mutation volume."""
    total = sum(len(_mutations(load_fixture(k), k)) for k in CONTRACT_KINDS)
    assert total >= 100, f"only {total} mutations - corpus too thin to prove anything"


# --- failure injection ---------------------------------------------------------


def test_truncated_payload_injection() -> None:
    raw = json.dumps(load_fixture("handoff"))[:50]
    result = runner.invoke(app, ["contracts", "conformance", "-"], input=raw)
    assert result.exit_code == 1
    assert "unreadable" in result.output or result.exception is None


def test_scalar_payload_injection() -> None:
    result = runner.invoke(app, ["contracts", "conformance", "-"], input="42")
    assert result.exit_code == 1


def test_wrong_family_injection() -> None:
    mutant = dict(load_fixture("finding"), contract_version="other-contracts/1")
    assert not check_conformance(mutant, "finding").valid


def test_newer_major_injection() -> None:
    mutant = dict(load_fixture("finding"), contract_version="forge-contracts/99")
    assert not check_conformance(mutant, "finding").valid


def test_malformed_version_string_injection() -> None:
    mutant = dict(load_fixture("finding"), contract_version="garbage")
    assert not check_conformance(mutant, "finding").valid


def test_deep_nesting_no_crash() -> None:
    """Pathological nesting must not crash the gate."""
    deep: dict = {}
    node = deep
    for _ in range(500):
        node["x"] = {}
        node = node["x"]
    result = check_conformance(deep)
    assert not result.valid  # detected as unknown kind, no crash


def test_fleet_manifest_injection(tmp_path) -> None:
    """Corrupt fleet manifests raise FleetManifestError, never a traceback."""
    from forge_doctor_data.core.fleet import FleetManifestError, load_manifest

    bad_json = tmp_path / "m.json"
    bad_json.write_text('{"repos": [')
    with pytest.raises(FleetManifestError):
        load_manifest(bad_json)

    bad_yaml = tmp_path / "m.yml"
    bad_yaml.write_text("repos: [not, a, dir]")
    with pytest.raises(FleetManifestError):
        load_manifest(bad_yaml)

    missing = tmp_path / "gone.yml"
    with pytest.raises(FleetManifestError):
        load_manifest(missing)


def test_handoff_bounded_failure_semantics() -> None:
    """Bounded handoff stays conformant - truncation is honest, not lossy."""
    from forge_doctor_data.contracts import HandoffBundle

    bundle = HandoffBundle.from_dict(load_fixture("handoff"))
    bounded = bundle.bounded(findings=0, entities=0)
    result = check_conformance(bounded.to_dict(), "handoff")
    assert result.valid
    assert any(u.kind == "truncated" for u in bounded.unknowns)
