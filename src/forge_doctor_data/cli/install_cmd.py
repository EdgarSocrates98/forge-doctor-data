"""``forge-doctor-data install`` lifecycle — portable installation contract.

``forge-doctor-data install`` with no subcommand APPLIES the install to the
resolved scope (project by default); subcommands cover the rest of the
lifecycle. Writes require ``--yes``; ``--dry-run`` plans without touching
the filesystem.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Annotated, Any

import typer

from forge_doctor_data import _installkit as kit
from forge_doctor_data.cli.app import app
from forge_doctor_data.install import service

install_app = typer.Typer(
    name="install",
    help=(
        "Install Forge Doctor Data into a project, workspace or the user "
        "home; manage the lifecycle (status, doctor, repair, update, "
        "uninstall)."
    ),
    invoke_without_command=True,
    no_args_is_help=False,
)
app.add_typer(install_app, name="install")

ScopeOpt = Annotated[str, typer.Option("--scope", help="project|workspace|user.")]
HostOpt = Annotated[str, typer.Option("--host", help="claude|devin|codex|copilot|all.")]
ProfileOpt = Annotated[str, typer.Option("--profile", help="minimal|recommended|full.")]
RootOpt = Annotated[
    Path | None,
    typer.Option("--root", help="Target root (default: VCS root or cwd)."),
]
DryRunOpt = Annotated[bool, typer.Option("--dry-run", help="Plan only — writes nothing.")]


def _emit(doc: Any) -> None:
    typer.echo(json.dumps(doc, indent=2, ensure_ascii=False))


def _call(fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    try:
        return fn(*args, **kwargs)
    except kit.InstallError as exc:
        _emit(exc.document(service.FORGE_ID))
        raise typer.Exit(1) from exc


@install_app.callback()
def install_apply(
    ctx: typer.Context,
    scope: ScopeOpt = "project",
    host: HostOpt = "all",
    profile: ProfileOpt = "recommended",
    root: RootOpt = None,
    yes: Annotated[
        bool,
        typer.Option(
            "--yes",
            "-y",
            help="Explicit approval; without it only --dry-run is allowed.",
        ),
    ] = False,
    dry_run: DryRunOpt = False,
    components: Annotated[
        str | None,
        typer.Option(
            "--components",
            help="Optional components csv: skills,agents,mcp,tui,graph-studio.",
        ),
    ] = None,
) -> None:
    """Install Forge Doctor Data host assets into the resolved scope."""
    if ctx.invoked_subcommand is not None:
        return
    comps = (
        tuple(c.strip() for c in components.split(",") if c.strip())
        if components
        else None
    )
    doc = _call(
        service.install,
        host,
        scope=scope,
        root=root,
        profile=profile,
        yes=yes,
        dry_run=dry_run,
        components=comps,
    )
    _emit(doc)
    if doc.get("status") not in ("planned", "completed"):
        raise typer.Exit(1)


@install_app.command(name="status")
def install_status(scope: ScopeOpt = "project", root: RootOpt = None) -> None:
    """Report drift/health of the resolved installation."""
    doc = _call(service.status, scope=scope, root=root)
    _emit(doc)


@install_app.command(name="doctor")
def install_doctor(scope: ScopeOpt = "project", root: RootOpt = None) -> None:
    """Run installation health checks (ledger, MCP availability)."""
    doc = _call(service.doctor, scope=scope, root=root)
    _emit(doc)
    if doc.get("status") in ("degraded", "broken"):
        raise typer.Exit(1)


@install_app.command(name="repair")
def install_repair(
    scope: ScopeOpt = "project",
    root: RootOpt = None,
    dry_run: DryRunOpt = False,
) -> None:
    """Restore missing managed assets; user-modified content is kept."""
    doc = _call(service.repair, scope=scope, root=root, dry_run=dry_run)
    _emit(doc)


@install_app.command(name="uninstall")
def install_uninstall(
    scope: ScopeOpt = "project",
    root: RootOpt = None,
    purge: Annotated[
        bool,
        typer.Option("--purge", help="Also remove the forge state dir."),
    ] = False,
    dry_run: DryRunOpt = False,
) -> None:
    """Remove ledger-owned assets only; user content is preserved."""
    doc = _call(service.uninstall, scope=scope, root=root, purge=purge, dry_run=dry_run)
    _emit(doc)


@install_app.command(name="update")
def install_update(
    to: Annotated[
        str | None,
        typer.Option("--to", help="Pin a version (never 'latest')."),
    ] = None,
    repo: Annotated[
        Path | None,
        typer.Option("--repo", help="Checkout to upgrade from."),
    ] = None,
    dry_run: DryRunOpt = False,
) -> None:
    """Upgrade the bootstrapped runtime from its registered checkout."""
    doc = _call(service.update, to=to, repo=repo, dry_run=dry_run)
    _emit(doc)
    if doc.get("status") == "failed":
        raise typer.Exit(1)


@install_app.command(name="mcp-verify")
def install_mcp_verify() -> None:
    """Handshake the configured MCP server (PASS/BLOCKED/FAIL)."""
    doc = _call(service.mcp_verify)
    _emit(doc)
    if doc.get("status") == "FAIL":
        raise typer.Exit(1)


__all__ = ["install_app"]
