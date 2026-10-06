"""RC baseline + freeze policy guards (rc-hardening Phase 1).

The RC cycle is only real if the freeze is provable: the baseline
artifact exists with the required fields, every public surface carries
a known stability class, and the frozen measurements in the baseline
still match the code they describe.
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import rc_baseline  # noqa: E402

BASELINE = ROOT / "docs" / "rc-baseline.json"
POLICY = ROOT / "docs" / "rc-policy.md"
API_SURFACE = ROOT / "docs" / "api-surface.json"

REQUIRED_TOP = {
    "kind",
    "schema_version",
    "rc_target",
    "git",
    "package",
    "verification",
    "ci",
    "contracts",
    "mcp",
    "corpus",
    "labs",
    "fleet",
    "public_api",
}
KNOWN_STABILITY = {"stable", "wire", "ux", "experimental", "internal", "deprecated"}


def _baseline() -> dict:
    return json.loads(BASELINE.read_text(encoding="utf-8"))


def test_baseline_exists_with_required_fields() -> None:
    assert BASELINE.exists()
    data = _baseline()
    assert set(data) >= REQUIRED_TOP
    assert data["kind"] == "forge-doctor-data/rc-baseline"
    assert data["schema_version"] == "1"
    assert data["rc_target"] == "1.0.0-rc1"


def test_baseline_records_provenance() -> None:
    data = _baseline()
    assert len(data["git"]["head"]) == 40
    assert data["package"]["version"]
    assert isinstance(data["verification"]["test_count"], int)
    assert data["verification"]["test_count"] > 0
    assert isinstance(data["verification"]["coverage_percent"], int | float)
    assert data["ci"]["job_definitions"] >= 5


def test_baseline_frozen_fields_match_current_code() -> None:
    from forge_doctor_data.core.handoff import CONTRACT_VERSION
    from forge_doctor_data.integrations.mcp_server import _TOOL_DEFS

    data = _baseline()
    assert data["contracts"]["contract_version"] == CONTRACT_VERSION
    assert data["mcp"]["tool_count"] == len(_TOOL_DEFS)
    current_hash = hashlib.sha256(API_SURFACE.read_bytes()).hexdigest()
    assert data["public_api"]["public_api_sha256"] == current_hash


def test_every_public_surface_has_known_stability_class() -> None:
    surface = json.loads(API_SURFACE.read_text(encoding="utf-8"))
    declared = set(surface["stability_classes"])
    assert declared <= KNOWN_STABILITY
    for name, entry in surface["surfaces"].items():
        assert entry["stability"] in KNOWN_STABILITY, name


def test_rc_policy_documents_freeze_and_no_feature_rule() -> None:
    text = POLICY.read_text(encoding="utf-8")
    for marker in (
        "DataPlatformGraph",
        "forge-contracts/1",
        "HandoffBundle",
        "stable",
        "wire",
        "ux",
        "new vendors",
        "public schema redesign",
        "P0",
        "P3",
        "Trusted Publishing",
    ):
        assert marker in text, marker


def test_rc_baseline_check_passes() -> None:
    out = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "rc_baseline.py"), "--check"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert out.returncode == 0, out.stdout + out.stderr


def test_collect_baseline_shape() -> None:
    data = rc_baseline.collect_baseline(100, 85.0)
    assert data["verification"] == {"test_count": 100, "coverage_percent": 85.0}
    assert data["corpus"]["golden_entries"] >= 11
    assert data["labs"]["scenario_count"] >= 60
    assert data["fleet"]["scan_validated_envelope"] == 250
    assert data["fleet"]["merge_validated_envelope"] == 500
