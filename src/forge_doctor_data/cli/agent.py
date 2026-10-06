"""Agent-facing compact context commands."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer

from forge_doctor_data.cli.app import app

agent_app = typer.Typer(name="agent", help="Deterministic, budget-aware agent context.")
app.add_typer(agent_app, name="agent")

PathArg = Annotated[Path, typer.Argument(help="Project directory.")]
JsonOption = Annotated[bool, typer.Option("--json", help="Emit JSON (default).")]


def _emit(payload: object, as_json: bool) -> None:
    if as_json:
        typer.echo(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    typer.echo(json.dumps(payload, indent=2, ensure_ascii=False))


@agent_app.command(name="manifest")
def agent_manifest(path: PathArg = Path("."), as_json: JsonOption = True) -> None:
    """Emit compact domains, risks, capabilities, and evidence references."""
    from forge_doctor_data.core.agent_context import manifest

    _emit(manifest(path), as_json)


@agent_app.command(name="context")
def agent_context(
    path: PathArg = Path("."),
    budget: Annotated[int, typer.Option("--budget", min=1)] = 8000,
    as_json: JsonOption = True,
) -> None:
    """Emit summary-first context constrained by an approximate token budget."""
    from forge_doctor_data.core.agent_context import context

    _emit(context(path, budget), as_json)


@agent_app.command(name="delta")
def agent_delta(
    path: PathArg = Path("."),
    since: Annotated[Path | None, typer.Option("--since")] = None,
    as_json: JsonOption = True,
) -> None:
    """Emit added/removed/unchanged finding fingerprints."""
    from forge_doctor_data.core.agent_context import delta

    if since is None:
        typer.echo("--since is required", err=True)
        raise typer.Exit(2)
    try:
        _emit(delta(path, since), as_json)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(2) from exc


@agent_app.command(name="evidence")
def agent_evidence(
    reference: Annotated[str, typer.Argument(help="finding:<fingerprint> or entity:<id>.")],
    path: PathArg = Path("."),
    as_json: JsonOption = True,
) -> None:
    """Resolve one lazy evidence reference."""
    from forge_doctor_data.core.agent_context import evidence

    try:
        _emit(evidence(reference, path), as_json)
    except ValueError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1) from exc
