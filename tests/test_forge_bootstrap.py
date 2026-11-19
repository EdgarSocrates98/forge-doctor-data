"""``scripts/forge_bootstrap.py`` — vendored-copy drift gate + the
install-2.1 ``register`` propagation.

The script is imported by path (``scripts/`` is not a package). Writes
stay under ``FORGE_HOME_OVERRIDE`` — the same seam the install lifecycle
tests use — never the real ``~/.forge``.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "forge_bootstrap.py"


def _load_module() -> Any:
    spec = importlib.util.spec_from_file_location("forge_bootstrap", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture()
def fb() -> Any:
    return _load_module()


@pytest.fixture()
def forge_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("FORGE_HOME_OVERRIDE", str(home))
    return home


def _register_kwargs(cfg: dict, tmp: Path) -> dict:
    return {
        "cfg": cfg,
        "install_root": tmp / "root",
        "venv": tmp / "v",
        "version": "1.1.4",
        "source": {"kind": "pypi", "spec": "forge-doctor-data==1.1.4"},
        "shim": None,
        "mcp_cmd": ["forge-doctor-data", "mcp"],
        "mcp_name": "forge-doctor-data",
        "hosts": {},
    }


_CFG = {
    "forge_id": "forge-doctor-data",
    "package": "forge_doctor_data",
    "distribution": "forge-doctor-data",
    "cli": "forge-doctor-data",
    "python": ">=3.11",
}


# --------------------------------------------------------------------------
# Canonical drift gate
# --------------------------------------------------------------------------

# SHA-256 of the canonical the-forge/scripts/installkit/forge_bootstrap.py.
# The vendored copy is byte-identical to the canonical installkit variant —
# any upstream change must land deliberately: update the copy AND this pin
# in the same commit, never drift silently.
_CANONICAL_BOOTSTRAP_SHA256 = "02f20671e2020d3a719808a48cf0330348ab11902188534924f7f1aecede8384"


def test_bootstrap_byte_parity_with_canonical() -> None:
    digest = hashlib.sha256(SCRIPT.read_bytes()).hexdigest()
    assert digest == _CANONICAL_BOOTSTRAP_SHA256, (
        "scripts/forge_bootstrap.py drifted from the canonical "
        "the-forge/scripts/installkit/forge_bootstrap.py — re-vendor the "
        "canonical copy and update _CANONICAL_BOOTSTRAP_SHA256 together"
    )


# --------------------------------------------------------------------------
# register() — install-2.1 declared fields land in the manifest
# --------------------------------------------------------------------------


def test_register_writes_sorted_manifest(fb: Any, forge_home: Path, tmp_path: Path) -> None:
    path = fb.register(**_register_kwargs(dict(_CFG), tmp_path))
    assert path == forge_home / ".forge" / "installations" / "forge-doctor-data.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert doc["schema"] == "forge/InstallationManifest/v1"
    assert doc["installation_method"] == "pypi-wheel"  # derived from source.kind
    assert doc["mcp"]["verified"] is False
    assert doc["cli"]["version_cmd"] == ["forge-doctor-data", "--version"]


def test_register_propagates_install21_fields(fb: Any, forge_home: Path, tmp_path: Path) -> None:
    """forge.json install-2.1 declarations land verbatim in
    ``~/.forge/installations/<id>.json`` — the surface the orchestrator's
    typed delegation reads."""
    cfg = dict(_CFG)
    cfg.update(
        {
            "installation_kind": "content",
            "install_command": ["{python}", "-m", "forge_doctor_data", "install"],
            "install": {
                "operations": ["plan", "apply", "uninstall"],
                "flags": ["--scope", "--root", "--yes", "--dry-run"],
                "hosts": ["claude", "devin"],
                "scopes": ["project", "workspace", "user"],
                "profiles": ["minimal", "recommended", "full"],
                "approval": "--yes",
            },
            "depends_on": ["the-forge"],
        }
    )
    path = fb.register(**_register_kwargs(cfg, tmp_path))
    manifest = json.loads(path.read_text(encoding="utf-8"))
    assert manifest["installation_kind"] == "content"
    assert manifest["install_command"] == ["{python}", "-m", "forge_doctor_data", "install"]
    assert manifest["install"]["operations"] == ["plan", "apply", "uninstall"]
    assert manifest["install"]["approval"] == "--yes"
    assert manifest["depends_on"] == ["the-forge"]


def test_register_rejects_bad_installation_kind(fb: Any, forge_home: Path, tmp_path: Path) -> None:
    """An undeclared/invalid installation_kind is a typed refusal
    (FORGE-INSTALL-BAD-CONFIG), never a registered bad manifest."""
    cfg = dict(_CFG, installation_kind="widget")
    with pytest.raises(fb.Refusal) as exc:
        fb.register(**_register_kwargs(cfg, tmp_path))
    assert exc.value.kind == "FORGE-INSTALL-BAD-CONFIG"
    assert "widget" in exc.value.detail
    assert not (forge_home / ".forge" / "installations" / "forge-doctor-data.json").exists()


def test_register_omits_empty_declared_fields(fb: Any, forge_home: Path, tmp_path: Path) -> None:
    """Absent/empty declarations stay absent — ``depends_on: []`` is not
    fabricated into the doc (the wheel `_register` declares it
    explicitly; the bootstrap copies only real values)."""
    path = fb.register(**_register_kwargs(dict(_CFG), tmp_path))
    manifest = json.loads(path.read_text(encoding="utf-8"))
    assert "installation_kind" not in manifest
    assert "install" not in manifest
    assert "depends_on" not in manifest


# --------------------------------------------------------------------------
# setup.sh — vendored POSIX entry point (cycle 16.1.1)
# --------------------------------------------------------------------------


def test_setup_sh_sem_python_recusa_nomeada(tmp_path: Path) -> None:
    """``set -e`` must not kill the script before the named refusal.

    Regression: ``PY="$(command -v python3 || command -v python || command -v py)"``
    exits rc=1 silently when no python exists — the command substitution fails
    and ``set -e`` aborts the assignment before the ``FORGE-PYTHON-NOT-FOUND``
    branch runs. The probe must be guarded (``|| true``) so the script reaches
    its named refusal: rc=2 + ``FORGE-PYTHON-NOT-FOUND`` on stderr.
    """
    bash = shutil.which("bash")
    if not bash:
        pytest.skip("bash indisponivel")
    stub = tmp_path / "stubbin"
    stub.mkdir()
    # setup.sh runs `cd "$(dirname "$0")"` — dirname is the only binary the
    # PATH-stripped environment still needs before the python probe.
    dn = shutil.which("dirname")
    if dn:
        (stub / "dirname").symlink_to(dn)
    out = subprocess.run(
        [bash, "setup.sh"],
        cwd=SCRIPT.parents[1],
        env={"PATH": str(stub), "HOME": str(tmp_path)},
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert out.returncode == 2
    assert "FORGE-PYTHON-NOT-FOUND" in out.stderr
