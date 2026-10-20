"""Resolver coverage: packaged fallbacks and write guards (cycle 12)."""

from __future__ import annotations

import sysconfig
from pathlib import Path

import pytest
import typer
from typer.testing import CliRunner

from forge_doctor_data.cli.common import _packaged_dir
from forge_doctor_data.cli.golden import GOLDEN_ROOT, _golden_root
from forge_doctor_data.cli.lab import _default_labs
from forge_doctor_data.cli.misc import knowledge_app

runner = CliRunner()


def test_packaged_dir_returns_real_path() -> None:
    golden = _packaged_dir("_data/golden")
    if not golden.is_dir():  # editable checkout sem _data materializado
        pytest.skip("packaged _data ausente neste ambiente")
    assert isinstance(golden, Path)
    assert str(golden).endswith(("_data/golden", "_data\\golden"))


def test_golden_root_explicit_wins(tmp_path: Path) -> None:
    assert _golden_root(tmp_path) == tmp_path
    existing = tmp_path / "g"
    existing.mkdir()
    assert _golden_root(existing) == existing


def test_golden_root_default_falls_back_to_packaged(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)  # cwd sem golden/
    packaged = _packaged_dir("_data/golden")
    if not packaged.is_dir():
        pytest.skip("packaged _data ausente neste ambiente")
    assert _golden_root(Path(GOLDEN_ROOT)) == packaged


def test_golden_root_for_write_refuses_packaged(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    packaged = _packaged_dir("_data/golden")
    if not packaged.is_dir():
        pytest.skip("packaged _data ausente neste ambiente")
    with pytest.raises(typer.Exit) as exc:
        _golden_root(Path(GOLDEN_ROOT), for_write=True)
    assert exc.value.exit_code == 2


def test_default_labs_prefers_cwd(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "labs").mkdir()
    monkeypatch.chdir(tmp_path)
    assert _default_labs() == tmp_path / "labs"


def test_default_labs_packaged_fallback(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    packaged = _packaged_dir("_data/labs")
    expected = packaged if packaged.is_dir() else tmp_path / "labs"
    assert _default_labs() == expected


def test_knowledge_new_refuses_purelib_write(monkeypatch) -> None:
    purelib = Path(sysconfig.get_paths()["purelib"])
    fake = purelib / "forge_doctor_data" / "knowledge"
    monkeypatch.setattr(
        "forge_doctor_data.cli.misc._bundled_knowledge_root", lambda: fake
    )
    result = runner.invoke(knowledge_app, ["new", "snowflake"])
    assert result.exit_code == 2
    assert "refuse to write" in (result.output + getattr(result, "stderr", ""))


def test_knowledge_new_refuses_non_fs_traversable(tmp_path: Path, monkeypatch) -> None:
    class _FakeTrav:
        def __truediv__(self, part: str):
            return self

    monkeypatch.setattr("importlib.resources.files", lambda pkg: _FakeTrav())
    monkeypatch.setattr(
        "forge_doctor_data.cli.misc._bundled_knowledge_root",
        lambda: tmp_path / "knowledge",
    )
    result = runner.invoke(knowledge_app, ["new", "snowflake"])
    assert result.exit_code == 2
    assert "refuse to write" in (result.output + getattr(result, "stderr", ""))


def test_knowledge_new_explicit_dir_writes(tmp_path: Path) -> None:
    result = runner.invoke(
        knowledge_app, ["new", "snowflake", "--dir", str(tmp_path / "kn")]
    )
    assert result.exit_code == 0


def test_knowledge_new_refuses_when_resolve_fails(monkeypatch, capsys):
    """resolve() que falha nao prova fora-do-site-packages: recusa, nao escreve."""
    from forge_doctor_data.cli.misc import knowledge_new
    import typer

    monkeypatch.setattr(Path, "resolve", lambda self, *a, **k: (_ for _ in ()).throw(
        RuntimeError("symlink loop")
    ))
    with pytest.raises(typer.Exit) as exc:
        knowledge_new("snowflake")
    assert exc.value.exit_code == 2
