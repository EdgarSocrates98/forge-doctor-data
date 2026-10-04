"""Spec-257 fleet-scale benchmark: cold/warm scan curves at N repos.

Generates a deterministic synthetic workspace (seeded, offline) and
measures per-repo cold and warm scan times plus aggregate wall time.
Budgets in ``docs/performance-budgets.md`` must cite a recorded run.

Usage:
    python tools/benchmarks/fleet.py --sizes 10,50 --root .pytest_tmp/fleet
    python tools/benchmarks/fleet.py --sizes 10 --json
"""

from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
import time
import tracemalloc
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from forge_doctor_data.core.service import ScanRequest, ScanService

_PYSPARK_JOB = """import pyspark
df = spark.table('{table}')
df.filter(df.id > {threshold}).write.parquet('out/{i}')
"""

_SQL = """CREATE TABLE t{i} (id INT, d STRING) USING iceberg
PARTITIONED BY (d);
INSERT INTO t{i} SELECT * FROM s;
"""

_TF = """resource "aws_glue_job" "j{i}" {{
  name = "job-{i}"
  glue_version = "{glue}"
}}
"""


def generate_repo(root: Path, i: int, rng: random.Random) -> Path:
    """Create one deterministic synthetic repo: 3 files, seeded content."""
    repo = root / f"repo-{i:04d}"
    repo.mkdir(parents=True, exist_ok=True)
    (repo / "job.py").write_text(
        _PYSPARK_JOB.format(table=f"t{i}", threshold=rng.randint(0, 99), i=i),
        encoding="utf-8",
    )
    (repo / "ddl.sql").write_text(_SQL.format(i=i), encoding="utf-8")
    (repo / "main.tf").write_text(
        _TF.format(i=i, glue=rng.choice(["4.0", "5.0"])), encoding="utf-8"
    )
    return repo


def generate_workspace(root: Path, n: int, seed: int) -> list[Path]:
    rng = random.Random(seed)
    return [generate_repo(root, i, rng) for i in range(n)]


@dataclass(frozen=True)
class SizeResult:
    repos: int
    files: int
    cold_ms_mean: float
    cold_ms_p50: float
    warm_ms_mean: float
    findings_mean: float
    peak_mb: float
    wall_s: float


def measure_size(root: Path, n: int, seed: int) -> SizeResult:
    """Cold-scan every repo once, then warm-scan (cache hot) and time both."""
    repos = generate_workspace(root / f"n{n}", n, seed)
    service = ScanService()
    cold: list[float] = []
    warm: list[float] = []
    findings: list[int] = []
    tracemalloc.start()
    t0 = time.perf_counter()
    for repo in repos:
        t = time.perf_counter()
        outcome = service.run(ScanRequest(path=repo, cache=True))
        cold.append((time.perf_counter() - t) * 1000)
        findings.append(len(outcome.report.results))
    for repo in repos:
        t = time.perf_counter()
        service.run(ScanRequest(path=repo, cache=True))
        warm.append((time.perf_counter() - t) * 1000)
    wall = time.perf_counter() - t0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return SizeResult(
        repos=n,
        files=n * 3,
        cold_ms_mean=round(statistics.fmean(cold), 1),
        cold_ms_p50=round(statistics.median(cold), 1),
        warm_ms_mean=round(statistics.fmean(warm), 1),
        findings_mean=round(statistics.fmean(findings), 1),
        peak_mb=round(peak / 1e6, 1),
        wall_s=round(wall, 2),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", default="10", help="comma-separated repo counts")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--root", type=Path, default=Path(".pytest_tmp/fleet"))
    parser.add_argument("--out", type=Path, default=None, help="write JSON results")
    parser.add_argument(
        "--budget",
        type=Path,
        default=None,
        help=(
            'JSON budget, e.g. {"cold_ms_p50_max": 800, '
            '"ms_per_repo_wall_max": 1500}. A breached key fails the run; '
            "absent keys report 'unknown' and are not gated."
        ),
    )
    parser.add_argument("--json", action="store_true", help="print JSON to stdout")
    args = parser.parse_args()

    sizes = [int(s) for s in args.sizes.split(",") if s.strip()]
    results = [measure_size(args.root, n, args.seed) for n in sizes]
    payload = {
        "benchmark": "fleet",
        "seed": args.seed,
        "sizes": [asdict(r) for r in results],
    }
    text = json.dumps(payload, indent=2)
    if args.out is not None:
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    if not args.json:
        for r in results:
            print(
                f"n={r.repos:>5} files={r.files:>5} "
                f"cold={r.cold_ms_p50:>8.1f}ms/repo warm={r.warm_ms_mean:>7.1f}ms/repo "
                f"peak={r.peak_mb:>6.1f}MB wall={r.wall_s:>6.1f}s",
                file=sys.stderr,
            )
    if args.budget is not None:
        sys.exit(_check_budget(results, args.budget))


def _check_budget(results: list[SizeResult], budget_path: Path) -> int:
    """Gate measured curves against a JSON budget file.

    Reports per-key PASS/FAIL/unknown; a key absent from the budget is
    'unknown' (per docs/performance-budgets.md - no invented budgets).
    Exit 1 if any measured size breaches.
    """
    budget = json.loads(budget_path.read_text(encoding="utf-8"))
    worst = 0
    for r in results:
        measured = {
            "cold_ms_p50_max": r.cold_ms_p50,
            "cold_ms_mean_max": r.cold_ms_mean,
            "warm_ms_mean_max": r.warm_ms_mean,
            "ms_per_repo_wall_max": (r.wall_s * 1000) / r.repos if r.repos else 0.0,
            "peak_mb_max": r.peak_mb,
        }
        for key, value in measured.items():
            limit = budget.get(key)
            if limit is None:
                continue
            ok = value <= limit
            worst = worst or (not ok)
            print(
                f"budget n={r.repos} {key}: {value:.1f} {'<=' if ok else '>'} "
                f"{limit} -> {'PASS' if ok else 'FAIL'}",
                file=sys.stderr,
            )
    absent = [k for k in _BUDGET_KEYS if k not in budget]
    for key in absent:
        print(f"budget {key}: unknown (not in budget file)", file=sys.stderr)
    return int(worst)


_BUDGET_KEYS = (
    "cold_ms_p50_max",
    "cold_ms_mean_max",
    "warm_ms_mean_max",
    "ms_per_repo_wall_max",
    "peak_mb_max",
)


if __name__ == "__main__":
    main()
