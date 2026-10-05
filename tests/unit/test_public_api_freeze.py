"""Spec 271: public contract freeze.

``tools/api_surface.py`` emits the machine-readable inventory of every
semver/wire/ux-bound surface; this suite pins the recorded artifact so
any addition, removal, or signature change is a reviewable diff - never
a silent drift.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import api_surface  # noqa: E402

SURFACE_PATH = ROOT / "docs" / "api-surface.json"
RECORDED = json.loads(SURFACE_PATH.read_text(encoding="utf-8"))


def test_surface_inventory_matches_recorded_freeze() -> None:
    """THE freeze: regenerated inventory must equal the recorded file."""
    current = api_surface.collect_surface()
    assert json.dumps(current, sort_keys=True) == json.dumps(RECORDED, sort_keys=True), (
        "public surface drifted - run `python tools/api_surface.py` and review the diff"
    )


def test_every_surface_has_a_stability_class() -> None:
    classes = set(RECORDED["stability_classes"])
    for name, surface in RECORDED["surfaces"].items():
        assert surface["stability"] in classes, f"{name}: undeclared stability class"


def test_stable_surfaces_are_nonempty() -> None:
    for name in ("python_api", "plugin_sdk", "contracts_vocabulary", "mcp"):
        assert RECORDED["surfaces"][name]["entries"], f"{name} empty - freeze would be vacuous"


def test_mcp_surface_frozen() -> None:
    """Explicit legibility: the 13 MCP tools and protocol versions are pinned."""
    mcp = RECORDED["surfaces"]["mcp"]
    assert len(mcp["entries"]) == 13
    assert mcp["protocols"]["modern"]
    assert mcp["protocols"]["legacy"]  # legacy adapters remain until a major boundary


def test_contracts_schemas_cover_vocabulary() -> None:
    schemas = set(RECORDED["surfaces"]["contracts_schemas"]["entries"])
    fixtures = set(RECORDED["surfaces"]["contracts_fixtures"]["entries"])
    fixtures_kinds = {f.removesuffix(".json") for f in fixtures}
    assert schemas == fixtures_kinds, "schema and fixture kinds must stay 1:1"


def test_wire_versions_recorded() -> None:
    wire = RECORDED["surfaces"]["legacy_wire_schemas"]
    assert wire["scan_schema_version"]
    assert wire["schema_version"]
    assert RECORDED["surfaces"]["contracts_vocabulary"]["contract_version"] == "forge-contracts/1"
