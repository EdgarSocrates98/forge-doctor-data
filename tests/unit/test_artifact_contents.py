"""The wheel must carry the packaged `_data` labs + golden corpora.

`pyproject.toml` maps `labs` and `golden` into `forge_doctor_data/_data`
via `tool.poetry.packages.to`; inspecting the config proves intent, not
result — a packaging regression silently ships a wheel where `lab`/
`golden` resolvers find no packaged fallback. Building the real wheel
is the only honest gate (paridade api-forge test_artifact_contents).
"""

import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def wheel(tmp_path_factory) -> zipfile.ZipFile:
    out = tmp_path_factory.mktemp("dist")
    result = subprocess.run(
        [sys.executable, "-m", "build", "--wheel", "--outdir", str(out), str(ROOT)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        pytest.skip(f"`python -m build` unavailable or failed: {result.stderr[-400:]}")
    built = sorted(out.glob("*.whl"))
    assert built, "build succeeded without producing a wheel"
    return zipfile.ZipFile(built[0])


def _rel_set(wheel: zipfile.ZipFile, prefix: str) -> set[str]:
    return {
        n.removeprefix(prefix)
        for n in wheel.namelist()
        if n.startswith(prefix) and not n.endswith("/")
    }


def test_wheel_carries_packaged_labs(wheel):
    assert _rel_set(wheel, "forge_doctor_data/_data/labs/")


def test_wheel_carries_packaged_golden(wheel):
    assert _rel_set(wheel, "forge_doctor_data/_data/golden/")


def test_wheel_data_matches_checkout(wheel):
    for group in ("labs", "golden"):
        wheel_files = _rel_set(wheel, f"forge_doctor_data/_data/{group}/")
        checkout = {
            p.relative_to(ROOT / group).as_posix()
            for p in (ROOT / group).rglob("*")
            if p.is_file()
        }
        assert wheel_files == checkout, f"_data/{group} diverges from checkout"
