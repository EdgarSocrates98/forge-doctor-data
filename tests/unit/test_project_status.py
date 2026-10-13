"""P3: deterministic project-status snapshot + doc-drift gate."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from forge_doctor_data.cli import app
from forge_doctor_data.core.project_status import (
    check_status_doc,
    collect_status,
    render_status_markdown,
    status_doc_path,
)

runner = CliRunner()


def test_collect_status_is_deterministic(tmp_path: Path) -> None:
    a = collect_status(tmp_path)
    b = collect_status(tmp_path)
    assert a == b
    assert render_status_markdown(a) == render_status_markdown(b)


def test_status_covers_all_registries(tmp_path: Path) -> None:
    status = collect_status(tmp_path)
    assert status["version"]
    assert "scan" in status["commands"]
    assert "project status" in status["commands"]
    assert status["check_total"] == sum(len(ids) for ids in status["checks"].values())
    assert "scan-report" in status["contracts"]
    assert status["mcp_tools"]
    assert "spark" in status["knowledge_domains"]
    assert set(status["factory"]) == {"inbox", "active", "archive", "runs"}


def test_check_missing_doc_reports_hint(tmp_path: Path) -> None:
    drift = check_status_doc(tmp_path)
    assert drift
    assert "missing" in drift[0]
    assert "--write" in drift[0]


def test_check_uptodate_doc(tmp_path: Path) -> None:
    target = status_doc_path(tmp_path)
    target.parent.mkdir(parents=True)
    target.write_text(render_status_markdown(collect_status(tmp_path)) + "\n", encoding="utf-8")
    assert check_status_doc(tmp_path) == []


def test_check_stale_doc_reports_diff(tmp_path: Path) -> None:
    target = status_doc_path(tmp_path)
    target.parent.mkdir(parents=True)
    target.write_text("# stale\n", encoding="utf-8")
    drift = check_status_doc(tmp_path)
    assert drift
    assert any(line.startswith("---") for line in drift)


def test_cli_status_text_and_json() -> None:
    text = runner.invoke(app, ["project", "status"])
    assert text.exit_code == 0
    assert "commands:" in text.output
    payload = runner.invoke(app, ["project", "status", "-f", "json"])
    assert payload.exit_code == 0
    assert json.loads(payload.output)["check_total"] > 0


def test_cli_rejects_bad_format() -> None:
    result = runner.invoke(app, ["project", "status", "-f", "yaml"])
    assert result.exit_code != 0
