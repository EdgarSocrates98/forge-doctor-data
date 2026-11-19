"""Lifecycle tests for ``forge-doctor-data install`` (forge/* contract v1).

Drives ``forge_doctor_data.install.service`` in-process against tmp roots:
approval gating, ownership ledger, drift/repair, marker/mcp managed regions,
uninstall pruning and the typer dispatch.
"""

from __future__ import annotations

import json
import sys
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
    # PATH-independent launch (cycle 16.1 §9.3): no registered shim in
    # the test home → the managed key pins the running interpreter and
    # launches the package module — never a bare PATH command.
    assert Path(entry["command"]).is_absolute()
    assert entry["command"] == sys.executable
    assert entry["args"] == ["-m", "forge_doctor_data", "mcp"]
    # Consumer docs moved to the forge_context layer: `forge:*` blocks +
    # the shared workspace registry, not `forge-doctor-data:managed`.
    agents = (target / "AGENTS.md").read_text(encoding="utf-8")
    assert "forge:forge-doctor-data:begin" in agents
    assert "forge:ecosystem:begin" in agents
    reg = json.loads((target / ".forge" / "context" / "registry.json").read_text())
    assert reg["schema"] == "forge/context-registry/v1"
    entry = next(e for e in reg["forges"] if e["forge_id"] == "forge-doctor-data")
    assert entry["kind"] == "diagnostic-provider"
    assert {c["id"] for c in doc["checks"]} >= {"context-registry", "consumer-docs"}


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
    # `.mcp.json` is the only file the installkit ledger owns — the
    # consumer docs live in the forge_context layer — so losing it is
    # "broken" (every owned file missing), not "degraded".
    assert st["status"] == "broken"
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


def test_doctor_mcp_handshake_is_not_masked(target: Path) -> None:
    """The MCP server is stdlib-only — the removed ``find_spec('mcp')``
    guard used to overwrite the real handshake check with a fake
    'extra not installed' UNVERIFIED. Whatever the env reports, it must
    be the kit's own result."""
    service.install(scope="project", root=target, yes=True)
    doc = service.doctor(scope="project", root=target)
    handshake = next(c for c in doc["checks"] if c["id"] == "mcp-handshake")
    assert handshake["status"] in ("PASS", "FAIL", "BLOCKED", "UNVERIFIED")
    assert "extra 'mcp' not installed" not in str(handshake.get("detail", ""))


def test_register_writes_install21_declared_fields(target: Path) -> None:
    """``_register`` copies the forge.json install-2.1 declarations into
    ``~/.forge/installations/`` verbatim (bootstrap register() parity)."""
    service.install(scope="project", root=target, yes=True)
    manifest = service._installation_manifest()
    assert manifest["installation_kind"] == "content"
    assert manifest["install"]["approval"] == "--yes"
    assert "--gateway-profile" in manifest["install"]["flags"]
    assert manifest["depends_on"] == []
    assert manifest["install_command"] == ["{python}", "-m", "forge_doctor_data", "install"]
    assert manifest["mcp"]["verify_tool"] == "get_execution_baseline"


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
    repaired = new["mcpServers"]["forge-doctor-data"]
    assert repaired["command"] == sys.executable
    assert repaired["args"] == ["-m", "forge_doctor_data", "mcp"]
    assert new["mcpServers"]["mine"] == {"command": "y"}


def test_repair_heals_damaged_marker_block(target: Path) -> None:
    service.install(scope="project", root=target, yes=True)
    ag = target / "AGENTS.md"
    ag.write_text("# user\n\n(corrupted)\n", encoding="utf-8")
    out = service.repair(scope="project", root=target)
    # Doc blocks are re-asserted by the forge_context layer (`docs:` prefix).
    assert "docs:AGENTS.md" in out["repaired"]
    txt = ag.read_text(encoding="utf-8")
    assert "# user" in txt
    assert "forge:forge-doctor-data:begin" in txt
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
    # Account scope has no workspace — consumer docs and the context
    # registry are never written there (same rule as sibling forges).
    assert not (home / "AGENTS.md").exists()
    assert not (home / ".forge" / "context").exists()
    assert (home / ".forge" / "installations" / "forge-doctor-data.json").exists()


# --- cycle 16.1 wave-14: incremental reinstall, lifecycle, L0 -----------------


def test_reinstall_is_incremental(target: Path) -> None:
    """A second install is a no-op on disk: the ledger compares managed
    bytes before writing, the context layer keeps identical docs and the
    receipt reports honest zero counters (§7.4 — repeated installs do
    not re-touch unchanged assets)."""
    first = service.install(scope="project", root=target, yes=True)
    assert first["status"] == "completed"
    watched = [
        target / ".mcp.json",
        target / "AGENTS.md",
        target / "AGENT_PROTOCOL.md",
        target / ".forge" / "context" / "registry.json",
        target / ".forge" / "context" / "capabilities" / "forge-doctor-data.json",
    ]
    mtimes = {p: p.stat().st_mtime_ns for p in watched}
    second = service.install(scope="project", root=target, yes=True)
    assert second["status"] == "completed"
    counts = second["counts"]
    assert counts["written"] == 0
    assert counts["written_bytes"] == 0
    for path, mtime in mtimes.items():
        assert path.stat().st_mtime_ns == mtime, f"{path} rewritten on reinstall"


_LIFECYCLE_RECEIPT_STATUSES = {
    "completed",
    "failed",
    "planned",
    "blocked",
    "refused",
    "unsupported",
    "unverified",
    "rolled-back",
}
_LIFECYCLE_VERIFICATION = {"PASS", "FAIL", "BLOCKED", "UNVERIFIED", "NOT_APPLICABLE"}
_LIFECYCLE_HEALTH = {"healthy", "degraded", "broken", "unverified"}


def _derive_receipt_state(doc: dict) -> str:
    """Mirror of ``forge/InstallLifecycle/v1`` ``receipt_state`` — the
    control plane derives, never trusts a stored verdict (contract v1 is
    a document shape: no shared code, the table is re-stated here as a
    compatibility pin)."""
    status = str(doc.get("status") or "")
    verification = str((doc.get("verification") or {}).get("status") or "")
    if status == "planned":
        return "planned"
    if status in ("blocked", "refused", "unsupported"):
        return "blocked"
    if status == "completed":
        if verification == "PASS":
            return "verified"
        if verification == "FAIL":
            return "failed"
        return "applied"
    if status == "failed":
        checks = [c for c in doc.get("checks") or [] if isinstance(c, dict)]
        if checks and all(
            c.get("status") in ("BLOCKED", "UNVERIFIED", "NOT_APPLICABLE") for c in checks
        ):
            return "blocked"
        return "failed"
    return "unverified"


def test_receipt_fields_derive_install_lifecycle(target: Path) -> None:
    """Every receipt this forge emits lands inside the closed vocabularies
    ``forge/InstallLifecycle/v1`` derives from — and now carries the
    envelope itself: ``completed`` + ``PASS`` → ``verified``, never an
    inflated state."""
    doc = service.install(scope="project", root=target, yes=True)
    assert doc["schema"] == "forge/InstallReceipt/v1"
    assert doc["status"] in _LIFECYCLE_RECEIPT_STATUSES
    assert doc["verification"]["status"] in _LIFECYCLE_VERIFICATION
    for check in doc["checks"]:
        assert check["status"] in _LIFECYCLE_VERIFICATION
    assert _derive_receipt_state(doc) == "verified"
    assert doc["lifecycle"]["schema"] == "forge/InstallLifecycle/v1"
    assert doc["lifecycle"]["state"] == "verified"
    # the persisted receipt on disk carries the same envelope
    receipts = list((target / service.STATE_DIR / "receipts").glob("install-*.json"))
    persisted = json.loads(receipts[-1].read_text())
    assert persisted["lifecycle"]["state"] == "verified"

    plan = service.install(scope="project", root=target, dry_run=True)
    assert plan["status"] == "planned"
    assert _derive_receipt_state(plan) == "planned"
    assert plan["lifecycle"]["state"] == "planned"


def test_dry_run_writes_nothing_not_even_state_dir(target: Path) -> None:
    """The plan path is read-only end to end — no lock, no
    ``.forge-doctor-data/`` skeleton on a pristine root."""
    plan = service.install(scope="project", root=target, dry_run=True)
    assert plan["status"] == "planned"
    assert not (target / ".forge-doctor-data").exists()


def test_health_doc_derives_lifecycle_ready(target: Path) -> None:
    """``forge/InstallationHealth/v1`` maps onto the same lifecycle:
    ``healthy`` (verified + clean on disk) → ``ready``."""
    service.install(scope="project", root=target, yes=True)
    doc = service.doctor(scope="project", root=target)
    assert doc["schema"] == "forge/InstallationHealth/v1"
    assert doc["status"] in _LIFECYCLE_HEALTH
    assert doc["status"] == "healthy"  # install + intact ledger + handshake
    assert doc["lifecycle"]["schema"] == "forge/InstallLifecycle/v1"
    # health_state("healthy") → "ready" — the only terminal-success a
    # clean ledger can claim; "certified" requires external evidence.
    assert doc["lifecycle"]["state"] == "ready"
    st = service.status(scope="project", root=target)
    assert st["lifecycle"]["state"] == "ready"


def test_update_refusal_derives_lifecycle_blocked() -> None:
    """A gate refusal (no registered checkout) is ``blocked``, never
    ``failed``: every check gated means nothing ran — the distinction
    the binary vocabulary erased."""
    doc = service.update()
    assert doc["status"] == "failed"  # receipt vocabulary; gate says BLOCKED
    assert doc["lifecycle"]["state"] == "blocked"
    latest = service.update(to="latest")
    assert latest["lifecycle"]["state"] == "failed"


def test_managed_mcp_key_is_path_independent(target: Path) -> None:
    """§9.3 — the host never launches the forge through a PATH lookup:
    the managed ``.mcp.json`` key carries an absolute interpreter (or
    shim) argv, and ``install mcp-verify`` probes that same argv."""
    service.install(scope="project", root=target, yes=True)
    mcp = json.loads((target / ".mcp.json").read_text())
    entry = mcp["mcpServers"]["forge-doctor-data"]
    assert Path(entry["command"]).is_absolute()
    assert entry["args"][-1] == "mcp"
    out = service.mcp_verify()
    (check,) = out["checks"]
    assert check["status"] == "PASS"  # real handshake over the resolved argv
    # tools/list enumerated the real server — the declared verify tool
    # is among them (the probe ran the managed argv, not a PATH guess).
    assert "get_execution_baseline" in check["tools"]


def test_agents_block_is_compact_l0(target: Path) -> None:
    """§8.1/§8.2 minimal L0 boot: the per-forge block in AGENTS.md carries
    identity, domains and verifiable pointers only — CLI/MCP/discovery
    detail lives in the capability manifest and AGENT_PROTOCOL.md, never
    duplicated into permanent context."""
    service.install(scope="project", root=target, yes=True)
    text = (target / "AGENTS.md").read_text(encoding="utf-8")
    begin = "<!-- forge:forge-doctor-data:begin -->"
    end = "<!-- forge:forge-doctor-data:end -->"
    block = text.split(begin)[1].split(end)[0]
    assert "forge-doctor-data" in block
    assert "Domains:" in block
    assert "Capability manifest" in block
    assert "AGENT_PROTOCOL.md" in block
    # the compact block never re-inlines the discovery/CLI detail
    assert "Discovery:" not in block
    assert "- CLI:" not in block
    assert len(block.encode("utf-8")) < 700
    # the detail it points at actually exists and is ours
    manifest = json.loads(
        (target / ".forge" / "context" / "capabilities" / "forge-doctor-data.json").read_text()
    )
    assert manifest["schema"] == "forge/context/v1"
    protocol = (target / "AGENT_PROTOCOL.md").read_text(encoding="utf-8")
    assert "forge:forge-doctor-data" in protocol


def test_capability_manifest_is_honest(target: Path) -> None:
    """Context metadata honesty: the installed manifest declares only what
    exists — real domains, real discovery argv, absent capabilities named
    ``unavailable`` (never fabricated), health from real bundled assets."""
    service.install(scope="project", root=target, yes=True)
    manifest = json.loads(
        (target / ".forge" / "context" / "capabilities" / "forge-doctor-data.json").read_text()
    )
    assert manifest["forge_id"] == "forge-doctor-data"
    assert manifest["domains"]
    assert manifest["domains"] == sorted(manifest["domains"])
    for cmd in manifest["discovery"]["commands"]:
        assert cmd["argv"][0] == "forge-doctor-data"
        assert cmd["read_only"] is True
    caps = manifest["capabilities"]
    # no host skill/agent mirrors are published — honest unavailability
    for name in ("skills", "knowledge", "rules", "evals"):
        assert caps[name]["status"] == "unavailable", name
        assert caps[name]["count"] == 0
    # the bundled agent specs are real files inside the package
    assert caps["agents"]["status"] == "available"
    assert caps["agents"]["count"] == len(manifest["agents"]) == 3
    for agent in manifest["agents"]:
        assert (service._AGENTS_DIR / f"{agent}.md").is_file(), (
            f"manifest names missing spec {agent}"
        )
    assert manifest["interfaces"]["mcp"]["verify_tool"] == "get_execution_baseline"
    assert manifest["health"]["status"] == "healthy"


# --- update / mcp-verify -------------------------------------------------------


def test_update_latest_refused() -> None:
    doc = service.update(to="latest")
    assert doc["status"] == "failed"
    assert doc["verification"]["status"] == "FAIL"


def test_update_without_manifest_blocked() -> None:
    doc = service.update()
    assert doc["status"] in ("failed", "BLOCKED")


def test_mcp_verify_reports_env_independently() -> None:
    doc = service.mcp_verify()
    # forge/InstallationHealth/v1 envelope — the same shape the script emits.
    assert doc["schema"] == "forge/InstallationHealth/v1"
    assert doc["forge_id"] == "forge-doctor-data"
    assert doc["status"] in ("healthy", "degraded", "unverified")
    (check,) = doc["checks"]
    assert check["id"] == "mcp-handshake"
    assert check["status"] in ("PASS", "FAIL", "BLOCKED")
    # status tracks the check honestly: FAIL -> degraded, else healthy.
    if check["status"] == "FAIL":
        assert doc["status"] == "degraded"
    elif check["status"] == "PASS":
        assert doc["status"] == "healthy"


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


def test_hosts_none_e_csv():
    """GAP-003: `none` nunca vira `all`; csv subconjunto e validado."""
    import pytest

    from forge_doctor_data import _installkit as kit
    from forge_doctor_data.install.service import HOSTS, _hosts

    assert _hosts("all") == HOSTS
    assert _hosts("none") == ()
    assert _hosts("") == ()
    assert set(_hosts("claude,devin")) == {"claude", "devin"}
    with pytest.raises(kit.InstallError):
        _hosts("nope")
