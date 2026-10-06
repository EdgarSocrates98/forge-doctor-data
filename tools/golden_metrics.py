"""Golden-corpus precision/recall report (spec 268, Phase D).

Runs the engine against every ``golden/<name>/repo`` and scores findings
against the recorded ground truth in ``expected/findings.json``:

- TP: expected finding rows the engine reproduces
- FP: finding rows the engine emits beyond the ground truth
- FN: ground-truth rows the engine no longer produces

For deterministically generated snapshots P=R=1.0 by construction -
the report is the artifact that *proves* it, split by origin so the
"I work on real repositories" claim reads straight off real OSS slices.

Usage::

    python tools/golden_metrics.py            # writes golden/metrics.json
    python tools/golden_metrics.py --check    # fail when metrics.json is stale
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from forge_doctor_data.core.context import ProjectContext, ScanOptions  # noqa: E402
from forge_doctor_data.core.golden import (  # noqa: E402
    _row_key,
    discover_golden,
    snapshot_findings,
)

GOLDEN = ROOT / "golden"
METRICS_PATH = GOLDEN / "metrics.json"


def _actual_findings(repo_dir: Path) -> list[dict[str, Any]]:
    from forge_doctor_data.checks import builtin_checks

    ctx = ProjectContext(root=repo_dir.resolve(), options=ScanOptions(hermetic=True))
    results = [r for check in builtin_checks() for r in check.run(ctx)]
    return snapshot_findings(results)


def _pr(expected: set[str], actual: set[str]) -> dict[str, Any]:
    tp = len(expected & actual)
    fp = len(actual - expected)
    fn = len(expected - actual)
    precision = tp / (tp + fp) if tp + fp else (1.0 if not expected else 0.0)
    recall = tp / (tp + fn) if tp + fn else (1.0 if not actual else 0.0)
    return {"tp": tp, "fp": fp, "fn": fn, "precision": precision, "recall": recall}


_REAL_ORIGINS = {"real", "real-oss"}


def collect_metrics(golden_root: Path = GOLDEN, name_filter: str | None = None) -> dict[str, Any]:
    manifest = json.loads((golden_root / "manifest.json").read_text(encoding="utf-8"))
    origins = {e["name"]: e["origin"] for e in manifest["entries"]}
    domains = {e["name"]: e.get("domain", []) for e in manifest["entries"]}
    entries: dict[str, Any] = {}
    for repo_dir in discover_golden(golden_root):
        name = repo_dir.parent.name
        if name_filter is not None and name != name_filter:
            continue
        expected_path = repo_dir.parent / "expected" / "findings.json"
        expected = {_row_key(r) for r in json.loads(expected_path.read_text("utf-8"))}
        actual = {_row_key(r) for r in _actual_findings(repo_dir)}
        entries[name] = {
            "origin": origins.get(name, "unknown"),
            "domain": domains.get(name, []),
            **_pr(expected, actual),
        }

    def aggregate(subset: dict[str, Any]) -> dict[str, Any]:
        tp = sum(v["tp"] for v in subset.values())
        fp = sum(v["fp"] for v in subset.values())
        fn = sum(v["fn"] for v in subset.values())
        return {
            "entries": len(subset),
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "precision": tp / (tp + fp) if tp + fp else 1.0,
            "recall": tp / (tp + fn) if tp + fn else 1.0,
        }

    real = {k: v for k, v in entries.items() if v["origin"] in _REAL_ORIGINS}
    synthetic = {k: v for k, v in entries.items() if v["origin"] == "synthetic"}
    by_domain = {
        d: aggregate({k: v for k, v in entries.items() if d in v["domain"]})
        for d in sorted({d for v in entries.values() for d in v["domain"]})
    }
    return {
        "schema_version": "1",
        "metric": "finding-level precision/recall vs recorded ground truth",
        "entries": dict(sorted(entries.items())),
        "total_entries": len(entries),
        "passed_entries": sum(
            1 for v in entries.values() if v["precision"] == 1.0 and v["recall"] == 1.0
        ),
        "failed_entries": sum(
            1 for v in entries.values() if v["precision"] < 1.0 or v["recall"] < 1.0
        ),
        "aggregate": aggregate(entries),
        "real_only": aggregate(real),
        "synthetic_only": aggregate(synthetic),
        "by_domain": by_domain,
        "precision_by_domain": {d: m["precision"] for d, m in by_domain.items()},
        "recall_by_domain": {d: m["recall"] for d, m in by_domain.items()},
    }


def main(argv: list[str]) -> int:
    metrics = collect_metrics()
    rendered = json.dumps(metrics, indent=2, sort_keys=True) + "\n"
    if "--check" in argv:
        current = METRICS_PATH.read_text("utf-8") if METRICS_PATH.is_file() else ""
        if current != rendered:
            print("golden/metrics.json is stale - regenerate with tools/golden_metrics.py")
            return 1
        print("golden/metrics.json up to date")
        return 0
    METRICS_PATH.write_text(rendered, encoding="utf-8")
    real = metrics["real_only"]
    agg = metrics["aggregate"]
    print(
        f"corpus: {agg['entries']} entries "
        f"(P={agg['precision']:.3f} R={agg['recall']:.3f}) | "
        f"real: {real['entries']} entries "
        f"(P={real['precision']:.3f} R={real['recall']:.3f})"
    )
    print(f"wrote {METRICS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
