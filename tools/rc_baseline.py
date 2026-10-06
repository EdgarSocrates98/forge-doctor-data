"""RC baseline artifact generator (prompt_evo_rc_hardening Phase 1.4).

Writes ``docs/rc-baseline.json`` — the frozen reference point for the
1.0 release-candidate cycle. During RC the file is the drift ruler:
frozen fields (contract version, public API hash, MCP tool inventory)
must not move without an explicit maintainer decision; observational
fields (test count, coverage, corpus counts) are expected to grow and
are reported as drift, not failure.

Usage::

    python tools/rc_baseline.py                      # write docs/rc-baseline.json
    python tools/rc_baseline.py --tests 2400 --coverage 82.5
    python tools/rc_baseline.py --check              # verify frozen fields still hold

``--check`` exits non-zero when a frozen measurement moved: contract
version, public-API surface hash, or MCP tool count. Everything else is
printed as informational drift.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

BASELINE_PATH = ROOT / "docs" / "rc-baseline.json"
API_SURFACE_PATH = ROOT / "docs" / "api-surface.json"
KIND = "forge-doctor-data/rc-baseline"

# Frozen during RC — a mismatch here is a freeze violation, not drift.
FROZEN_FIELDS = ("contract_version", "mcp_tool_count", "public_api_sha256")


def _git(*args: str) -> str | None:
    try:
        out = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, timeout=10)
        if out.returncode != 0:
            return None
        return out.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def _count_tests() -> int | None:
    out = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "--co-q"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=300,
    )
    for line in reversed(out.stdout.splitlines()):
        m = re.search(r"(\d+) tests? collected", line)
        if m:
            return int(m.group(1))
    return None


def _coverage_percent() -> float | None:
    xml = ROOT / "coverage.xml"
    if not xml.exists():
        return None
    m = re.search(r'line-rate="([0-9.]+)"', xml.read_text(encoding="utf-8")[:2000])
    return round(float(m.group(1)) * 100, 2) if m else None


def _ci_jobs() -> dict[str, Any]:
    """Job ids declared in ci.yml plus the matrix-expanded job total."""
    ci = ROOT / ".github" / "workflows" / "ci.yml"
    jobs: list[str] = []
    matrices = 0
    in_jobs = False
    for line in ci.read_text(encoding="utf-8").splitlines():
        if re.match(r"^jobs:\s*$", line):
            in_jobs = True
            continue
        if in_jobs and re.match(r"^[a-zA-Z#]", line):  # left the jobs block
            in_jobs = False
        if not in_jobs:
            continue
        m = re.match(r"^  ([a-z][a-z0-9-]*):\s*$", line)
        if m:
            jobs.append(m.group(1))
        if re.search(r"matrix:\s*$", line):
            matrices += 1
    # matrix jobs expand: unit-tests x3 pythons, smoke x3 OSes
    matrix_total = len(jobs) - matrices + matrices * 3
    return {
        "workflow": "ci.yml",
        "jobs": jobs,
        "job_definitions": len(jobs),
        "matrix_total": matrix_total,
    }


def _fleet_envelope() -> dict[str, int | None]:
    budget = ROOT / "docs" / "benchmarks" / "fleet-budget.json"
    scale: dict[str, int | None] = {"scan": None, "merge": None}
    if budget.exists():
        baseline = json.loads(budget.read_text(encoding="utf-8")).get("baseline", {})
        for key in ("scan", "merge"):
            names = baseline.get(key, "") or ""
            if isinstance(names, str):
                names = [names]
            sizes = [int(s) for n in names for s in re.findall(r"n(\d+)", n)]
            if sizes:
                scale[key] = max(sizes)
    return scale


def collect_baseline(tests: int | None, coverage: float | None) -> dict[str, Any]:
    from forge_doctor_data import __version__
    from forge_doctor_data.core.handoff import CONTRACT_VERSION
    from forge_doctor_data.integrations.mcp_server import _TOOL_DEFS

    manifest = json.loads((ROOT / "golden" / "manifest.json").read_text(encoding="utf-8"))
    origins = [e.get("origin", "synthetic") for e in manifest["entries"]]
    labs = sorted((ROOT / "labs").glob("*/*/expected.json"))
    api_surface = API_SURFACE_PATH.read_bytes()

    real = sum(1 for o in origins if o in {"real", "real-oss"})
    return {
        "kind": KIND,
        "schema_version": "1",
        "rc_target": "1.0.0-rc1",
        "git": {
            "head": _git("rev-parse", "HEAD"),
            "branch": _git("rev-parse", "--abbrev-ref", "HEAD"),
            "dirty": bool(_git("status", "--porcelain")),
        },
        "package": {"name": "forge-doctor-data", "version": __version__},
        "verification": {"test_count": tests, "coverage_percent": coverage},
        "ci": _ci_jobs(),
        "contracts": {
            "contract_version": CONTRACT_VERSION,
            "family": f"forge-contracts/{CONTRACT_VERSION}",
        },
        "mcp": {"tool_count": len(_TOOL_DEFS)},
        "corpus": {
            "golden_entries": len(manifest["entries"]),
            "real_oss_entries": real,
            "synthetic_entries": sum(1 for o in origins if o == "synthetic"),
            "adversarial_entries": sum(1 for o in origins if o == "adversarial"),
        },
        "labs": {"scenario_count": len(labs)},
        "fleet": {
            "scan_validated_envelope": _fleet_envelope()["scan"],
            "merge_validated_envelope": _fleet_envelope()["merge"],
        },
        "public_api": {
            "public_api_sha256": hashlib.sha256(api_surface).hexdigest(),
            "surface_file": "docs/api-surface.json",
        },
    }


def flatten_frozen(baseline: dict[str, Any]) -> dict[str, Any]:
    return {
        "contract_version": baseline["contracts"]["contract_version"],
        "mcp_tool_count": baseline["mcp"]["tool_count"],
        "public_api_sha256": baseline["public_api"]["public_api_sha256"],
    }


def check() -> int:
    if not BASELINE_PATH.exists():
        print("docs/rc-baseline.json missing - run tools/rc_baseline.py")
        return 1
    recorded = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    if recorded.get("kind") != KIND:
        print(f"unexpected kind: {recorded.get('kind')!r}")
        return 1
    current = collect_baseline(None, None)
    failures = []
    for field in FROZEN_FIELDS:
        old, new = flatten_frozen(recorded)[field], flatten_frozen(current)[field]
        if old != new:
            failures.append(f"{field}: baseline={old} current={new}")
    if failures:
        print("RC freeze violations:")
        for f in failures:
            print(f"  {f}")
        return 1
    # Informational drift: observational fields are expected to move.
    drift = []
    for key in ("golden_entries", "real_oss_entries"):
        if recorded["corpus"][key] != current["corpus"][key]:
            drift.append(f"corpus.{key}: {recorded['corpus'][key]} -> {current['corpus'][key]}")
    if recorded["labs"]["scenario_count"] != current["labs"]["scenario_count"]:
        drift.append("labs.scenario_count changed")
    if drift:
        print("drift (informational):")
        for d in drift:
            print(f"  {d}")
    print("rc-baseline frozen fields intact")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify frozen fields unchanged")
    parser.add_argument("--tests", type=int, default=None, help="recorded test count")
    parser.add_argument("--coverage", type=float, default=None, help="recorded coverage percent")
    args = parser.parse_args()

    if args.check:
        return check()

    tests = args.tests if args.tests is not None else _count_tests()
    coverage = args.coverage if args.coverage is not None else _coverage_percent()
    baseline = collect_baseline(tests, coverage)
    BASELINE_PATH.write_text(
        json.dumps(baseline, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"wrote {BASELINE_PATH.relative_to(ROOT)}")
    if tests is None:
        print("warning: test count unknown (no --tests, collection failed)")
    if coverage is None:
        print("warning: coverage unknown (no --coverage, coverage.xml missing)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
