"""Evidence collector contract utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from forge_doctor_data.cli.app import app
from forge_doctor_data.core.collectors import load_bundle

collector_app = typer.Typer(name="collector", help="Validate normalized evidence bundles.")
app.add_typer(collector_app, name="collector")


@collector_app.command(name="validate")
def collector_validate(
    path: Annotated[Path, typer.Argument(help="Normalized evidence bundle JSON.")],
    as_json: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    """Validate a bundle before offline analysis consumes it."""
    try:
        payload = load_bundle(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        if as_json:
            typer.echo(json.dumps({"valid": False, "errors": [str(exc)]}))
        else:
            Console().print(f"[red]invalid[/red] {exc}")
        raise typer.Exit(1) from exc
    if as_json:
        typer.echo(json.dumps({"valid": True, "schema": payload["schema"]}, indent=2))
    else:
        records = payload.get("records")
        record_count = len(records) if isinstance(records, list) else 0
        Console().print(f"[green]valid[/green] {payload['collector']} records={record_count}")
