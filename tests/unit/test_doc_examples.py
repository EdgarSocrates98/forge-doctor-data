"""Documentation-as-contract gate (spec 265, section 13).

If a documented `forge-doctor-data ...` invocation stops resolving against
the real CLI - renamed command, dropped subcommand, removed flag - this
suite fails. The docs are executable promises, not prose.

Also pins `tools/<name>.py` references: a release/example doc pointing at a
script that no longer exists fails the gate.
"""

from __future__ import annotations

import re
from pathlib import Path

import typer.main

from forge_doctor_data.cli import app

ROOT = Path(__file__).resolve().parents[2]
DOCS = [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]

_COMMAND_LINE = re.compile(r"^(?:\$\s*)?forge-doctor-data\s+(.+?)\s*$")
_TOOL_REF = re.compile(r"`?(tools/[\w.-]+\.py)`?")
_ENV_ASSIGN = re.compile(r"^[A-Z_][A-Z0-9_]*=")

_COMMAND_TREE = typer.main.get_command(app)


def _is_group(cmd: object) -> bool:
    return isinstance(getattr(cmd, "commands", None), dict)


def _cli_invocations() -> list[tuple[str, int, list[str]]]:
    out: list[tuple[str, int, list[str]]] = []
    for doc in DOCS:
        in_fence = False
        for lineno, line in enumerate(doc.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            m = _COMMAND_LINE.match(line) if in_fence else None
            if not m:
                continue
            raw = m.group(1).split()
            if "#" in raw:  # inline comment tail is not argv
                raw = raw[: raw.index("#")]
            tokens = [t for t in raw if not _ENV_ASSIGN.match(t)]
            out.append((f"{doc.relative_to(ROOT)}:{lineno}", lineno, tokens))
    return out


def _resolve(tokens: list[str]):
    """Walk the click tree. Returns (deepest command, remaining argv)."""
    cmd = _COMMAND_TREE
    rest = list(tokens)
    while _is_group(cmd) and rest:
        nxt = cmd.commands.get(rest[0])
        if nxt is None:
            break
        cmd, rest = nxt, rest[1:]
    return cmd, rest


def _option_names(cmd) -> set[str]:
    names: set[str] = set()
    for p in cmd.params:
        opts = getattr(p, "opts", None)
        if opts:
            names.update(opts)
            names.update(getattr(p, "secondary_opts", ()))
    if _has_custom_dispatch(cmd):
        for sub in cmd.commands.values():
            names.update(_option_names(sub))
    return names


def _has_custom_dispatch(cmd) -> bool:
    """Groups like `_GraphGroup` override resolve_command to alias argv to a
    default subcommand (`graph --format x` -> `graph project --format x`)."""
    return _is_group(cmd) and type(cmd).resolve_command is not type(_COMMAND_TREE).resolve_command


def test_every_documented_command_resolves() -> None:
    failures = []
    for where, _, tokens in _cli_invocations():
        if not tokens:
            continue
        first = tokens[0]
        if first not in _COMMAND_TREE.commands:
            failures.append(f"{where}: unknown command '{first}'")
            continue
        cmd, rest = _resolve(tokens)
        # A group that can't run bare needs a real subcommand next, unless
        # its class overrides dispatch to alias argv to a default subcommand.
        if (
            _is_group(cmd)
            and not getattr(cmd, "invoke_without_command", False)
            and not _has_custom_dispatch(cmd)
        ):
            failures.append(f"{where}: group '{first}' without valid subcommand ({rest[:1]})")
    assert failures == []


def test_every_documented_flag_exists() -> None:
    failures = []
    for where, _, tokens in _cli_invocations():
        cmd, rest = _resolve(tokens)
        opts = _option_names(cmd)
        for tok in rest:
            if tok.startswith("--"):
                flag = tok.split("=")[0]
                if flag not in opts:
                    failures.append(f"{where}: '{flag}' not an option of '{cmd.name}'")
    assert failures == []


def test_tool_references_exist() -> None:
    missing = [
        f"{doc.relative_to(ROOT)}: {ref}"
        for doc in DOCS
        for ref in _TOOL_REF.findall(doc.read_text(encoding="utf-8"))
        if not (ROOT / ref).exists()
    ]
    assert missing == []
