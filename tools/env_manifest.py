"""Emit a deterministic environment manifest for CI/reproducibility audits.

Records exactly what produced a run so "clean install == CI == wheel" is an
observable claim, not a hope. Stdlib-only so it runs before ``poetry install``
and inside a bare wheel venv alike.

Fields: interpreter, platform, poetry version (or ``null`` when absent),
``poetry.lock`` sha256, project version, contract version, knowledge-pack
inventory (domain/name/pack_version/schema_version/verified_at), discovered
external plugins, and git state when inside a checkout.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import tomllib
from importlib import metadata
from pathlib import Path
from typing import Any

CONTRACT_VERSION = "forge-contracts/1"
ENTRY_POINT_GROUP = "forge_doctor_data.checks"


def _sha256(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def _project_version(root: Path) -> str | None:
    pyproject = root / "pyproject.toml"
    try:
        with pyproject.open("rb") as fh:
            version = tomllib.load(fh).get("project", {}).get("version")
        return version if isinstance(version, str) else None
    except (OSError, tomllib.TOMLDecodeError):
        return None


def _poetry_version() -> str | None:
    try:
        out = subprocess.run(
            ["poetry", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None
    # "Poetry (version 2.4.3)" -> "2.4.3"
    return out.rpartition(" ")[-1].strip(")") or None


def _knowledge_packs(root: Path) -> list[dict[str, Any]]:
    """Pack inventory straight from the JSON resources - no engine import."""
    packs: list[dict[str, Any]] = []
    knowledge = root / "src" / "forge_doctor_data" / "knowledge"
    if not knowledge.is_dir():
        return packs
    for domain_dir in sorted(p for p in knowledge.iterdir() if p.is_dir()):
        for pack_file in sorted(domain_dir.glob("*.json")):
            entry: dict[str, Any] = {"domain": domain_dir.name, "name": pack_file.stem}
            try:
                pack = json.loads(pack_file.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                entry["status"] = "unreadable"
                packs.append(entry)
                continue
            entry["schema_version"] = pack.get("schema_version")
            entry["pack_version"] = pack.get("pack_version")
            entry["verified_at"] = pack.get("verified_at")
            packs.append(entry)
    return packs


def _plugins() -> list[dict[str, Any]]:
    """External entry points visible in this environment (none is also data)."""
    try:
        eps = list(metadata.entry_points(group=ENTRY_POINT_GROUP))
    except Exception:  # manifest must never crash CI
        return []
    found: list[dict[str, Any]] = []
    for ep in sorted(eps, key=lambda e: e.name):
        dist = getattr(ep, "dist", None)
        found.append(
            {
                "name": ep.name,
                "value": ep.value,
                "distribution": getattr(dist, "name", None) or None,
                "version": getattr(dist, "version", None) or None,
            }
        )
    return found


def _git(root: Path) -> dict[str, Any]:
    def run(*args: str) -> str | None:
        try:
            out = subprocess.run(
                ["git", "-C", str(root), *args],
                capture_output=True,
                text=True,
                timeout=10,
            )
        except (OSError, subprocess.SubprocessError):
            return None
        return out.stdout.strip() if out.returncode == 0 else None

    sha = run("rev-parse", "HEAD")
    if sha is None:
        return {"available": False}
    dirty = run("status", "--porcelain")
    return {
        "available": True,
        "head": sha,
        "dirty": bool(dirty),
    }


def build_manifest(root: Path) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "kind": "forge-doctor-data/env-manifest",
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "executable": sys.executable,
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "poetry_version": _poetry_version(),
        "lockfile_sha256": _sha256(root / "poetry.lock"),
        "project": {
            "name": "forge-doctor-data",
            "version": _project_version(root)
            or (metadata.version("forge-doctor-data") if _installed() else None),
        },
        "contract_version": CONTRACT_VERSION,
        "knowledge_packs": _knowledge_packs(root),
        "plugins": _plugins(),
        "git": _git(root),
        "ci": {
            "github_actions": os.environ.get("GITHUB_ACTIONS") == "true",
            "run_id": os.environ.get("GITHUB_RUN_ID"),
            "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
            "ref": os.environ.get("GITHUB_REF"),
            "sha": os.environ.get("GITHUB_SHA"),
        },
    }


def _installed() -> bool:
    try:
        metadata.version("forge-doctor-data")
        return True
    except metadata.PackageNotFoundError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    manifest = build_manifest(args.root.resolve())
    text = json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
