"""Spec 268: real-OSS corpus provenance + precision/recall proof."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import golden_metrics  # noqa: E402

GOLDEN = ROOT / "golden"
METRICS = json.loads((GOLDEN / "metrics.json").read_text(encoding="utf-8"))
MANIFEST = json.loads((GOLDEN / "manifest.json").read_text(encoding="utf-8"))


def _real_entries() -> dict[str, dict[str, str]]:
    return {e["name"]: e for e in MANIFEST["entries"] if e["origin"] == "real"}


def test_corpus_contains_real_oss_slices() -> None:
    real = _real_entries()
    assert len(real) >= 3, "Phase D requires >=3 vendored real OSS slices"
    for name, entry in real.items():
        assert entry["url"].startswith("https://github.com/")
        assert len(entry["commit"]) == 40
        assert entry["license"]
        assert (GOLDEN / name / "repo" / "LICENSE").is_file(), f"{name}: no vendored LICENSE"


def test_metrics_file_covers_every_manifest_entry() -> None:
    assert set(METRICS["entries"]) == {e["name"] for e in MANIFEST["entries"]}


def test_metrics_perfect_against_ground_truth() -> None:
    """Recorded metrics must show P=R=1.0 - deterministic output vs truth."""
    for name, m in METRICS["entries"].items():
        assert m["precision"] == 1.0 and m["recall"] == 1.0, f"{name}: {m}"
    assert METRICS["aggregate"]["precision"] == 1.0
    assert METRICS["aggregate"]["recall"] == 1.0


def test_real_slices_scored_separately() -> None:
    real = METRICS["real_only"]
    assert real["entries"] == len(_real_entries())
    assert real["precision"] == 1.0 and real["recall"] == 1.0


def test_metrics_tool_recomputes_one_entry() -> None:
    """The tool isn't decorative: recomputing one real slice reproduces P=R=1."""
    name = sorted(_real_entries())[0]
    metrics = golden_metrics.collect_metrics(GOLDEN, name_filter=name)
    assert metrics["entries"][name]["precision"] == 1.0
    assert metrics["entries"][name]["recall"] == 1.0


def test_pr_helper_edge_cases() -> None:
    assert golden_metrics._pr(set(), set()) == {
        "tp": 0,
        "fp": 0,
        "fn": 0,
        "precision": 1.0,
        "recall": 1.0,
    }
    m = golden_metrics._pr({"a", "b"}, {"a", "c"})
    assert m == {"tp": 1, "fp": 1, "fn": 1, "precision": 0.5, "recall": 0.5}
