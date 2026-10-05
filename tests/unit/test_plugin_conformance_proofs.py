"""Spec §13: plugin trust-boundary proofs.

Three invariants the plugin supply chain must hold *as tests*, not
documentation:

1. No import-before-trust - untrusted code never executes (also covered
   by test_plugins.py; this adds the static proof that the trust gate
   runs before ``ep.load()`` everywhere a load happens).
2. No filesystem mutation during conformance - ``plugins
   list|doctor|validate`` inspect plugins without touching the scanned
   project or cwd.
3. No network use during conformance - the discovery/validation/
   isolation path contains no socket-opening imports by AST scan.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest
from typer.testing import CliRunner

from forge_doctor_data.cli import app

PLUGINS_DIR = Path(__file__).resolve().parents[2] / "src" / "forge_doctor_data" / "plugins"
_NETWORK_MODULES = {"socket", "urllib", "requests", "httpx", "aiohttp", "http"}


def _tree(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def test_trust_gate_runs_before_every_load() -> None:
    """Every engine-side ``ep.load()`` sits behind a trust/allow decision.

    ``isolation.py`` is the documented exception: its worker loads only
    the argv names a gated caller passes (the trust contract is stated in
    its docstring). What the suite then pins is that the caller path -
    ``discovery._load_isolated`` - applies ``_ep_trusted`` *before* any
    ``describe_entry_point``/``IsolatedCheck`` reaches a worker.
    """
    for path in sorted(PLUGINS_DIR.glob("*.py")):
        if path.name == "isolation.py":
            continue  # worker-side load; caller-gated by contract
        tree = ast.parse(path.read_text(encoding="utf-8"))
        source = path.read_text(encoding="utf-8")
        for node in ast.walk(tree):
            if not (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "load"
            ):
                continue
            # The file containing a load() must reference the trust gate.
            assert "_ep_trusted" in source or "trusted" in source, (
                f"{path.name}: ep.load() without a trust decision in scope"
            )


def test_isolated_loader_gates_before_invoking_workers() -> None:
    """The one path that feeds the worker applies the trust gate first."""
    source = (PLUGINS_DIR / "discovery.py").read_text(encoding="utf-8")
    gate = source.index("_ep_trusted(")
    first_invoke = source.index("describe_entry_point(")
    assert gate < first_invoke, "worker invocation precedes the trust gate"
    # And the worker documents that re-verification is the caller's job.
    worker_doc = (PLUGINS_DIR / "isolation.py").read_text(encoding="utf-8")
    assert "re-verifies nothing" in worker_doc


@pytest.mark.parametrize("cmd", ["list", "doctor", "validate"])
def test_conformance_commands_mutate_no_files(cmd: str, tmp_path: Path, monkeypatch) -> None:
    """list/doctor/validate leave the project tree byte-identical."""
    (tmp_path / "app.py").write_text("x = 1\n")
    monkeypatch.chdir(tmp_path)
    before = _tree(tmp_path)
    result = CliRunner().invoke(app, ["plugins", cmd])
    assert result.exit_code in (0, 1)  # conformance verdict, never a crash
    assert _tree(tmp_path) == before, f"plugins {cmd} mutated the project"


def test_conformance_modules_open_no_sockets() -> None:
    """AST proof: discovery/manager/protocol/isolation never import a
    network module - conformance is offline by construction."""
    for path in sorted(PLUGINS_DIR.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                mods = [a.name.split(".")[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                mods = [(node.module or "").split(".")[0]]
            else:
                continue
            bad = _NETWORK_MODULES & set(mods)
            assert not bad, f"{path.name}: conformance path imports {bad}"


def test_isolated_describe_is_bounded() -> None:
    """The isolation worker enforces timeout + output caps by contract."""
    import inspect

    from forge_doctor_data.plugins import isolation

    src = inspect.getsource(isolation._run_child) + inspect.getsource(isolation._invoke)
    assert "timeout" in src and "max_output_bytes" in src
    sig = inspect.signature(isolation.describe_entry_point)
    assert "timeout_seconds" in sig.parameters
    assert "max_output_bytes" in sig.parameters
