"""Spec-257 fleet benchmark: generator determinism + small-N smoke."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_FLEET = Path(__file__).resolve().parents[2] / "tools" / "benchmarks" / "fleet.py"
_spec = importlib.util.spec_from_file_location("fleet_bench", _FLEET)
assert _spec is not None and _spec.loader is not None
fleet = importlib.util.module_from_spec(_spec)
sys.modules.setdefault("fleet_bench", fleet)
_spec.loader.exec_module(fleet)


def _tree(root: Path) -> dict[str, str]:
    return {p.relative_to(root).as_posix(): p.read_text() for p in root.rglob("*") if p.is_file()}


def test_generator_deterministic(tmp_path: Path) -> None:
    a = _tree(fleet.generate_workspace(tmp_path / "a", 5, seed=42)[0].parent)
    b = _tree(fleet.generate_workspace(tmp_path / "b", 5, seed=42)[0].parent)
    assert a == b


def test_generator_seed_changes_corpus(tmp_path: Path) -> None:
    a = _tree(fleet.generate_workspace(tmp_path / "a", 5, seed=1)[0].parent)
    b = _tree(fleet.generate_workspace(tmp_path / "b", 5, seed=2)[0].parent)
    assert a != b


def test_measure_small_workspace(tmp_path: Path) -> None:
    result = fleet.measure_size(tmp_path, 2, seed=42)
    assert result.repos == 2
    assert result.files == 6
    assert result.cold_ms_mean > 0
