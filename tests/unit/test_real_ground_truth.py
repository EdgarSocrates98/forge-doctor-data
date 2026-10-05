"""Real-OSS ground truth: human-declared expectations for every vendored
slice. Where ground_truth.json declares expected findings/entities/edges,
the engine must produce them; where it declares forbidden cross-domain
findings or honest unknowns, the engine must stay silent.

These run the engine live (not just the recorded snapshot) so a future
regression in detection cannot hide behind a stale snapshot.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

import golden_metrics  # noqa: E402

GOLDEN = ROOT / "golden"
MANIFEST = json.loads((GOLDEN / "manifest.json").read_text(encoding="utf-8"))

_REAL = [
    e["name"]
    for e in MANIFEST["entries"]
    if e["origin"] in {"real", "real-oss"}
]


def _prefixes(rows: list[dict]) -> set[str]:
    return {r["check_id"].rstrip("0123456789") for r in rows}


@pytest.mark.parametrize("entry", _REAL)
def test_expected_findings_present(entry: str) -> None:
    """Declared check families must each produce >=1 finding."""
    gt = json.loads((GOLDEN / entry / "ground_truth.json").read_text(encoding="utf-8"))
    actual = golden_metrics._actual_findings(GOLDEN / entry / "repo")
    actual_prefixes = _prefixes(actual)
    actual_ids = {r["check_id"] for r in actual}
    for prefix in gt["expected_findings"]["check_id_prefixes"]:
        assert prefix in actual_prefixes, (
            f"{entry}: expected {prefix}* findings, got {sorted(actual_ids)}"
        )
    for check_id in gt["expected_findings"]["check_ids"]:
        assert check_id in actual_ids, f"{entry}: expected {check_id}"


@pytest.mark.parametrize("entry", _REAL)
def test_forbidden_findings_absent(entry: str) -> None:
    """Cross-domain leakage: declared-forbidden families must stay silent."""
    gt = json.loads((GOLDEN / entry / "ground_truth.json").read_text(encoding="utf-8"))
    actual = golden_metrics._actual_findings(GOLDEN / entry / "repo")
    actual_prefixes = _prefixes(actual)
    actual_ids = {r["check_id"] for r in actual}
    for prefix in gt["forbidden_findings"]["check_id_prefixes"]:
        assert prefix not in actual_prefixes, (
            f"{entry}: forbidden family {prefix}* emitted findings - "
            "cross-domain false positive"
        )
    for check_id in gt["forbidden_findings"]["check_ids"]:
        assert check_id not in actual_ids, (
            f"{entry}: forbidden check {check_id} fired"
        )


@pytest.mark.parametrize("entry", _REAL)
def test_expected_unknowns_silent(entry: str) -> None:
    """Declared unknowns are claims the evidence cannot support; the
    engine's honest output is silence."""
    gt = json.loads((GOLDEN / entry / "ground_truth.json").read_text(encoding="utf-8"))
    actual_ids = {
        r["check_id"] for r in golden_metrics._actual_findings(GOLDEN / entry / "repo")
    }
    for decl in gt["expected_unknowns"]:
        assert decl["check_id"] not in actual_ids, (
            f"{entry}: {decl['check_id']} fired but truth declares it "
            f"unprovable ({decl['reason']})"
        )


@pytest.mark.parametrize("entry", _REAL)
def test_expected_entities_and_edges(entry: str) -> None:
    """Declared graph domains/kinds/relationships must appear in the
    recorded graph snapshot (entities may legitimately be empty, e.g.
    client-only Kafka evidence)."""
    gt = json.loads((GOLDEN / entry / "ground_truth.json").read_text(encoding="utf-8"))
    graph = json.loads(
        (GOLDEN / entry / "expected" / "graph.json").read_text(encoding="utf-8")
    )
    domains = {n.get("domain") for n in graph["entities"]}
    kinds = {n.get("kind") for n in graph["entities"]}
    rels = {e.get("kind") for e in graph["relationships"]}
    for d in gt["expected_entities"]["domains"]:
        assert d in domains, f"{entry}: expected entity domain {d}"
    for k in gt["expected_entities"]["kinds"]:
        assert k in kinds, f"{entry}: expected entity kind {k}"
    for r in gt["expected_edges"]["kinds"]:
        assert r in rels, f"{entry}: expected edge kind {r}"
