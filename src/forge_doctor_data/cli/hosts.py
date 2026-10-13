"""``forge-doctor-data hosts`` — observe AI host CLIs, launch one on a TTY.

Read-only by default: reports binary, version, auth state and this
project's forge integration per host. ``--launch`` with an explicit host
opens it in the repository — never through MCP, never while signed out.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer

from forge_doctor_data.cli.app import app
from forge_doctor_data.integrations.hostflow import HOST_NAMES, hosts_flow


@app.command(name="hosts")
def hosts_cmd(
    target: Annotated[
        str,
        typer.Argument(help="claude|devin|codex|copilot|all"),
    ] = "all",
    launch: Annotated[
        bool,
        typer.Option("--launch", help="Open the host in this repo (TTY only)."),
    ] = False,
    root: Annotated[
        Path,
        typer.Option("--root", help="Repository to observe (default: cwd)."),
    ] = Path("."),
) -> None:
    """Observe AI host CLIs and this project's integration with them."""
    if target not in (*HOST_NAMES, "all"):
        typer.echo(
            json.dumps(
                {
                    "status": "refused",
                    "reason": "host_unknown",
                    "host": target,
                    "known": [*HOST_NAMES, "all"],
                },
                indent=2,
            )
        )
        raise typer.Exit(2)
    doc = hosts_flow(target, repo=root, launch=launch)
    typer.echo(json.dumps(doc, indent=2, ensure_ascii=False))
    if doc.get("launched"):
        raise typer.Exit(int(doc.get("host_exit_code") or 0))
