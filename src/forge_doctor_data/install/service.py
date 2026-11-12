"""Portable install lifecycle for Forge Doctor Data — the ``forge/*``
contract v1 implemented over the vendored installkit
(``forge_doctor_data._installkit``).

The generic engine (ledger, lock, receipts, marker blocks, managed
``.mcp.json`` key, scope resolution, drift, MCP handshake) lives in the
installkit; this module carries the ``ForgeSpec`` for Forge Doctor Data and
the typed wrappers the CLI calls.

Forge Doctor Data publishes no host skill/agent mirrors today — all
profiles install the managed MCP key plus the shared ``forge/context/v1``
workspace registration (capability manifest + ``forge:*`` doc blocks).
``spawn_ok`` stays ``True``: subprocess is used only by
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
from forge_doctor_data import _forgecontext as fctx
from forge_doctor_data import _installkit as kit

FORGE_ID = "forge-doctor-data"
STATE_DIR = ".forge-doctor-data/install"
PROFILES: tuple[str, ...] = ("minimal", "recommended", "full")
GATEWAY_PROFILES: tuple[str, ...] = ("economy", "balanced", "deep")
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
        mcp_verify_tool="get_execution_baseline",
        version_cmd=("--version",),
        render_assets=_render_for,
        # Consumer docs (AGENTS.md/CLAUDE.md/AGENT_PROTOCOL.md) belong to
        # the forge_context layer — `forge:<forge-id>` blocks + the
        # consolidated protocol, not `forge-doctor-data:managed` markers
        # (same migration as the api-forge/spark-aws/platform/data-sentinel
        # siblings).
        marker_files=(),
        marker_body="",
        user_state_dir="~/.forge-doctor-data",
    )


def _render_for(ctx: kit.InstallContext) -> dict[str, bytes]:
    # No repo-authored host mirrors exist today; the managed MCP key and
    # `forge:*` doc blocks are emitted by the engines themselves.
    return {}


def _ctx(
    scope: str,
    root: Path | None,
    hosts: tuple[str, ...],
    profile: str,
    dry_run: bool,
    components: tuple[str, ...] | None = None,
    gateway_profile: str = "balanced",
) -> kit.InstallContext:
    spec = _spec()
    target = kit.resolve_scope(spec, scope, Path.cwd(), root)
    options = kit.component_options(profile, components)
    options["execution_profile"] = gateway_profile
    return kit.InstallContext(
        spec=spec,
        scope=scope,
        root=target,
        state_dir=kit.state_dir_for(spec, scope, target),
        profile=profile,
        hosts=hosts,
        dry_run=dry_run,
        options=options,
    )


def _hosts(host: str) -> tuple[str, ...]:
    """``all`` → todos; ``none``/vazio → opt-out explícito (nunca todos);
    nome único ou csv → subconjunto validado (GAP-003)."""
    if host == "all":
        return HOSTS
    if not host or host == "none":
        return ()
    nomes = [h.strip() for h in host.split(",") if h.strip()]
    desconhecidos = [h for h in nomes if h not in HOSTS]
    if desconhecidos:
        raise kit.InstallError(
            kit.E_HOST, f"host {desconhecidos[0]!r}; known: {list(HOSTS)} + all,none"
        )
    return tuple(dict.fromkeys(nomes))


def install(
    host: str = "all",
    *,
    scope: str = "project",
    root: Path | None = None,
    profile: str = "recommended",
    yes: bool = False,
    dry_run: bool = False,
    components: tuple[str, ...] | None = None,
    gateway_profile: str = "balanced",
) -> dict[str, Any]:
    """Apply the installation to the resolved target. Without ``yes`` or
    ``dry_run`` writes are refused — the plan is the contract."""
    if profile not in PROFILES:
        raise kit.InstallError(kit.E_PROFILE, f"profile {profile!r}; {PROFILES}")
    if gateway_profile not in GATEWAY_PROFILES:
        raise kit.InstallError(
            kit.E_PROFILE,
            f"gateway_profile {gateway_profile!r}; {GATEWAY_PROFILES}",
        )
    ctx = _ctx(
        scope,
        root,
        _hosts(host),
        profile,
        dry_run,
        components=components,
        gateway_profile=gateway_profile,
    )
    state = ctx.state_dir
    with kit.acquire_lock(state):
        receipt = kit.apply_install(ctx, approved=yes)
        # Receipt + registry writes stay inside the install lock — a
        # context-registry BLOCKED flips the receipt to "failed" before
        # it is persisted, never a silent "completed".
        if not dry_run and receipt.get("status") == "completed":
            _register_context(ctx, receipt)
            _drop_stale_doc_entries(ctx)
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
        receipt = kit.repair(ctx)
        # Context registry recovery: unwedge the journal, reclaim stale
        # locks, rebuild registry+ROUTING.md — only when `.forge/context/`
        # already exists (repair never creates residue on a pristine
        # root).
        if (ctx.root / fctx.CONTEXT_DIR).exists():
            try:
                out_ctx = fctx.repair_context(ctx.root)
                receipt["repaired"].extend(f"context:{w}" for w in out_ctx["written"])
                rec = out_ctx.get("recovered")
                receipt.setdefault("checks", []).append(
                    {
                        "id": "context-registry",
                        "status": "PASS",
                        "detail": (
                            f"{out_ctx['status']} ({len(out_ctx['written'])} writes)"
                            + (f"; recovered {rec['op']}:{rec['forge_id']}" if rec else "")
                            + ("; stale lock reclaimed" if out_ctx.get("lock_recovered") else "")
                        ),
                    }
                )
            except fctx.ContextError as exc:
                receipt["skipped"].append(f"context:{exc.kind}")
                receipt.setdefault("checks", []).append(
                    {
                        "id": "context-registry",
                        "status": "BLOCKED",
                        "detail": f"{exc.kind}: {exc.detail}",
                    }
                )
        # `forge:*` consumer-doc blocks: deterministic re-assert from the
        # manifests under `.forge/context/` — user content outside the
        # markers is never touched.
        try:
            out_docs = fctx.repair_docs(ctx.root, legacy_tags=_LEGACY_DOC_TAGS)
            receipt["repaired"].extend(f"docs:{w}" for w in out_docs["written"])
            receipt.setdefault("checks", []).append(
                {
                    "id": "consumer-docs",
                    "status": "PASS",
                    "detail": f"{out_docs['status']} ({len(out_docs['written'])} writes)",
                }
            )
        except fctx.ContextError as exc:
            receipt["skipped"].append(f"docs:{exc.kind}")
            receipt.setdefault("checks", []).append(
                {"id": "consumer-docs", "status": "BLOCKED", "detail": f"{exc.kind}: {exc.detail}"}
            )
        return receipt


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
        doc = kit.uninstall(ctx, purge_state=purge)
        # The context transaction acquires its own lock and would create
        # `.forge/context/` on a pristine root — only run it when residue
        # actually exists.
        if _docs_leftovers(ctx.root):
            checks = _unregister_context(ctx.root)
            doc.setdefault("checks", []).extend(checks)
            if any(c.get("status") == "BLOCKED" for c in checks):
                doc["status"] = "failed"
    return doc


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


# --------------------------------------------------------------------------
# forge-context/v1 wiring (install-2.0 — same design as the
# api-forge/spark-aws/platform-forge/data-sentinel siblings). `.forge/context/`
# is the workspace-level registry shared between forges — a different layer
# from `~/.forge/installations/` (account) and `.forge-doctor-data/install/`
# (ownership ledger). This forge only ever registers/unregisters its own
# `forge_id`.
# --------------------------------------------------------------------------

_PKG_DIR = Path(__file__).resolve().parents[1]
_REPO_DIR = _PKG_DIR.parent.parent  # src/forge_doctor_data -> repo root

# Marker tags from earlier generations (`forge-doctor-data:managed` emitted
# by the generic installkit); `install_docs`/`uninstall_docs` strip them
# while converging the consumer docs to `forge:*` blocks.
_LEGACY_DOC_TAGS: tuple[str, ...] = ("forge-doctor-data:managed",)
_CONSUMER_DOCS: tuple[str, ...] = ("AGENTS.md", "CLAUDE.md", "AGENT_PROTOCOL.md")

_AGENTS_DIR = _PKG_DIR / "installation" / "assets" / "agents"

_DOCTOR_DOMAINS: tuple[str, ...] = (
    "data-platform-diagnostics",
    "data-quality",
    "data-contracts",
    "pipeline-lineage",
    "apache-spark",
    "cloud-data-services",
)


def _mds(base: Path) -> list[str]:
    return sorted(p.stem for p in base.glob("*.md")) if base.is_dir() else []


def _drop_stale_doc_entries(ctx: kit.InstallContext) -> None:
    """Drop old ledger entries for the consumer docs: the files are now
    managed by the forge_context layer (`forge:*` blocks), not by whole-
    file hashes — user content outside the markers is not drift."""
    ledger = kit.Ledger.load(ctx.state_dir)
    changed = False
    for name in _CONSUMER_DOCS:
        if ledger.get(name) is not None:
            ledger.drop(name)
            changed = True
    if changed:
        ledger.save()


def _context_manifest(ctx: kit.InstallContext) -> dict[str, Any]:
    """The ``forge/context/v1`` manifest built from real sources:
    ``forge.json`` / ``forge.agentic.json`` (repo root) and the bundled
    agent specs under ``installation/assets/agents``."""

    def _bundled_json(name: str) -> dict[str, Any] | None:
        for cand in (_PKG_DIR / name, _REPO_DIR / name):
            data = kit._load_json(cand, None)
            if isinstance(data, dict):
                return data
        return None

    forge_json = _bundled_json("forge.json")
    agentic = _bundled_json("forge.agentic.json")
    agents = _mds(_AGENTS_DIR)

    hosts = sorted(set(ctx.hosts) & set(fctx.HOSTS))
    checks: list[dict[str, Any]] = [
        {
            "id": "agent-specs",
            "status": "PASS" if agents else "UNVERIFIED",
            "detail": f"{len(agents)} bundled agent specs",
        },
    ]
    return fctx.build_manifest(
        forge_id=FORGE_ID,
        name="Forge Doctor Data",
        version=__version__,
        cli="forge-doctor-data",
        package="forge_doctor_data",
        distribution="forge-doctor-data",
        python_spec=">=3.11",
        scope=ctx.scope,
        profile=ctx.profile,
        hosts=hosts,
        forge_json=forge_json,
        agentic=agentic,
        kind="diagnostic-provider",
        domains=_DOCTOR_DOMAINS,
        agents=agents,
        protocols=(
            {"id": "forge/v1", "version": "1"},
            {"id": "forge/context/v1", "version": "1"},
            {"id": "forge/context-registry/v1", "version": "1"},
        ),
        discovery_commands=(
            {
                "id": "scan",
                "argv": ["forge-doctor-data", "scan", "{target}"],
                "mode": "diagnostic-only",
                "read_only": True,
                "description": "independent data-platform diagnostic",
            },
            {
                "id": "diagnose",
                "argv": ["forge-doctor-data", "diagnose", "{target}"],
                "mode": "diagnostic-only",
                "read_only": True,
                "description": "data findings diagnosis",
            },
            {
                "id": "doctor",
                "argv": ["forge-doctor-data", "install", "doctor"],
                "mode": "diagnostic-only",
                "read_only": True,
                "description": "installation + environment health",
            },
        ),
        mcp={
            "server_name": "forge-doctor-data",
            "command": ["forge-doctor-data", "mcp"],
            "verify_tool": "get_execution_baseline",
        },
        resources={
            "agents-bundle": {
                "kind": "bundled",
                "location": "forge_doctor_data/installation/assets/agents",
                "optional": False,
            },
            "install-ledger": {
                "kind": "referenced",
                "location": ".forge-doctor-data/install",
                "optional": True,
            },
        },
        # `fix`/`remediate` only write when an explicit `--apply` flag is
        # passed; `init` scaffolds project config — all approval-gated.
        mutating_verbs=("install", "uninstall", "repair", "init", "fix", "remediate"),
        requires_approval=("install", "uninstall", "fix", "remediate"),
        offline_available=True,
        health={
            "status": "healthy" if agents else "degraded",
            "checks": checks,
        },
        components=ctx.options or None,
        recorded_by="forge-doctor-data",
    )


def _register_context(ctx: kit.InstallContext, receipt: dict[str, Any]) -> None:
    """Write `.forge/context/` — manifest + registry entry + ROUTING.md +
    consumer docs — in ONE transaction (install-2.0 §9.2). A failure
    becomes a named BLOCKED check and the receipt reports "failed"
    (registry is a mandatory component), never a silent "completed".
    ``scope=user`` resolves to ``~``: `~/.forge/` is account-level —
    workspace context is never written there (same rule as siblings)."""
    if ctx.scope == "user":
        return
    try:
        manifest = _context_manifest(ctx)
        out = fctx.install_transaction(
            ctx.root, manifest, owner=FORGE_ID, legacy_tags=_LEGACY_DOC_TAGS
        )
        receipt.setdefault("checks", []).append(
            {
                "id": "context-registry",
                "status": "PASS",
                "detail": f".forge/context {out['status']} ({len(out['written'])} writes)",
            }
        )
        docs = out["docs"]
        receipt.setdefault("checks", []).append(
            {
                "id": "consumer-docs",
                "status": "PASS",
                "detail": f"{docs['status']}: {len(docs['written'])} written, "
                f"{len(docs['kept'])} kept",
            }
        )
    except fctx.ContextError as exc:
        receipt.setdefault("checks", []).append(
            {"id": "context-registry", "status": "BLOCKED", "detail": f"{exc.kind}: {exc.detail}"}
        )
        receipt["status"] = "failed"


def _unregister_context(root: Path) -> list[dict[str, Any]]:
    """Remove this forge's manifest/entry/`forge:*` blocks in ONE
    transaction (§9.2) — only own artifacts; shared docs regenerate for
    the survivors."""
    try:
        out = fctx.uninstall_transaction(
            root, FORGE_ID, owner=FORGE_ID, legacy_tags=_LEGACY_DOC_TAGS
        )
        docs = out["docs"]
        return [
            {
                "id": "context-registry",
                "status": "PASS",
                "detail": f".forge/context {out['status']}",
            },
            {
                "id": "consumer-docs",
                "status": "PASS",
                "detail": f"{docs['status']}: {len(docs['written'])} changed",
            },
        ]
    except fctx.ContextError as exc:
        return [
            {
                "id": "context-registry",
                "status": "BLOCKED",
                "detail": f"{exc.kind}: {exc.detail}",
            }
        ]


def _docs_leftovers(root: Path) -> bool:
    """True when the target still carries forge_context residue — a
    lock-free read; only a hit justifies the write path (we never create
    `.forge/context/` on a pristine root)."""
    if (root / fctx.CONTEXT_DIR).exists():
        return True
    needles = (
        f"forge:{FORGE_ID}:",
        f"{fctx.DOC_TAG_ECOSYSTEM}:",
        fctx.PROTOCOL_SENTINEL,
        *_LEGACY_DOC_TAGS,
    )
    for name in _CONSUMER_DOCS:
        path = root / name
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if any(n in text for n in needles):
            return True
    return False


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
