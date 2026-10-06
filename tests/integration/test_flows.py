"""P5 integration flows — end-to-end journeys, not isolated flags.

Flow A: scan → save baseline → modify fixture → diff → new-only.
Flow B: runtime evidence → history → baseline → regression →
        correlation → incident.
Flow C: workspace → fleet → portfolio → regressions.
Flow D: export handoff → contract validation → consumer deserialization.
Flow E: plugin injection → plugins validate/doctor → scan.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from forge_doctor_data.cli import app

runner = CliRunner()


# --------------------------------------------------------------------------
# Flow A — scan/baseline/diff/new-only
# --------------------------------------------------------------------------


def test_flow_a_scan_baseline_modify_diff_newonly(tmp_path: Path) -> None:
    proj = tmp_path / "proj"
    proj.mkdir()
    (proj / "job.py").write_text(
        "import pyspark\ndf = spark.table('t')\ndf.collect()\n", encoding="utf-8"
    )
    baseline = tmp_path / "baseline.json"
    report_path = tmp_path / "report.json"

    first = runner.invoke(
        app,
        [
            "scan",
            str(proj),
            "--save-baseline",
            str(baseline),
            "-f",
            "json",
            "-o",
            str(report_path),
        ],
    )
    assert first.exit_code == 0, first.output
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert any(r["check_id"] == "SPARK001" for r in report["results"])

    # Unmodified tree → no new findings vs the saved baseline.
    clean = runner.invoke(app, ["scan", str(proj), "--baseline", str(baseline), "--new-only"])
    assert clean.exit_code == 0

    # Modify the fixture: a second collect() must surface as NEW only.
    (proj / "job2.py").write_text(
        "import pyspark\ndf2 = spark.table('u')\ndf2.collect()\n", encoding="utf-8"
    )
    new_only = runner.invoke(
        app,
        ["scan", str(proj), "--baseline", str(baseline), "--new-only", "-f", "json"],
    )
    payload = json.loads(new_only.output)
    files = {r["file"] for r in payload["results"] if r["file"]}
    assert files and all("job2" in f for f in files), files

    # diff two saved reports: new/resolved tracking.
    new_report = tmp_path / "new.json"
    runner.invoke(app, ["scan", str(proj), "-f", "json", "-o", str(new_report)])
    diff = runner.invoke(app, ["diff", str(report_path), str(new_report)])
    assert diff.exit_code in (0, 1)
    assert "new" in diff.output.lower()


# --------------------------------------------------------------------------
# Flow B — runtime evidence lifecycle
# --------------------------------------------------------------------------

_SPARK_LOG = "\n".join(
    [
        json.dumps(
            {"Event": "SparkListenerApplicationStart", "App Name": "etl", "App ID": "app-1"}
        ),
        json.dumps({"Event": "SparkListenerJobStart", "Job ID": 0}),
        json.dumps(
            {
                "Event": "SparkListenerStageCompleted",
                "Stage Info": {
                    "Stage ID": 0,
                    "Number of Tasks": 4,
                    "Accumulables": [
                        {"Name": "internal.metrics.shuffle.write.bytesWritten", "Value": 2048},
                        {"Name": "internal.metrics.memoryBytesSpilled", "Value": 512},
                    ],
                },
            }
        ),
        *(
            json.dumps(
                {
                    "Event": "SparkListenerTaskEnd",
                    "Task Info": {"Stage ID": 0, "Task ID": i},
                    "Task Metrics": {"Executor Run Time": d, "JVM GC Time": 5},
                }
            )
            for i, d in enumerate((10, 11, 12, 100))
        ),
        json.dumps(
            {"Event": "SparkListenerJobEnd", "Job ID": 0, "Job Result": {"Result": "JobSucceeded"}}
        ),
    ]
)


def test_flow_b_runtime_evidence_lifecycle(tmp_path: Path) -> None:
    root = tmp_path / "proj"
    root.mkdir()
    artifact = tmp_path / "eventlog.jsonl"
    artifact.write_text(_SPARK_LOG, encoding="utf-8")

    # evidence → normalized executions
    norm = runner.invoke(app, ["runtime", "executions", str(artifact)])
    assert norm.exit_code == 0, norm.output

    # record into history, then the series is listed
    for _ in range(3):
        rec = runner.invoke(app, ["runtime", "history", str(artifact), "--root", str(root)])
        assert rec.exit_code == 0, rec.output
    series = runner.invoke(app, ["runtime", "history", "--root", str(root), "--json"])
    assert series.exit_code == 0

    # baseline over the recorded series
    base = runner.invoke(app, ["runtime", "baseline", "--root", str(root)])
    assert base.exit_code == 0, base.output

    # regression scan over the same history (may legitimately report none)
    reg = runner.invoke(app, ["runtime", "regressions", "--root", str(root)])
    assert reg.exit_code in (0, 1), reg.output

    # correlation + incident grouping over recorded events
    events = tmp_path / "events.json"
    events.write_text(
        json.dumps(
            [
                {
                    "entities": ["spark:job:etl"],
                    "timestamp": "2026-10-01T00:00:00Z",
                    "class": "deploy",
                    "commit": "abc123",
                }
            ]
        ),
        encoding="utf-8",
    )
    corr = runner.invoke(app, ["runtime", "correlate", str(events), "--root", str(root)])
    assert corr.exit_code in (0, 1), corr.output
    inc = runner.invoke(app, ["incident", "inspect", "--root", str(root)])
    assert inc.exit_code == 0, inc.output


# --------------------------------------------------------------------------
# Flow C — workspace → fleet → portfolio → regressions
# --------------------------------------------------------------------------


def _monorepo(root: Path) -> None:
    a = root / "repo-a"
    a.mkdir(parents=True)
    (a / "pyproject.toml").write_text('[project]\nname = "a"\n', encoding="utf-8")
    (a / "job.py").write_text("import pyspark\ndf.collect()\n", encoding="utf-8")
    b = root / "repo-b"
    (b / "dags").mkdir(parents=True)
    (b / "dags" / "dag.py").write_text(
        "from airflow import DAG\ndag = DAG('etl')\n", encoding="utf-8"
    )


def test_flow_c_workspace_fleet_portfolio(tmp_path: Path) -> None:
    ws = tmp_path / "ws"
    ws.mkdir()
    _monorepo(ws)

    discovered = runner.invoke(app, ["workspace", "inspect", "--path", str(ws)])
    assert discovered.exit_code == 0, discovered.output

    manifest = ws / "fleet.yml"
    manifest.write_text("repos:\n  - path: ./repo-a\n  - path: ./repo-b\n", encoding="utf-8")
    for step in ("inspect", "report", "portfolio", "regressions"):
        out = runner.invoke(app, ["fleet", step, str(manifest)])
        assert out.exit_code in (0, 1), f"fleet {step}: {out.output}"


# --------------------------------------------------------------------------
# Flow D — export handoff → contract validation → consumer
# --------------------------------------------------------------------------


def test_flow_d_handoff_contract_consumer(tmp_path: Path) -> None:
    proj = tmp_path / "proj"
    proj.mkdir()
    (proj / "job.py").write_text("import pyspark\ndf.collect()\n", encoding="utf-8")

    bundle_path = tmp_path / "bundle.json"
    exported = runner.invoke(
        app, ["export", str(proj), "--format", "handoff", "-o", str(bundle_path)]
    )
    assert exported.exit_code == 0, exported.output

    verified = runner.invoke(
        app, ["contracts", "verify", str(bundle_path), "--contract", "handoff-bundle"]
    )
    assert verified.exit_code == 0, verified.output

    # A downstream consumer deserializes via the shared contract models.
    from forge_doctor_data.contracts import HandoffBundle

    payload = json.loads(bundle_path.read_text(encoding="utf-8"))
    bundle = HandoffBundle.from_dict(payload)
    assert bundle.tool == "forge-doctor-data"
    assert bundle.findings or bundle.summary


# --------------------------------------------------------------------------
# Flow E — plugin injection → validate/doctor/scan
# --------------------------------------------------------------------------


def test_flow_e_plugin_injection_pipeline(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from importlib.metadata import EntryPoint

    from forge_doctor_data.core.models import CheckResult, Severity
    from forge_doctor_data.plugins import discovery

    class DemoCheck:
        id = "DEMO001"
        title = "demo plugin check"
        category = "demo"
        why = "w"
        when_ok = "ok"
        fix = "f"

        def run(self, ctx) -> list:
            return [
                CheckResult(
                    check_id="DEMO001",
                    title=self.title,
                    severity=Severity.INFO,
                    category=self.category,
                    message="plugin finding",
                )
            ]

    ep = EntryPoint(name="demo", value="x:Y", group="forge_doctor_data.checks")
    monkeypatch.setattr(ep.__class__, "load", lambda self: DemoCheck)
    monkeypatch.setattr(discovery, "iter_entry_points", lambda: [ep])

    assert runner.invoke(app, ["plugins", "list"]).exit_code == 0
    assert runner.invoke(app, ["plugins", "validate"]).exit_code == 0
    assert runner.invoke(app, ["plugins", "doctor"]).exit_code == 0

    proj = tmp_path / "proj"
    proj.mkdir()
    (proj / "a.py").write_text("x = 1\n", encoding="utf-8")
    scan = runner.invoke(app, ["scan", str(proj), "-f", "json", "--profile", "demo"])
    # The plugin check is untrusted by default → skipped; --allow would
    # be required. Either way the scan must not crash.
    assert scan.exit_code in (0, 1, 2)
