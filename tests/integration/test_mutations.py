"""P6 metamorphic/mutation suite: expected detections under mutation.

Each case applies one detrimental mutation to a minimal project and
asserts the engine produces the expected check ids — a mutation the
Doctor cannot detect is a coverage gap, not a test tweak. Metamorphic
invariant: unmutated projects must NOT produce the expected ids; the
mutated tree must.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from forge_doctor_data.cli import app

runner = CliRunner()


def _scan_ids(proj: Path) -> set[str]:
    out = runner.invoke(app, ["scan", str(proj), "-f", "json"])
    assert out.exit_code in (0, 1), out.output
    return {r["check_id"] for r in json.loads(out.output)["results"]}


def _write(proj: Path, files: dict[str, str]) -> None:
    proj.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (proj / name).write_text(content, encoding="utf-8")


_SPARK_BASE = "import pyspark\ndf = spark.table('t')\n"

_MUTATIONS: list[tuple[str, dict[str, str], dict[str, str], set[str]]] = [
    (
        "add-collect",
        {"job.py": _SPARK_BASE},
        {"job.py": _SPARK_BASE + "df.collect()\n"},
        {"SPARK001"},
    ),
    (
        "single-partition-write",
        {"job.py": _SPARK_BASE + "df.write.parquet('out')\n"},
        {"job.py": _SPARK_BASE + "df.repartition(1).write.parquet('out')\n"},
        {"PARQ010"},
    ),
    (
        "remove-checkpoint",
        {
            "stream.py": (
                "q = (df.writeStream\n"
                "     .format('parquet')\n"
                "     .option('checkpointLocation', 's3://ckpt')\n"
                "     .start())\n"
            )
        },
        {"stream.py": "q = df.writeStream.format('parquet').start()\n"},
        {"STREAM002"},
    ),
    (
        "glue-downgrade",
        {"job.py": ("import awsglue\nclient.create_job(Name='etl', GlueVersion='5.0')\n")},
        {"job.py": ("import awsglue\nclient.create_job(Name='etl', GlueVersion='2.0')\n")},
        {"GLUE002"},
    ),
    (
        "iceberg-format-downgrade",
        {
            "ddl.sql": (
                "CREATE TABLE t (id INT) USING iceberg "
                "TBLPROPERTIES ('format-version'='2');\n"
                "MERGE INTO t USING s ON t.id = s.id "
                "WHEN MATCHED THEN UPDATE SET *;\n"
            )
        },
        {
            "ddl.sql": (
                "CREATE TABLE t (id INT) USING iceberg "
                "TBLPROPERTIES ('format-version'='1');\n"
                "MERGE INTO t USING s ON t.id = s.id "
                "WHEN MATCHED THEN UPDATE SET *;\n"
            )
        },
        {"ICE001"},
    ),
    (
        "remove-partition-strategy",
        {
            "ddl.sql": (
                "CREATE TABLE t (id INT, d STRING) USING iceberg "
                "PARTITIONED BY (d);\n"
                "MERGE INTO t USING s ON t.id = s.id "
                "WHEN MATCHED THEN UPDATE SET *;\n"
            )
        },
        {
            "ddl.sql": (
                "CREATE TABLE t (id INT, d STRING) USING iceberg;\n"
                "MERGE INTO t USING s ON t.id = s.id "
                "WHEN MATCHED THEN UPDATE SET *;\n"
            )
        },
        {"ICE002"},
    ),
    (
        "dynamicframe-mix",
        {"job.py": ("import awsglue\nimport pyspark\ndf = spark.table('t')\n")},
        {
            "job.py": (
                "import awsglue\nimport pyspark\n"
                "from awsglue.dynamicframe import DynamicFrame\n"
                "dyf = DynamicFrame(glueContext)\n"
                "df = dyf.toDF()\n"
            )
        },
        {"GLUE004"},
    ),
]


@pytest.mark.parametrize(
    ("name", "baseline_files", "mutated_files", "expected"),
    _MUTATIONS,
    ids=[m[0] for m in _MUTATIONS],
)
def test_expected_detection_under_mutation(
    tmp_path: Path,
    name: str,
    baseline_files: dict[str, str],
    mutated_files: dict[str, str],
    expected: set[str],
) -> None:
    proj = tmp_path / "proj"
    _write(proj, baseline_files)
    before = _scan_ids(proj)
    assert not expected & before, f"{name}: {expected & before} before mutation"

    _write(proj, mutated_files)
    after = _scan_ids(proj)
    missing = expected - after
    assert not missing, f"{name}: mutation not detected ({sorted(missing)})"


def test_identical_scan_is_byte_identical(tmp_path: Path) -> None:
    """Metamorphic determinism: same tree → same JSON, twice."""
    proj = tmp_path / "proj"
    _write(proj, {"job.py": _SPARK_BASE + "df.collect()\n"})
    first = runner.invoke(app, ["scan", str(proj), "-f", "json"]).output
    second = runner.invoke(app, ["scan", str(proj), "-f", "json"]).output
    assert first == second
