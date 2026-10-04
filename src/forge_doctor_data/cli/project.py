"""``project`` group - deterministic status generated from live registries (P3)."""

from __future__ import annotations

from typing import Annotated

import typer

from forge_doctor_data.cli.app import app
from forge_doctor_data.cli.common import _stderr
from forge_doctor_data.core.project_status import (
    STATUS_DOC,
    check_status_doc,
    collect_status,
    render_status_markdown,
    render_status_text,
    status_doc_path,
    status_json,
)
from forge_doctor_data.output.summary import INTERNAL_ERROR_EXIT

project_app = typer.Typer(
    name="project",
    help="Project self-inspection: generated status and doc-drift checks.",
)
app.add_typer(project_app, name="project")


@project_app.command(name="status")
def project_status(
    fmt: Annotated[str, typer.Option("--format", "-f", help="text|json|markdown")] = "text",
    write: Annotated[
        bool,
        typer.Option("--write", help=f"Regenerate {STATUS_DOC} (commit the diff)."),
    ] = False,
    check: Annotated[
        bool,
        typer.Option(
            "--check",
            help=f"Verify {STATUS_DOC} matches the live registries; exit 1 on drift.",
        ),
    ] = False,
) -> None:
    """Deterministic project status from source registries.

    Same inputs → same bytes: commands, checks, contracts, MCP tools,
    knowledge domains, and Loop Factory state are all read from their
    source of truth, sorted, and rendered without timestamps.
    """
    if fmt not in ("text", "json", "markdown"):
        _stderr.print(f"[red]Unknown format:[/red] {fmt} (text|json|markdown)")
        raise typer.Exit(INTERNAL_ERROR_EXIT)
    if write and check:
        _stderr.print("[red]--write and --check are mutually exclusive.[/red]")
        raise typer.Exit(INTERNAL_ERROR_EXIT)

    if check:
        drift = check_status_doc()
        if not drift:
            _stderr.print(f"[green]{STATUS_DOC} is up to date.[/green]")
            raise typer.Exit(0)
        _stderr.print(f"[red]{STATUS_DOC} is stale:[/red]")
        for line in drift[:60]:
            _stderr.print(f"[dim]{line}[/dim]")
        if len(drift) > 60:
            _stderr.print(f"[dim]... ({len(drift) - 60} more diff lines)[/dim]")
        _stderr.print("[red]Run `project status --write` and commit the result.[/red]")
        raise typer.Exit(INTERNAL_ERROR_EXIT)

    status = collect_status()
    if write:
        target = status_doc_path()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_status_markdown(status) + "\n", encoding="utf-8")
        _stderr.print(f"[green]{target} regenerated - commit the diff.[/green]")
        return

    if fmt == "json":
        typer.echo(status_json(status))
    elif fmt == "markdown":
        typer.echo(render_status_markdown(status))
    else:
        typer.echo(render_status_text(status))
