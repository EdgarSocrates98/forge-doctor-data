"""``forge-doctor-data portal`` — optional local web UI over the real services.

Serves the Forge Portal on 127.0.0.1 with a session token: install status,
host detection, MCP verification, project scan and the evidence graph —
the same truth the CLI reports. The portal is additive: every CLI verb,
the MCP server and the TUI keep working with or without it. Mutations go
through confirm + signed plan token, exactly like ``install --yes``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer

from forge_doctor_data.cli.app import app


@app.command(name="portal")
def portal_cmd(
    no_browser: Annotated[
        bool,
        typer.Option(
            "--no-browser", help="Print the URL instead of opening a browser (SSH/remote)."
        ),
    ] = False,
    port: Annotated[
        int,
        typer.Option("--port", help="Port to bind (default: free port)."),
    ] = 0,
    root: Annotated[
        Path | None,
        typer.Option("--root", help="Workspace root (default: cwd)."),
    ] = None,
) -> None:
    """Serve the optional local portal over the real services (127.0.0.1)."""
    import webbrowser

    from forge_doctor_data import _forge_portal as fp
    from forge_doctor_data.portal_adapter import ForgeDoctorDataPortal

    workspace = Path(root).resolve() if root else Path.cwd()
    adapter = ForgeDoctorDataPortal(workspace)
    if adapter.assets_dir is None:
        typer.echo(
            json.dumps(
                {
                    "refusal": "FDD-PORTAL-NO-ASSETS",
                    "status": "refused",
                    "detail": (
                        "portal assets not vendored — run "
                        "`python scripts/vendor.py` in forge-portal"
                    ),
                },
                indent=2,
            )
        )
        raise typer.Exit(code=1)
    server = fp.PortalServer(adapter, port=port, quiet=True)
    typer.echo(
        json.dumps(
            {"url": server.url, "note": "portal is optional — CLI/MCP keep working without it"}
        )
    )
    if not no_browser:
        webbrowser.open(server.url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        server.server_close()
