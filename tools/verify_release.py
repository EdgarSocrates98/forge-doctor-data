"""Validate release metadata before artifacts leave CI.

The check is intentionally stdlib-only and deterministic so it can run before
any upload or publication step.
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

PROJECT_NAME = "forge-doctor-data"
ARTIFACT_RE = re.compile(r"^forge_doctor_data-(?P<version>[^-]+)-")


def project_version(root: Path) -> str:
    with (root / "pyproject.toml").open("rb") as fh:
        payload = tomllib.load(fh)
    version = payload.get("project", {}).get("version")
    if not isinstance(version, str) or not version:
        raise ValueError("pyproject.toml project.version is missing")
    return version


def artifact_versions(dist: Path) -> set[str]:
    versions: set[str] = set()
    for artifact in sorted(dist.glob("forge_doctor_data-*")):
        match = ARTIFACT_RE.match(artifact.name)
        if match:
            versions.add(match.group("version").replace("_", "+"))
    return versions


def verify(root: Path, dist: Path | None = None, tag: str | None = None) -> str:
    version = project_version(root)
    normalized_tag = (tag or "").removeprefix("v")
    if normalized_tag and normalized_tag != version:
        raise ValueError(f"tag version {normalized_tag!r} != project version {version!r}")
    if dist is not None:
        versions = artifact_versions(dist)
        if not versions:
            raise ValueError(f"no {PROJECT_NAME} artifacts found in {dist}")
        if versions != {version}:
            raise ValueError(
                f"artifact versions {sorted(versions)!r} != project version {version!r}"
            )
    return version


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dist", type=Path)
    parser.add_argument("--tag", default="")
    args = parser.parse_args()
    try:
        version = verify(args.root.resolve(), args.dist.resolve() if args.dist else None, args.tag)
    except (OSError, ValueError) as exc:
        print(f"release metadata invalid: {exc}", file=sys.stderr)
        return 1
    print(f"release metadata valid: {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
