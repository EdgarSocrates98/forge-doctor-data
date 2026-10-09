"""Lifecycle tests for ``forge-doctor-data install`` (forge/* contract v1).

Drives ``forge_doctor_data.install.service`` in-process against tmp roots:
approval gating, ownership ledger, drift/repair, marker/mcp managed regions,
uninstall pruning and the typer dispatch.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from forge_doctor_data import _installkit as kit
from forge_doctor_data.cli import app
from forge_doctor_data.install import service

runner = CliRunner()


@pytest.fixture()
def target(tmp_path: Path) -> Path:
    root = tmp_path / "consumer"
    root.mkdir()
    (root / ".git").mkdir()
    return root


@pytest.fixture(autouse=True)
def _isolate_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("FORGE_HOME_OVERRIDE", str(home))
    return home


# --- plan / apply -----------------------------------------------------------


def test_dry_run_plans_without_mutating(target: Path) -> None:
    doc = service.install(scope="project", root=target, dry_run=True)
    assert doc["status"] == "planned"
    assert doc["schema"] == "forge/InstallReceipt/v1"
    assert not (target / ".mcp.json").exists()
    assert not (target / "AGENTS.md").exists()


def test_apply_requires_approval(target: Path) -> None:
    with pytest.raises(kit.InstallError) as exc:
        service.install(scope="project", root=target)
    assert exc.value.kind == kit.E_NOTAPPROVED


def test_invalid_profile_refused(target: Path) -> None:
    with pytest.raises(kit.InstallError) as exc:
        service.install(scope="project", root=target, profile="bogus", dry_run=True)
    assert exc.value.kind == kit.E_PROFILE


def test_invalid_host_refused(target: Path) -> None:
    with pytest.raises(kit.InstallError) as exc:
        service.install("--bogus", scope="project", root=target, dry_run=True)
    assert exc.value.kind == kit.E_HOST


def test_apply_writes_mcp_and_markers(target: Path) -> None:
    doc = service.install(scope="project", root=target, yes=True)
    assert doc["status"] == "completed"
    mcp = json.loads((target / ".mcp.json").read_text())
    entry = mcp["mcpServers"]["forge-doctor-data"]
    assert entry["command"] == "forge-doctor-data"
    assert entry["args"] == ["mcp"]
    assert "forge-doctor-data:managed:begin" in (target / "AGENTS.md").read_text(encoding="utf-8")


def test_apply_preserves_existing_mcp_servers(target: Path) -> None:
    (target / ".mcp.json").write_text(
        json.dumps({"mcpServers": {"other": {"command": "x"}}, "unrelated": True})
    )
    service.install(scope="project", root=target, yes=True)
    doc = json.loads((target / ".mcp.json").read_text())
    assert doc["mcpServers"]["other"] == {"command": "x"}
    assert doc["unrelated"] is True
    assert "forge-doctor-data" in doc["mcpServers"]


def test_receipt_written_under_state_dir(target: Path) -> None:
    service.install(scope="project", root=target, yes=True)
    receipts = list((target / service.STATE_DIR / "receipts").glob("*.json"))
    assert receipts
    doc = json.loads(receipts[0].read_text())
    assert doc["schema"] == "forge/InstallReceipt/v1"


# --- status / doctor / repair ------------------------------------------------


def test_status_healthy_then_missing(target: Path) -> None:
    service.install(scope="project", root=target, yes=True)
    assert service.status(scope="project", root=target)["status"] == "healthy"
    (target / ".mcp.json").unlink()
    st = service.status(scope="project", root=target)
    assert st["status"] == "degraded"
    assert ".mcp.json" in [d["path"] for d in st["drift"]["missing"]]


def test_user_text_outside_marker_is_not_drift(target: Path) -> None:
    service.install(scope="project", root=target, yes=True)
    ag = target / "AGENTS.md"
    ag.write_text(ag.read_text(encoding="utf-8") + "\n# mine\n", encoding="utf-8")
    assert service.status(scope="project", root=target)["status"] == "healthy"


def test_doctor_schema_and_checks(target: Path) -> None:
    service.install(scope="project", root=target, yes=True)
    doc = service.doctor(scope="project", root=target)
    assert doc["schema"] == "forge/InstallationHealth/v1"
    assert {c["id"] for c in doc["checks"]} >= {"ledger", "mcp-config"}
    assert doc["status"] in ("healthy", "degraded")


def test_repair_restores_missing_mcp_keeps_user_keys(target: Path) -> None:
    service.install(scope="project", root=target, yes=True)
    mcp = target / ".mcp.json"
    doc = json.loads(mcp.read_text())
    doc["mcpServers"].pop("forge-doctor-data")
    doc["mcpServers"]["mine"] = {"command": "y"}
    mcp.write_text(json.dumps(doc))
    out = service.repair(scope="project", root=target)
    assert ".mcp.json" in out["repaired"]
    new = json.loads(mcp.read_text())
    assert new["mcpServers"]["forge-doctor-data"]["command"] == ("forge-doctor-data")
    assert new["mcpServers"]["mine"] == {"command": "y"}


def test_repair_heals_damaged_marker_block(target: Path) -> None:
    service.install(scope="project", root=target, yes=True)
    ag = target / "AGENTS.md"
    ag.write_text("# user\n\n(corrupted)\n", encoding="utf-8")
    out = service.repair(scope="project", root=target)
    assert "AGENTS.md" in out["repaired"]
    txt = ag.read_text(encoding="utf-8")
    assert "# user" in txt
    assert "forge-doctor-data:managed:begin" in txt
    assert service.status(scope="project", root=target)["status"] == "healthy"


# --- uninstall / user scope ---------------------------------------------------


def test_uninstall_removes_owned_prunes_dirs(target: Path) -> None:
    service.install(scope="project", root=target, yes=True)
    out = service.uninstall(scope="project", root=target)
    assert out["status"] == "completed"
    assert not (target / ".mcp.json").exists()
    # AGENTS.md was created by install (marker only) → removed entirely
    assert not (target / "AGENTS.md").exists()
    # state dir keeps the ledger for audit unless --purge
    assert (target / service.STATE_DIR).exists()


def test_uninstall_purge_removes_state(target: Path) -> None:
    service.install(scope="project", root=target, yes=True)
    service.uninstall(scope="project", root=target, purge=True)
    assert not (target / ".forge-doctor-data").exists()


def test_uninstall_keeps_user_modified_managed(target: Path) -> None:
    service.install(scope="project", root=target, yes=True)
    ag = target / "AGENTS.md"
    ag.write_text("# entirely mine now\n", encoding="utf-8")
    service.uninstall(scope="project", root=target)
    assert ag.exists()  # sha mismatch → user-owned


def test_user_scope_installs_home(tmp_path: Path) -> None:
    # FORGE_HOME_OVERRIDE (autouse fixture) is the resolved user home.
    home = tmp_path / "home"
    doc = service.install(scope="user", yes=True)
    assert doc["status"] == "completed"
    assert (home / ".mcp.json").exists()
    assert "forge-doctor-data:managed:begin" in (home / "AGENTS.md").read_text(encoding="utf-8")


# --- update / mcp-verify -------------------------------------------------------


def test_update_latest_refused() -> None:
    doc = service.update(to="latest")
    assert doc["status"] == "failed"
    assert doc["verification"]["status"] == "FAIL"


def test_update_without_manifest_blocked() -> None:
    doc = service.update()
    assert doc["status"] in ("failed", "BLOCKED")


def test_mcp_verify_reports_env_independently() -> None:
    check = service.mcp_verify()
    assert check["id"] == "mcp-handshake"
    assert check["status"] in ("PASS", "FAIL", "BLOCKED")


# --- CLI dispatch --------------------------------------------------------------


def test_cli_dry_run_no_mutation(target: Path) -> None:
    res = runner.invoke(app, ["install", "--root", str(target), "--dry-run"])
    assert res.exit_code == 0, res.output
    doc = json.loads(res.output)
    assert doc["status"] == "planned"
    assert not (target / ".mcp.json").exists()


def test_cli_apply_and_status(target: Path) -> None:
    res = runner.invoke(app, ["install", "--root", str(target), "--yes"])
    assert res.exit_code == 0, res.output
    res = runner.invoke(app, ["install", "status", "--root", str(target)])
    assert res.exit_code == 0
    assert json.loads(res.output)["status"] == "healthy"


def test_cli_refusal_document(target: Path) -> None:
    res = runner.invoke(app, ["install", "--root", str(target)])
    assert res.exit_code == 1
    doc = json.loads(res.output)
    assert doc["error"]["kind"] == "FORGE-INSTALL-PLAN-NOT-APPROVED"
