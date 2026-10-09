"""Portable install lifecycle for Forge Doctor Data — the ``forge/*``
contract v1 implemented over the vendored installkit
(``forge_doctor_data._installkit``).

The generic engine (ledger, lock, receipts, marker blocks, managed
``.mcp.json`` key, scope resolution, drift, MCP handshake) lives in the
installkit; this module carries the ``ForgeSpec`` for Forge Doctor Data and
the typed wrappers the CLI calls.

Forge Doctor Data publishes no host skill/agent mirrors today — all
profiles install the managed MCP key plus AGENTS.md/CLAUDE.md marker
blocks. ``spawn_ok`` stays ``True``: subprocess is used only by
``install mcp-verify``/``install update`` and never on the diagnostic
scan path (the offline guarantee of the engine is unchanged).
"""

from __future__ import annotations

import importlib.util
import subprocess  # install lifecycle only — never on the scan path
import sys
from pathlib import Path
from typing import Any

from forge_doctor_data import __version__
from forge_doctor_data import _installkit as kit

FORGE_ID = "forge-doctor-data"
STATE_DIR = ".forge-doctor-data/install"
PROFILES: tuple[str, ...] = ("minimal", "recommended", "full")
SCOPES: tuple[str, ...] = ("project", "workspace", "user")
HOSTS: tuple[str, ...] = ("claude", "devin", "codex", "copilot")


def _spec() -> kit.ForgeSpec:
    return kit.ForgeSpec(
        forge_id=FORGE_ID,
        package="forge_doctor_data",
        distribution="forge-doctor-data",
        cli_name="forge-doctor-data",
        python_spec=">=3.11",
        state_dir=STATE_DIR,
        mcp_command=("forge-doctor-data", "mcp"),
        mcp_server_name="forge-doctor-data",
        version_cmd=("--version",),
        render_assets=_render_for,
        marker_files=("AGENTS.md", "CLAUDE.md"),
        marker_body=(
            "**Forge Doctor Data** is installed in this project.\n\n"
            "- MCP server: `forge-doctor-data` (managed key in `.mcp.json`)\n"
            "- Lifecycle: `forge-doctor-data install "
            "status|doctor|repair|uninstall`\n\n"
            "Content between the `forge-doctor-data:managed` markers is "
            "managed; content outside belongs to the user."
        ),
        user_state_dir="~/.forge-doctor-data",
    )


def _render_for(ctx: kit.InstallContext) -> dict[str, bytes]:
    # No repo-authored host mirrors exist today; the managed MCP key and
    # marker blocks are emitted by the engine itself.
    return {}


def _ctx(
    scope: str,
    root: Path | None,
    hosts: tuple[str, ...],
    profile: str,
    dry_run: bool,
) -> kit.InstallContext:
    spec = _spec()
    target = kit.resolve_scope(spec, scope, Path.cwd(), root)
    return kit.InstallContext(
        spec=spec,
        scope=scope,
        root=target,
        state_dir=kit.state_dir_for(spec, scope, target),
        profile=profile,
        hosts=hosts,
        dry_run=dry_run,
    )


def _hosts(host: str) -> tuple[str, ...]:
    if host == "all":
        return HOSTS
    if host not in HOSTS:
        raise kit.InstallError(kit.E_HOST, f"host {host!r}; known: {list(HOSTS)} + all")
    return (host,)


def install(
    host: str = "all",
    *,
    scope: str = "project",
    root: Path | None = None,
    profile: str = "recommended",
    yes: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Apply the installation to the resolved target. Without ``yes`` or
    ``dry_run`` writes are refused — the plan is the contract."""
    if profile not in PROFILES:
        raise kit.InstallError(kit.E_PROFILE, f"profile {profile!r}; {PROFILES}")
    ctx = _ctx(scope, root, _hosts(host), profile, dry_run)
    state = ctx.state_dir
    with kit.acquire_lock(state):
        receipt = kit.apply_install(ctx, approved=yes)
    if not dry_run and receipt.get("status") == "completed":
        kit._write_receipt(state, receipt)
        _register(ctx)
    return receipt


def status(*, scope: str = "project", root: Path | None = None) -> dict[str, Any]:
    ctx = _ctx(scope, root, (), "recommended", dry_run=True)
    return kit.status(ctx)


def doctor(*, scope: str = "project", root: Path | None = None) -> dict[str, Any]:
    ctx = _ctx(scope, root, (), "recommended", dry_run=True)
    doc = kit.doctor(ctx)
    if importlib.util.find_spec("mcp") is None:
        doc["checks"] = [
            c
            if c["id"] != "mcp-handshake"
            else {
                **c,
                "status": "UNVERIFIED",
                "detail": "extra 'mcp' not installed — handshake not tested",
            }
            for c in doc["checks"]
        ]
        if not any(c["status"] == "FAIL" for c in doc["checks"]):
            doc["status"] = "healthy" if doc["status"] != "broken" else doc["status"]
    return doc


def repair(
    *,
    scope: str = "project",
    root: Path | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    ctx = _ctx(scope, root, HOSTS, "full", dry_run)
    if dry_run:
        return kit.status(ctx)
    with kit.acquire_lock(ctx.state_dir):
        return kit.repair(ctx)


def uninstall(
    *,
    scope: str = "project",
    root: Path | None = None,
    purge: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    ctx = _ctx(scope, root, (), "recommended", dry_run)
    if dry_run:
        st = kit.status(ctx)
        return {
            "schema": kit.SCHEMA_RECEIPT,
            "forge_id": FORGE_ID,
            "operation": "uninstall",
            "scope": scope,
            "dry_run": True,
            "would_remove": st.get("drift", {}),
            "status": "planned",
            "verification": {"status": "UNVERIFIED"},
            "created_at": kit._utc_now(),
        }
    with kit.acquire_lock(ctx.state_dir):
        return kit.uninstall(ctx, purge_state=purge)


def update(
    *,
    to: str | None = None,
    repo: Path | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Upgrade the runtime installed by the bootstrap; ``to`` is always
    pinned — ``latest`` is never installable."""
    if to == "latest":
        return _failed("version", "'latest' is never installable")
    manifest = _installation_manifest()
    src = repo or (Path(p) if (p := (manifest.get("source") or {}).get("path")) else None)
    if src is None or not src.exists():
        return _failed(
            "source",
            "no checkout registered — install via scripts/forge_bootstrap.py",
            "BLOCKED",
        )
    venv = manifest.get("venv")
    if not venv:
        return _failed("source", "no venv registered; run scripts/forge_bootstrap.py")
    venv_py = Path(venv) / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    if not venv_py.exists():
        return _failed("venv", f"venv {venv} incomplete")
    cmd = [str(venv_py), "-m", "pip", "install", "--upgrade", str(src)]
    if dry_run:
        return _receipt(
            "update",
            [{"id": "pip", "status": "UNVERIFIED", "detail": " ".join(cmd)}],
            "planned",
        )
    proc = subprocess.run(  # venv python + fixed pip args — no shell
        cmd, capture_output=True, text=True, timeout=900, check=False
    )
    checks = [
        {
            "id": "pip",
            "status": "PASS" if proc.returncode == 0 else "FAIL",
            "detail": (proc.stdout or proc.stderr)[-300:],
        }
    ]
    return _receipt("update", checks, "completed" if proc.returncode == 0 else "failed")


def mcp_verify() -> dict[str, Any]:
    return kit.mcp_verify(_spec())


# --------------------------------------------------------------------------


def _receipt(operation: str, checks: list[dict[str, Any]], status: str) -> dict[str, Any]:
    return {
        "schema": kit.SCHEMA_RECEIPT,
        "forge_id": FORGE_ID,
        "operation": operation,
        "managed_files": [],
        "checks": checks,
        "verification": {
            "status": "PASS"
            if all(c["status"] in ("PASS", "NOT_APPLICABLE", "UNVERIFIED") for c in checks)
            else "FAIL"
        },
        "status": status,
        "created_at": kit._utc_now(),
        "created_by": f"forge-doctor-data/{__version__}",
    }


def _failed(check_id: str, detail: str, status: str = "failed") -> dict[str, Any]:
    return _receipt("update", [{"id": check_id, "status": "FAIL", "detail": detail}], status)


def _installation_manifest() -> dict[str, Any]:
    path = kit.installations_dir() / f"{FORGE_ID}.json"
    doc = kit._load_json(path, None)
    return doc if isinstance(doc, dict) else {}


def _register(ctx: kit.InstallContext) -> None:
    """Merge ``~/.forge/installations/forge-doctor-data.json`` without losing
    bootstrap fields (venv, source)."""
    existing = _installation_manifest()
    doc: dict[str, Any] = dict(existing)
    doc.update(
        {
            "schema": kit.SCHEMA_MANIFEST,
            "forge_id": FORGE_ID,
            "package": "forge_doctor_data",
            "distribution": "forge-doctor-data",
            "cli": {
                "name": "forge-doctor-data",
                "version_cmd": ["forge-doctor-data", "--version"],
            },
            "version": __version__,
            "updated_at": kit._utc_now(),
            "installed_at": doc.get("installed_at", kit._utc_now()),
            "installed_by": doc.get(
                "installed_by",
                {"agent": "forge-doctor-data-cli", "version": __version__},
            ),
            "source": doc.get("source", {"kind": "project-install", "path": str(ctx.root)}),
        }
    )
    doc.setdefault("install_root", str(kit.installs_root() / FORGE_ID))
    doc.setdefault(
        "mcp",
        {
            "server_name": "forge-doctor-data",
            "command": ["forge-doctor-data", "mcp"],
            "verified": False,
        },
    )
    kit.register_installation(doc)


__all__ = [
    "FORGE_ID",
    "HOSTS",
    "PROFILES",
    "SCOPES",
    "doctor",
    "install",
    "mcp_verify",
    "repair",
    "status",
    "uninstall",
    "update",
]
