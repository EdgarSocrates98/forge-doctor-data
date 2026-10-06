"""Spec 267/§5+§7: The Forger boundary, bounded handoff, x-forge-data.

Doctor Data accepts a request-shaped dict and returns a
forge-contracts/1 HandoffBundle - no routing, no scheduling, no calls
to other Doctors. The boundary is proven by tests, not documentation.
"""

from __future__ import annotations

import json
import subprocess
import sys

import pytest

from forge_doctor_data.contracts import HandoffBundle
from forge_doctor_data.core.forger import (
    REQUEST_KINDS,
    ForgerRequestError,
    accept_request,
)


@pytest.fixture()
def mini_project(tmp_path):
    (tmp_path / "job.py").write_text("x = 1\n")
    return tmp_path


# --- request shape ------------------------------------------------------------


def test_scan_request_returns_handoff_bundle(mini_project) -> None:
    bundle = accept_request({"kind": "scan", "path": str(mini_project)})
    assert isinstance(bundle, HandoffBundle)
    assert bundle.tool == "forge-doctor-data"
    assert bundle.contract_version == "forge-contracts/1"


def test_non_dict_request_rejected() -> None:
    with pytest.raises(ForgerRequestError, match="JSON object"):
        accept_request(["scan"])


def test_unknown_kind_rejected() -> None:
    with pytest.raises(ForgerRequestError, match="unsupported request kind"):
        accept_request({"kind": "schedule", "path": "."})


def test_routing_kinds_absent_by_design() -> None:
    """The boundary cannot route: no schedule/fan-out/call-doctor kinds."""
    for forbidden in ("schedule", "route", "fan_out", "call", "delegate"):
        assert forbidden not in REQUEST_KINDS


def test_empty_path_rejected() -> None:
    with pytest.raises(ForgerRequestError, match="non-empty string"):
        accept_request({"kind": "scan", "path": ""})


def test_non_object_options_rejected() -> None:
    with pytest.raises(ForgerRequestError, match="object"):
        accept_request({"kind": "scan", "options": [1, 2]})


# --- bounded handoff + x-forge-data --------------------------------------------


def test_bounded_request_bounds_and_records(mini_project) -> None:
    bundle = accept_request(
        {
            "kind": "scan",
            "path": str(mini_project),
            "options": {"bounded": {"findings": 1, "entities": 2}},
        }
    )
    assert len(bundle.findings) <= 1
    assert len(bundle.entities) <= 2
    ext = bundle.extensions.get("x-forge-data")
    assert ext is not None
    assert ext["request_kind"] == "scan"
    assert ext["bounded"] is True
    assert ext["limits"] == {"entities": 2, "findings": 1}


def test_unbounded_request_still_stamps_extension(mini_project) -> None:
    bundle = accept_request({"kind": "scan", "path": str(mini_project)})
    ext = bundle.extensions.get("x-forge-data")
    assert ext is not None and ext["bounded"] is False


def test_x_forge_data_round_trips(mini_project) -> None:
    """The extension block survives serialize->parse (x-* preservation)."""
    bundle = accept_request({"kind": "scan", "path": str(mini_project)})
    again = HandoffBundle.from_dict(bundle.to_dict())
    assert again.extensions.get("x-forge-data") == bundle.extensions["x-forge-data"]


def test_handoff_is_conformant_contract(mini_project) -> None:
    """What The Forger receives validates as forge-contracts/1 handoff."""
    from forge_doctor_data.core.conformance import check_conformance

    bundle = accept_request({"kind": "scan", "path": str(mini_project)})
    result = check_conformance(bundle.to_dict(), "handoff")
    assert result.valid, result.errors


def test_forger_consumes_without_engine(tmp_path, mini_project) -> None:
    """A downstream tool parses the response using only contracts."""
    payload = tmp_path / "handoff.json"
    payload.write_text(
        json.dumps(accept_request({"kind": "scan", "path": str(mini_project)}).to_dict()),
        encoding="utf-8",
    )
    code = (
        "import json, sys\n"
        "from forge_doctor_data.contracts import HandoffBundle\n"
        f"h = HandoffBundle.from_dict(json.loads(open({str(payload)!r}).read()))\n"
        "assert h.tool == 'forge-doctor-data'\n"
        "bad=[m for m in sys.modules if m.startswith('forge_doctor_data.') "
        "and not m.startswith('forge_doctor_data.contracts')]\n"
        "assert not bad, bad\n"
        "print('ok')\n"
    )
    proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == "ok"


# --- no scheduling surface -----------------------------------------------------


def test_bundle_carries_no_scheduling_fields(mini_project) -> None:
    """Honest boundary: the payload contains diagnostics, not commands."""
    d = accept_request({"kind": "scan", "path": str(mini_project)}).to_dict()
    for forbidden in ("schedule", "cron", "route", "dispatch", "invoke"):
        assert forbidden not in d
