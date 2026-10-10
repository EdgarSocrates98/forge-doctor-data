"""Typer application object and root callback.

Kept dependency-free: command modules import ``app`` from here and register
themselves, so this module never imports them (no circularity).
"""

from __future__ import annotations

from typing import Annotated

import typer

from forge_doctor_data import __version__

app = typer.Typer(
    name="forge-doctor-data",
    help="Deterministic diagnostics for data engineering projects.",
    epilog=(
        "Start here: forge-doctor-data scan .  |  "
        "forge-doctor-data checks  |  forge-doctor-data explain <CHECK-ID>\n\n"
        "Docs & issues: https://github.com/EdgarSocrates98/forge-doctor-data"
    ),
    invoke_without_command=True,
    add_completion=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"forge-doctor-data {__version__}")
        raise typer.Exit()


@app.callback()
def _main(
    ctx: typer.Context,
    version: Annotated[
        bool, typer.Option("--version", callback=_version_callback, is_eager=True)
    ] = False,
) -> None:
    """Deterministic diagnostics for data engineering projects."""
    import sys

    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")
    if ctx.invoked_subcommand is None:
        import sys as _sys

        if _sys.stdin.isatty() and _sys.stdout.isatty():
            try:
                from forge_doctor_data.ui.home import run_home
                from forge_doctor_data.ui.kit import NonInteractive

                try:
                    raise typer.Exit(run_home())
                except NonInteractive:
                    pass
            except ImportError:
                pass
        typer.echo(ctx.get_help())
        raise typer.Exit()
