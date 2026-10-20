"""`forge-doctor-data golden` - full-output snapshot regression suites."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from forge_doctor_data.cli.app import app
from forge_doctor_data.cli.common import _stderr
from forge_doctor_data.core.golden import (
    GOLDEN_ROOT,
    discover_golden,
    run_all_golden,
    update_golden,
)

golden_app = typer.Typer(name="golden", help="Golden repositories - snapshot regression suites.")
app.add_typer(golden_app, name="golden")

_RootOpt = Annotated[Path, typer.Option("--root", help="Golden corpus root.")]
_JsonOpt = Annotated[bool, typer.Option("--json", help="Machine-readable output.")]


def _golden_root(root: Path, *, for_write: bool = False) -> Path:
    """cwd/explicit root wins; packaged `_data/golden` is the read fallback."""
    if root.is_dir() or root != Path(GOLDEN_ROOT):
        return root
    from forge_doctor_data.cli.common import _packaged_dir

    packaged = _packaged_dir("_data/golden")
    if not packaged.is_dir():
        return root
    if for_write:
        _stderr.print(
            f"[red]packaged golden corpus is read-only[/red] ({packaged})\n"
            "pass --root <dir> to regenerate snapshots in a writable copy."
        )
        raise typer.Exit(2)
    return packaged


@golden_app.command(name="list")
def golden_list(root: _RootOpt = Path(GOLDEN_ROOT)) -> None:
    """List golden repositories."""
    root = _golden_root(root)
    repos = discover_golden(root)
    if not repos:
        _stderr.print(f"[yellow]no golden repos under[/yellow] {root}")
        raise typer.Exit(1)
    console = Console()
    console.print(f"[bold]Golden repos[/bold]  {root}")
    for r in repos:
        snap = "snapshot" if (r.parent / "expected").is_dir() else "no snapshot"
        console.print(f"  {r.parent.name}  [dim]{snap}[/dim]")


@golden_app.command(name="run")
def golden_run(
    name: Annotated[str | None, typer.Argument(help="Repo name (default: all).")] = None,
    root: _RootOpt = Path(GOLDEN_ROOT),
    as_json: _JsonOpt = False,
) -> None:
    """Diff current engine output against stored snapshots."""
    root = _golden_root(root)
    reports = run_all_golden(root, name)
    if as_json:
        typer.echo(
            json.dumps(
                {
                    r.name: {
                        "passed": r.passed,
                        "missing_snapshot": r.missing_snapshot,
                        "errors": r.errors,
                        "diffs": [
                            {
                                "artifact": d.artifact,
                                "added": list(d.added),
                                "removed": list(d.removed),
                            }
                            for d in r.diffs
                        ],
                    }
                    for r in reports
                },
                indent=2,
            )
        )
    else:
        console = Console()
        console.print()
        console.print(f"[bold]Golden repos[/bold]  {root}")
        for r in reports:
            status = "[green]PASS[/green]" if r.passed else "[red]FAIL[/red]"
            console.print(f"  {status} {r.name}")
            for m in r.missing_snapshot:
                console.print(f"      [yellow]no snapshot:[/yellow] {m}")
            for e in r.errors:
                console.print(f"      [red]error:[/red] {e}")
            for d in r.diffs:
                console.print(f"      [red]{d.artifact}:[/red] +{len(d.added)} -{len(d.removed)}")
                for row in d.added[:3]:
                    console.print(f"        + {row}")
                for row in d.removed[:3]:
                    console.print(f"        - {row}")
        passed = sum(1 for r in reports if r.passed)
        console.print(f"\n  {passed} passed, {len(reports) - passed} failed")
    if not reports or any(not r.passed for r in reports):
        raise typer.Exit(1)


@golden_app.command(name="update")
def golden_update(
    name: Annotated[str | None, typer.Argument(help="Repo name (default: all).")] = None,
    root: _RootOpt = Path(GOLDEN_ROOT),
) -> None:
    """Regenerate snapshots — review the diff before committing."""
    root = _golden_root(root, for_write=True)
    repos = discover_golden(root)
    updated = 0
    for repo_dir in repos:
        if name and repo_dir.parent.name != name:
            continue
        update_golden(repo_dir)
        updated += 1
    console = Console()
    console.print(f"[bold]golden update[/bold] — regenerated {updated} snapshot(s)")
    if not updated:
        _stderr.print(f"[yellow]no golden repos under[/yellow] {root}")
        raise typer.Exit(1)
