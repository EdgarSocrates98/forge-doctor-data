"""``inspect`` group - convergent domain verbs (P14).

``forge-doctor-data inspect <domain> [path]`` is the canonical
information-architecture entry point: one verb, the domain as the
argument. The historical ``<domain> inspect`` groups keep working
unchanged; these are aliases registered dynamically from the live
command registry, so new domains appear here automatically.

A domain is aliased only when its ``inspect`` callback can be driven
by a single ``path`` argument (no other required parameters).
"""

from __future__ import annotations

import inspect as _inspect
from collections.abc import Callable
from pathlib import Path
from typing import Any

import typer

from forge_doctor_data.cli.app import app
from forge_doctor_data.cli.common import PathArg

inspect_app = typer.Typer(
    name="inspect",
    help="Domain inspection: `inspect <domain> [path]` (alias of `<domain> inspect`).",
)
app.add_typer(inspect_app, name="inspect")


def _alias(domain: str, callback: Callable[..., Any]) -> Callable[..., None]:
    def cmd(path: PathArg = Path(".")) -> None:
        callback(path=path)

    cmd.__name__ = f"inspect_{domain.replace('-', '_')}"
    doc = (callback.__doc__ or "").strip().splitlines()
    cmd.__doc__ = f"Alias of `{domain} inspect`. " + (doc[0] if doc else "")
    return cmd


def _drivable(callback: Callable[..., Any]) -> bool:
    """True when ``path`` is the only required parameter."""
    try:
        params = _inspect.signature(callback).parameters.values()
    except (TypeError, ValueError):
        return False
    for p in params:
        if p.name == "path":
            continue
        if p.default is _inspect.Parameter.empty and p.kind in (
            _inspect.Parameter.POSITIONAL_ONLY,
            _inspect.Parameter.POSITIONAL_OR_KEYWORD,
            _inspect.Parameter.KEYWORD_ONLY,
        ):
            return False
    return True


def _register_domain_aliases() -> int:
    """Alias every ``<group> inspect`` whose callback needs only ``path``."""
    count = 0
    for group in app.registered_groups:
        if group.name is None or group.typer_instance is None:
            continue
        if group.name in {"inspect", "project"}:
            continue
        for info in group.typer_instance.registered_commands:
            if info.name != "inspect" or info.callback is None:
                continue
            if _drivable(info.callback):
                inspect_app.command(group.name)(_alias(group.name, info.callback))
                count += 1
    return count


def register_domain_aliases() -> int:
    """Called by ``cli/__init__`` after every domain module is imported."""
    return _register_domain_aliases()
