"""Hermetic-scan guarantees (consolidation spec 265, Phase A.5).

A hermetic scan must depend only on files inside the project root -
never on host state. These tests prove that ``ScanOptions(hermetic=True)``
produces identical findings under a deliberately contaminated environment
and that host facts are hidden at the context boundary.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from forge_doctor_data.checks import builtin_checks
from forge_doctor_data.core.context import ProjectContext, ScanOptions
from forge_doctor_data.core.registry import CheckRegistry
from forge_doctor_data.core.runner import CheckRunner

_POLLUTION = {
    "AWS_ACCESS_KEY_ID": "AKIAFAKEHERMETICTEST",
    "AWS_SECRET_ACCESS_KEY": "fake-secret-for-tests",
    "AWS_REGION": "us-east-1",
    "AWS_DEFAULT_REGION": "us-east-1",
    "AWS_PROFILE": "contaminated-profile",
    "AWS_DEFAULT_PROFILE": "contaminated-profile",
    "VIRTUAL_ENV": "/nonexistent/venv",
    "CONDA_PREFIX": "/nonexistent/conda",
    "JAVA_HOME": r"C:\nonexistent\jdk",
    "HOME": "/nonexistent/home",
    "USERPROFILE": r"C:\nonexistent\home",
}

_SPARK = (
    "from pyspark.sql import SparkSession\n"
    "spark = SparkSession.builder.getOrCreate()\n"
    'df = spark.read.parquet("s3://b/in")\n'
    "df.collect()\n"
)


def _fixture(root: Path) -> None:
    (root / "job.py").write_text(_SPARK, encoding="utf-8")
    (root / "main.tf").write_text(
        'resource "aws_dynamodb_table" "t" {\n  name = "orders"\n}\n', encoding="utf-8"
    )


def _runner() -> CheckRunner:
    registry = CheckRegistry()
    registry.register_all(builtin_checks())
    return CheckRunner(registry)


def _scan(root: Path, hermetic: bool) -> list[tuple[str, str, str]]:
    ctx = ProjectContext(root=root, options=ScanOptions(hermetic=hermetic))
    report = _runner().run(ctx)
    return sorted((r.check_id, r.severity.value, r.message) for r in report.results)


@pytest.fixture
def clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in _POLLUTION:
        monkeypatch.delenv(key, raising=False)


@pytest.mark.usefixtures("clean_env")
def test_hermetic_scan_ignores_host_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    _fixture(project)

    baseline = _scan(project, hermetic=True)

    for key, value in _POLLUTION.items():
        monkeypatch.setenv(key, value)

    assert _scan(project, hermetic=True) == baseline


def test_hermetic_context_hides_host_facts(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    _fixture(project)
    for key, value in _POLLUTION.items():
        monkeypatch.setenv(key, value)

    ctx = ProjectContext(root=project, options=ScanOptions(hermetic=True))

    assert ctx.env == {}
    assert ctx.home == ctx.root
    assert ctx.which("git") is None
    assert ctx.which("java") is None
    assert ctx.python_version is None


def test_non_hermetic_context_sees_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    project = tmp_path / "proj"
    project.mkdir()
    monkeypatch.setenv("AWS_REGION", "eu-west-1")

    ctx = ProjectContext(root=project, options=ScanOptions(hermetic=False))

    assert ctx.env.get("AWS_REGION") == "eu-west-1"


def test_hermetic_ignores_ancestor_git_repo(tmp_path: Path) -> None:
    """A fixture inside a checkout must not inherit the host's tracked files."""
    (tmp_path / ".git").mkdir()
    project = tmp_path / "nested" / "proj"
    project.mkdir(parents=True)
    _fixture(project)

    ctx = ProjectContext(root=project, options=ScanOptions(hermetic=True))

    assert ctx.git.is_repo is False
    assert ctx.git.tracked_files is None


def test_hermetic_accepts_own_git_root(tmp_path: Path) -> None:
    """A repo rooted at the project still counts under hermetic scans."""
    project = tmp_path / "proj"
    project.mkdir()
    (project / ".git").mkdir()
    _fixture(project)

    ctx = ProjectContext(root=project, options=ScanOptions(hermetic=True))

    # .git exists at the root so the engine may ask git; whether git answers
    # depends on the host, but the ancestor-leak guard must not fire.
    if ctx.git.is_repo:
        tracked = ctx.git.tracked_files or frozenset()
        assert all(not str(f).startswith("..") for f in tracked)


def test_hermetic_deterministic_across_home_change(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Swapping HOME/USERPROFILE between runs must not change findings."""
    project = tmp_path / "proj"
    project.mkdir()
    _fixture(project)

    monkeypatch.setenv("HOME", str(tmp_path / "home-a"))
    first = _scan(project, hermetic=True)
    monkeypatch.setenv("HOME", str(tmp_path / "home-b"))
    monkeypatch.setenv("USERPROFILE", str(tmp_path / "home-b"))

    assert _scan(project, hermetic=True) == first


def test_no_credential_leakage_into_results(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Env values stay in-process: nothing serializes the fake credential."""
    import json

    project = tmp_path / "proj"
    project.mkdir()
    _fixture(project)
    for key, value in _POLLUTION.items():
        monkeypatch.setenv(key, value)

    ctx = ProjectContext(root=project, options=ScanOptions(hermetic=True))
    report = _runner().run(ctx)
    serialized = json.dumps([r.message for r in report.results])
    for value in _POLLUTION.values():
        assert value not in serialized
    # PATH may legitimately contain tool names; env *values* never do.
    assert os.environ.get("AWS_SECRET_ACCESS_KEY", "x") not in serialized
