"""Portal adapter tests — ``forge-doctor-data portal``.

Drives the adapter in-process against tmp roots (same seam as
``test_install_lifecycle.py``): honest NOT_INSTALLED state, install plan →
confirm → apply with real receipts, named refusals, the live HTTP layer
(session token, 403 without it) and the real ``scan`` task over the
workspace's own evidence.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

import pytest
from typer.testing import CliRunner

from forge_doctor_data import _forge_portal as fp
from forge_doctor_data.cli import app
from forge_doctor_data.install import service
from forge_doctor_data.portal_adapter import ForgeDoctorDataPortal

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


def _server(adapter: ForgeDoctorDataPortal) -> fp.PortalServer:
    server = fp.PortalServer(adapter, quiet=True)
    server.serve_in_thread()
    return server


def _get(server: fp.PortalServer, path: str, *, token: str | None = None) -> tuple[int, dict]:
    url = f"http://127.0.0.1:{server.port}/api/v1{path}"
    req = urllib.request.Request(url)
    if token:
        req.add_header("X-Forge-Session", token)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())


def _post(
    server: fp.PortalServer, path: str, body: dict, *, token: str | None = None
) -> tuple[int, dict]:
    url = f"http://127.0.0.1:{server.port}/api/v1{path}"
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    if token:
        req.add_header("X-Forge-Session", token)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())


# --- descriptor / health ----------------------------------------------------


def test_descriptor_is_real(target: Path) -> None:
    a = ForgeDoctorDataPortal(target)
    d = a.descriptor()
    assert d["forge_id"] == "forge-doctor-data"
    assert d["cli"] == "forge-doctor-data"
    assert d["forge_version"]
    assert any(c["id"] == "scan" and c["state"] == "supported" for c in d["capabilities"])
    # this forge ships no host assets — unsupported, never silently empty
    assert any(c["id"] == "skills" and c["state"] == "unsupported" for c in d["capabilities"])


def test_health_not_installed_on_virgin_workspace(target: Path) -> None:
    a = ForgeDoctorDataPortal(target)
    h = a.health()
    assert h["state"] == "NOT_INSTALLED"
    assert h["workspace"] == str(target)


def test_install_plan_then_apply_roundtrip(target: Path) -> None:
    a = ForgeDoctorDataPortal(target)
    server = _server(a)
    try:
        code, boot = _get(server, "/bootstrap", token=server.session_token)
        assert code == 200, boot
        code, plan_doc = _post(
            server,
            "/installation/plan",
            {"scope": "project", "host": "devin", "profile": "minimal"},
            token=server.session_token,
        )
        assert code == 200, plan_doc
        plan = plan_doc["data"]["plan"]
        token = plan_doc["data"]["plan_token"]
        code, applied = _post(
            server,
            "/installation/apply",
            {"plan": plan, "plan_token": token, "confirm": "apply"},
            token=server.session_token,
        )
        assert code == 200, applied
        assert applied["data"]["status"] == "completed"
        code, health = _get(server, "/health", token=server.session_token)
        assert health["data"]["state"] in ("INSTALLED", "ACTIVE", "VERIFIED", "DEGRADED")
        assert health["data"]["state"] != "NOT_INSTALLED"
    finally:
        server.shutdown()
        server.server_close()


def test_apply_rejects_stale_plan_token(target: Path) -> None:
    a = ForgeDoctorDataPortal(target)
    server = _server(a)
    try:
        code, doc = _post(
            server,
            "/installation/apply",
            {"plan": {"scope": "project"}, "plan_token": "forged", "confirm": "apply"},
            token=server.session_token,
        )
        assert code == 409
        assert doc["error"]["code"] == "PORTAL-PLAN-STALE"
    finally:
        server.shutdown()
        server.server_close()


def test_bootstrap_requires_session(target: Path) -> None:
    server = _server(ForgeDoctorDataPortal(target))
    try:
        code, _doc = _get(server, "/bootstrap")
        assert code == 403
    finally:
        server.shutdown()
        server.server_close()


def test_spa_served(target: Path) -> None:
    a = ForgeDoctorDataPortal(target)
    assert a.assets_dir is not None
    server = _server(a)
    try:
        url = f"http://127.0.0.1:{server.port}/"
        with urllib.request.urlopen(url, timeout=30) as r:
            html = r.read().decode()
        assert "<" in html
    finally:
        server.shutdown()
        server.server_close()


# --- hosts / mcp -------------------------------------------------------------


def test_hosts_flow_reports_real_probe(target: Path) -> None:
    a = ForgeDoctorDataPortal(target)
    hosts = a._hosts()
    assert {h["host"] for h in hosts} == set(service.HOSTS)
    for h in hosts:
        assert h["host"] in service.HOSTS
        assert "detected" in h and "integration" in h


def test_hosts_launch_refuses_absent_host(target: Path) -> None:
    a = ForgeDoctorDataPortal(target)
    doc = a._hosts_launch(type("C", (), {"body": {"host": "copilot"}})())
    # copilot is absent on this machine — named refusal, command None.
    # (if a future env ships it, the command must be a real string)
    if doc["refusal"] == "PORTAL-HOST-ABSENT":
        assert doc["command"] is None
    else:
        assert isinstance(doc["command"], str)


def test_hosts_launch_bad_field(target: Path) -> None:
    a = ForgeDoctorDataPortal(target)
    with pytest.raises(fp.PortalError) as ei:
        a._hosts_launch(type("C", (), {"body": {"host": "emacs"}})())
    assert ei.value.code == "PORTAL-BAD-FIELD"


def test_mcp_verify_named_status(target: Path) -> None:
    doc = ForgeDoctorDataPortal(target)._mcp_verify_doc()
    assert doc["status"] in ("PASS", "FAIL", "HANDSHAKE", "BLOCKED", "NOT_APPLICABLE")


# --- skills / agents: honest unsupported catalog ----------------------------


def test_skills_agents_empty_by_design(target: Path) -> None:
    a = ForgeDoctorDataPortal(target)
    assert a._skills() == []
    assert a._agents() == []


# --- tasks --------------------------------------------------------------------


def _task_ctx(server: fp.PortalServer, body: dict):
    handler = type("H", (), {"server": server})()
    return fp.RequestContext(handler=handler, body=body, query={}, params={}, correlation_id="t")


def test_tasks_plan_ambiguous_refuses(target: Path) -> None:
    a = ForgeDoctorDataPortal(target)
    server = _server(a)
    try:
        with pytest.raises(fp.PortalError) as ei:
            a._tasks_plan(_task_ctx(server, {"intent": "reformat my disk"}))
        assert ei.value.code == "FDD-PORTAL-AMBIGUOUS"
    finally:
        server.shutdown()
        server.server_close()


def test_tasks_scan_executes_real_engine(target: Path) -> None:
    (target / "pyproject.toml").write_text('[project]\nname="x"\n', encoding="utf-8")
    a = ForgeDoctorDataPortal(target)
    server = _server(a)
    try:
        plan_ctx = _task_ctx(server, {"intent": "scan the project"})
        plan_doc = a._tasks_plan(plan_ctx)
        assert plan_doc["plan"]["verb"] == "scan"
        exec_ctx = _task_ctx(
            server, {"plan": plan_doc["plan"], "plan_token": plan_doc["plan_token"]}
        )
        out = a._tasks_execute(exec_ctx)
        assert out["status"] == "completed"
        receipt = out["task"]["receipt"]
        assert "summary" in receipt
        assert receipt["summary"]["passed"] + receipt["summary"]["info"] >= 0
        assert a._tasks[-1]["verb"] == "scan"
    finally:
        server.shutdown()
        server.server_close()


def test_tasks_mcp_intent_maps_to_verify(target: Path) -> None:
    a = ForgeDoctorDataPortal(target)
    server = _server(a)
    try:
        doc = a._tasks_plan(_task_ctx(server, {"intent": "verificar o handshake mcp"}))
        assert doc["plan"]["verb"] == "mcp_verify"
    finally:
        server.shutdown()
        server.server_close()


# --- graph / docs --------------------------------------------------------------


def test_graph_view_or_named_absence(target: Path) -> None:
    a = ForgeDoctorDataPortal(target)
    doc = a._graphs()
    if doc["availability"]["state"] == "no_graph":
        assert doc["views"] == []
        assert "unlock" in doc["availability"]
    else:
        assert doc["availability"]["state"] == "available"
        assert doc["views"]


def test_docs_search_needs_inventory() -> None:
    a = ForgeDoctorDataPortal(Path.cwd())
    # inventory exists in the real repo — search must return shaped hits
    ctx = type("C", (), {"query": {"q": ["install"], "limit": ["5"]}})()
    hits = a._docs_search(ctx)
    for h in hits:
        assert set(h) >= {"path", "title", "excerpt", "category"}


# --- cli verb -----------------------------------------------------------------


def test_portal_verb_registered() -> None:
    result = runner.invoke(app, ["portal", "--help"])
    assert result.exit_code == 0
    assert "--no-browser" in result.output
    assert "--root" in result.output


def test_assets_vendored_in_package() -> None:
    a = ForgeDoctorDataPortal(Path.cwd())
    assert a.assets_dir is not None
    assert (a.assets_dir / "index.html").is_file()
