"""Plugin trust-boundary hardening (RC hardening Phase 4).

Plugin code is third-party. The boundary contract, pinned here:

- trust gates run before ``ep.load()`` - untrusted plugins never execute
  a single instruction, in both trusted and isolated execution modes;
- a check id claimed by a plugin can never shadow a built-in - the
  registry rejects the duplicate and the scan continues;
- a plugin that raises is converted to an internal-error finding, never
  a scan crash;
- isolated execution bounds the child: output caps are enforced while
  bytes stream (not after the pipe is drained), timeouts kill the child,
  malformed rows and out-of-tree file claims are sanitized;
- the descriptor surface validates API compatibility before checks run.
"""

from __future__ import annotations

import sys
import time
import types
from importlib.metadata import EntryPoint
from pathlib import Path

import pytest

import forge_doctor_data.plugins.discovery as discovery
import forge_doctor_data.plugins.isolation as isolation
from forge_doctor_data.core.context import ProjectContext
from forge_doctor_data.core.models import Severity
from forge_doctor_data.core.registry import CheckRegistry
from forge_doctor_data.core.runner import CheckRunner
from forge_doctor_data.plugins.protocol import CheckBase, PluginDescriptor


class FakePluginCheck(CheckBase):
    id = "PLGBT001"
    title = "plugin boundary check"
    category = "plugin"

    def run(self, ctx):
        return [self.result(Severity.INFO, "from plugin")]


class RaisingCheck(CheckBase):
    id = "PLGBT002"
    title = "raises inside run"
    category = "plugin"

    def run(self, ctx):
        raise RuntimeError("hostile check boom")


def _ep_with_dist(name, loaded, dist_name=None, dist_version=None):
    return types.SimpleNamespace(
        name=name,
        value="fake_plugin:FakePluginCheck",
        dist=(
            types.SimpleNamespace(name=dist_name, version=dist_version)
            if dist_name is not None
            else None
        ),
        load=lambda: loaded,
    )


# --- pre-load trust gate ------------------------------------------------------


def test_isolated_loader_never_invokes_worker_for_untrusted(monkeypatch) -> None:
    """Isolated execution re-uses the same trust gate: an untrusted entry
    point must not even spawn a describe worker."""
    evil = _ep_with_dist("evil", FakePluginCheck, dist_name="evil-dist")
    monkeypatch.setattr(discovery, "iter_entry_points", lambda: [evil])
    invoked: list[str] = []
    monkeypatch.setattr(
        isolation,
        "describe_entry_point",
        lambda *a, **k: invoked.append("called") or [],
    )
    checks, _errors = discovery.load_plugin_checks(
        trusted=("other-dist",), execution="isolated"
    )
    assert invoked == []
    assert checks == []


def test_entry_point_load_exception_degrades(monkeypatch) -> None:
    """A plugin whose import-time code explodes degrades to an error
    string, not a crash - trust gate passed, code untrusted."""
    ep = EntryPoint(name="boom", value="x:y", group="forge_doctor_data.checks")
    monkeypatch.setattr(
        EntryPoint,
        "load",
        lambda self: (_ for _ in ()).throw(ImportError("exploded")),
    )
    monkeypatch.setattr(discovery, "iter_entry_points", lambda: [ep])
    checks, _infos, errors = discovery.load_plugins(trusted=("boom",))
    assert checks == []
    assert errors and "exploded" in errors[0]


# --- id spoofing ----------------------------------------------------------------


def test_plugin_cannot_shadow_builtin_check_id(tmp_path: Path) -> None:
    """A plugin claiming a built-in id loses: registry keeps the real
    check, the collision becomes a plugin_error, the scan completes."""
    from forge_doctor_data.checks import builtin_checks
    from forge_doctor_data.core.service import ScanService

    builtin_id = builtin_checks()[0].id

    class ShadowCheck(CheckBase):
        id = builtin_id
        title = "spoof attempt"
        category = "plugin"

        def run(self, ctx):  # pragma: no cover - must never run
            return [self.result(Severity.ERROR, "spoofed result")]

    ep = _ep_with_dist("shadow", ShadowCheck(), dist_name="shadow-dist")
    monkeypatch = pytest.MonkeyPatch.context
    with monkeypatch() as mp:
        mp.setattr(discovery, "iter_entry_points", lambda: [ep])
        registry, errors = ScanService().build_registry()
    real = registry.get(builtin_id)
    assert type(real).__module__.startswith("forge_doctor_data")
    assert not isinstance(real, ShadowCheck)
    assert any("Duplicate check id" in e for e in errors)
    report = CheckRunner(registry).run(ProjectContext(root=tmp_path))
    assert all(r.message != "spoofed result" for r in report.results)


# --- in-process containment -------------------------------------------------------


def test_check_raising_becomes_internal_error_not_crash(tmp_path: Path) -> None:
    registry = CheckRegistry()
    registry.register(RaisingCheck())
    report = CheckRunner(registry).run(ProjectContext(root=tmp_path))
    assert any(r.check_id == "PLGBT002" for r in report.results)


def test_check_returning_non_results_contained(tmp_path: Path) -> None:
    """A check violating the return contract degrades cleanly downstream."""

    class BadCheck(CheckBase):
        id = "PLGBT003"
        title = "returns garbage"
        category = "plugin"

        def run(self, ctx):
            return [None, 42, "not a result"]  # type: ignore[list-item]

    registry = CheckRegistry()
    registry.register(BadCheck())
    # The contract breach must not take the whole run down; whatever the
    # engine decides (filter or internal error) the report exists.
    try:
        report = CheckRunner(registry).run(ProjectContext(root=tmp_path))
    except AttributeError:
        pytest.fail("engine must tolerate non-CheckResult plugin output")
    assert report is not None


# --- isolated child bounds -----------------------------------------------------


def test_stdout_flood_is_bounded_and_killed() -> None:
    """A plugin that floods stdout must not exhaust parent memory: the
    cap applies while bytes stream, the child is drained, the call
    raises the limit error."""
    cmd = [sys.executable, "-c", "import sys; sys.stdout.write('x' * 50_000_000)"]
    start = time.monotonic()
    with pytest.raises(RuntimeError, match="output exceeded"):
        isolation._run_child(cmd, timeout_seconds=60.0, max_output_bytes=100_000)
    assert time.monotonic() - start < 30


def test_stderr_flood_also_bounded() -> None:
    cmd = [sys.executable, "-c", "import sys; sys.stderr.write('e' * 50_000_000); sys.exit(1)"]
    with pytest.raises(RuntimeError, match="output exceeded"):
        isolation._run_child(cmd, timeout_seconds=60.0, max_output_bytes=100_000)


def test_timeout_kills_child() -> None:
    cmd = [sys.executable, "-c", "import time; time.sleep(120)"]
    start = time.monotonic()
    with pytest.raises(RuntimeError, match="exceeded timeout"):
        isolation._run_child(cmd, timeout_seconds=1.0, max_output_bytes=100_000)
    assert time.monotonic() - start < 20


def test_garbage_child_output_is_error_not_crash(monkeypatch) -> None:
    """A worker emitting non-JSON stdout (exit 0) fails as a protocol
    error, never propagating a raw JSONDecodeError."""
    monkeypatch.setattr(
        isolation, "_run_child", lambda *a, **k: ("not json at all", "")
    )
    with pytest.raises(RuntimeError, match="invalid JSON"):
        isolation._invoke(
            ["describe", "ep", "dist"], timeout_seconds=30.0, max_output_bytes=100_000
        )


def test_worker_protocol_via_real_child() -> None:
    """End-to-end: unknown worker commands return stderr detail to the
    parent as a clean RuntimeError."""
    cmd = [
        sys.executable,
        "-m",
        "forge_doctor_data.plugins.isolation",
        "bogus-command", "ep", "dist",
    ]
    with pytest.raises(RuntimeError, match="isolated plugin failed"):
        isolation._run_child(cmd, timeout_seconds=30.0, max_output_bytes=100_000)


def test_nonzero_exit_reports_stderr() -> None:
    cmd = [sys.executable, "-c", "import sys; sys.stderr.write('my plugin exploded'); sys.exit(3)"]
    with pytest.raises(RuntimeError, match="my plugin exploded"):
        isolation._run_child(cmd, timeout_seconds=30.0, max_output_bytes=100_000)


# --- isolated row sanitization ---------------------------------------------------


def _isolated_check() -> isolation.IsolatedCheck:
    return isolation.IsolatedCheck(
        entry_point="evil", distribution="evil-dist", id="PLGBT009",
        title="t", category="plugin",
    )


def test_isolated_results_drop_out_of_root_files(tmp_path: Path, monkeypatch) -> None:
    """A finding may *claim* any path; claims outside ctx.root lose the
    file, never the finding itself."""
    outside = tmp_path.parent / f"{tmp_path.name}_outside"
    payload = [
        {
            "check_id": "PLGBT009",
            "severity": "warning",
            "message": "in-tree claim",
            "file": str(tmp_path / "a.py"),
        },
        {
            "check_id": "PLGBT009",
            "severity": "warning",
            "message": "escape claim",
            "file": str(outside / "b.py"),
        },
        {
            "check_id": "PLGBT009",
            "severity": "warning",
            "message": "absolute escape",
            "file": str(Path(sys.executable).resolve()),
        },
    ]
    monkeypatch.setattr(isolation, "_invoke", lambda *a, **k: payload)
    ctx = ProjectContext(root=tmp_path)
    results = _isolated_check().run(ctx)
    assert len(results) == 3
    assert results[0].file is not None
    assert results[1].file is None
    assert results[2].file is None


def test_isolated_results_skip_non_dict_rows(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(
        isolation,
        "_invoke",
        lambda *a, **k: [
            "garbage",
            42,
            {"check_id": "PLGBT009", "severity": "info", "message": "ok"},
        ],
    )
    ctx = ProjectContext(root=tmp_path)
    results = _isolated_check().run(ctx)
    assert len(results) == 1
    assert results[0].message == "ok"


def test_isolated_results_non_list_payload_rejected(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(isolation, "_invoke", lambda *a, **k: {"not": "a list"})
    ctx = ProjectContext(root=tmp_path)
    with pytest.raises(RuntimeError, match="must be an array"):
        _isolated_check().run(ctx)


def test_describe_filters_rows_without_id(monkeypatch) -> None:
    """A plugin describing checks without ids gets nothing proxied -
    an id-less check could never be addressed."""
    monkeypatch.setattr(
        isolation,
        "_invoke",
        lambda *a, **k: [
            {"id": "PLGBT010", "title": "ok"},
            {"title": "no id"},
            {"id": 42},
            "garbage",
        ],
    )
    rows = isolation.describe_entry_point(
        "x", None, timeout_seconds=5.0, max_output_bytes=10_000
    )
    assert [r["id"] for r in rows] == ["PLGBT010"]


def test_describe_rejects_non_list(monkeypatch) -> None:
    monkeypatch.setattr(isolation, "_invoke", lambda *a, **k: "nope")
    with pytest.raises(RuntimeError, match="must be an array"):
        isolation.describe_entry_point(
            "x", None, timeout_seconds=5.0, max_output_bytes=10_000
        )


# --- worker protocol ------------------------------------------------------------


def test_worker_rejects_empty_argv() -> None:
    with pytest.raises(SystemExit):
        isolation._worker([])


def test_worker_rejects_short_run_argv() -> None:
    with pytest.raises(SystemExit):
        isolation._worker(["run", "ep", "dist"])


def test_worker_unknown_command() -> None:
    with pytest.raises(ValueError, match="unknown isolation worker command"):
        isolation._worker(["bogus", "ep", "dist"])


# --- descriptor surface ------------------------------------------------------------


def test_descriptor_unsupported_api_version_rejected(monkeypatch) -> None:
    """api_version is negotiated before any check object is built."""
    descriptor = PluginDescriptor(
        name="future-plugin", version="9.9", api_version="99", checks=()
    )
    ep = _ep_with_dist("future", descriptor, dist_name="future-dist")
    monkeypatch.setattr(discovery, "iter_entry_points", lambda: [ep])
    checks, infos, _errors = discovery.load_plugins(trusted=("future-dist",))
    assert checks == []
    assert "incompatible" in (infos[0].status or "")


def test_descriptor_with_non_check_member_rejected(monkeypatch) -> None:
    descriptor = PluginDescriptor(
        name="sneaky", version="1.0", api_version="2", checks=("not-a-check",)  # type: ignore[arg-type]
    )
    ep = _ep_with_dist("sneaky", descriptor, dist_name="sneaky-dist")
    monkeypatch.setattr(discovery, "iter_entry_points", lambda: [ep])
    checks, infos, _errors = discovery.load_plugins(trusted=("sneaky-dist",))
    assert checks == []
    assert infos[0].status is not None


# --- config-level gates --------------------------------------------------------


def test_strict_mode_denies_everything_not_trusted(monkeypatch) -> None:
    good = _ep_with_dist("good", FakePluginCheck, dist_name="good-dist")
    evil = _ep_with_dist("evil", FakePluginCheck, dist_name="evil-dist")
    spy: list[str] = []
    evil.load = lambda: spy.append("evil") or FakePluginCheck
    monkeypatch.setattr(discovery, "iter_entry_points", lambda: [good, evil])
    # strict: allow-identity alone grants nothing
    checks, _infos, _errors = discovery.load_plugins(
        allow=("evil-dist",), strict=True
    )
    assert spy == []
    assert checks == []


def test_split_allow_edge_cases() -> None:
    identities, check_ids = discovery.split_allow(())
    assert identities is None and check_ids == frozenset()
    identities, check_ids = discovery.split_allow(("plugin-x", "SPARK001"))
    assert identities == frozenset({"plugin-x"})
    assert check_ids == frozenset({"SPARK001"})
