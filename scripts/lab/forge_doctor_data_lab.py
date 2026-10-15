#!/usr/bin/env python3
"""Forge Lab emitter — runs the repo's real lab engine (core.lab.run_lab)
over labs/ ground-truth scenarios and emits forge/BenchmarkResult/v1.

Deterministic, offline, stdlib-only. Unsupported/unmeasurable metrics are
reported as explicit states, never zero.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

FORGE = "forge-doctor-data"
SUITE = "forge-doctor-data-lab"


import re as _re

def _slug(s: object) -> str:
    return _re.sub(r"[^a-z0-9-]+", "-", str(s).lower()).strip("-") or "scenario"


def m(state: str, value: object = None, unit: str = "") -> dict:
    return {"state": state, "unit": unit, "value": value}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkout", required=True)
    ap.add_argument("--mode", default="A", choices=["A", "B", "C"])
    ap.add_argument("--result-out", required=True)
    a = ap.parse_args()
    checkout = Path(a.checkout).resolve()
    sys.path.insert(0, str(checkout / "src"))

    from forge_doctor_data.core.lab import run_lab

    started = time.monotonic()
    report = run_lab(checkout / "labs", None)
    elapsed = int((time.monotonic() - started) * 1000)

    results = []
    for r in report.reports:
        cats = dict(getattr(r, "categories", {}) or {})
        expected = sum(len(getattr(c, "expected", ())) for c in cats.values())
        actual = sum(len(getattr(c, "actual", ())) for c in cats.values())
        missed = sum(len(getattr(c, "missed", ())) for c in cats.values())
        forbidden = sum(len(getattr(c, "forbidden_hit", ())) for c in cats.values())
        extra = sum(len(getattr(c, "extra", ())) for c in cats.values())
        matched = max(expected - missed, 0)
        precision = (matched / actual) if actual else (1.0 if expected == 0 else None)
        recall = (matched / expected) if expected else None
        metrics = {
            "success": m("measured", 1.0 if r.passed else 0.0, "ratio"),
            "precision": m("measured", precision, "ratio")
            if precision is not None
            else m("not_available"),
            "recall": m("measured", recall, "ratio")
            if recall is not None
            else m("not_available"),
            "false_positives": m("measured", forbidden + extra),
            "cost_usd": m("not_applicable"),
            "tokens": m("not_applicable"),
        }
        errors = getattr(r, "errors", ()) or ()
        detail = "; ".join(errors[:3]) if errors else ""
        results.append(
            {
                "scenario_id": _slug(
                    f"{getattr(r, 'path', Path('')).parent.name}-{r.scenario}"
                    if getattr(r, "path", None)
                    else str(r.scenario)
                ),
                "verdict": "pass" if r.passed else "fail",
                "duration_ms": elapsed,
                "detail": detail,
                "evidence_ref": str(
                    Path(getattr(r, "path", "") or "").relative_to(checkout)
                    if getattr(r, "path", None)
                    else ""
                ),
                "judge": None,
                "metrics": metrics,
            }
        )

    receipt = {
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "external": False,
        "suite": SUITE,
        "forge": FORGE,
        "mode": a.mode,
        "notes": [f"labs_root={checkout / 'labs'}"],
        "producer": {"id": FORGE, "version": "lab-script"},
        "results": results,
    }
    out = Path(a.result_out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
