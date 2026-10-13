"""Release-candidate pipeline (spec 272, Phase H).

Builds the full RC artifact set locally - no publishing, no network:

1. ``verify_release.py`` metadata gate (version/tag coherence).
2. ``poetry build`` (skipped with ``--no-build`` to reuse an existing
   ``dist/``).
3. ``dist/sbom.json`` - CycloneDX 1.5 SBOM of the project itself.
4. ``dist/SHA256SUMS`` - sha256 + byte size for every artifact.
5. ``dist/schemas/`` - the published wire schemas as release files:
   ``forge-contracts-1/<kind>.json`` and ``legacy/<name>.json``.
6. ``dist/release-manifest.json`` - deterministic manifest: version,
   git HEAD, artifact digests, contract versions, schema list.
7. ``dist/provenance.json`` - in-toto/SLSA-lite statement linking
   subjects (digests) to this build and the source revision.
8. ``dist/env-manifest.json`` - the CI environment manifest.

Everything is sorted/deterministic; a timestamp is only emitted when
``SOURCE_DATE_EPOCH`` is set (reproducible-build convention).

Usage::

    python tools/release_candidate.py                # full dry run
    python tools/release_candidate.py --no-build     # reuse dist/
    python tools/release_candidate.py --dist out/    # other artifact dir
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

import env_manifest  # noqa: E402
import verify_release  # noqa: E402

from forge_doctor_data.contracts.schemas import FORGE_CONTRACT_SCHEMAS  # noqa: E402
from forge_doctor_data.core.schemas import SCHEMAS  # noqa: E402

MANIFEST_KIND = "forge-doctor-data/release-manifest"
PROVENANCE_TYPE = "https://in-toto.io/Statement/v1"
PROVENANCE_PREDICATE = "https://slsa.dev/provenance/v1"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact_entries(dist: Path) -> list[dict[str, Any]]:
    """Digest+size for every distribution artifact, sorted by name."""
    entries = []
    for p in sorted(dist.glob("forge_doctor_data-*")):
        if p.is_file():
            entries.append({"file": p.name, "sha256": sha256_file(p), "bytes": p.stat().st_size})
    return entries


def write_sha256sums(dist: Path, entries: list[dict[str, Any]]) -> Path:
    out = dist / "SHA256SUMS"
    out.write_text("".join(f"{e['sha256']}  {e['file']}\n" for e in entries), encoding="utf-8")
    return out


def export_schemas(dist: Path) -> list[str]:
    """Dump every published wire schema as a release file; return relpaths."""
    written: list[str] = []
    for kind, schema in sorted(FORGE_CONTRACT_SCHEMAS.items()):
        rel = Path("schemas") / "forge-contracts-1" / f"{kind}.json"
        target = dist / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        written.append(rel.as_posix())
    for name, schema in sorted(SCHEMAS.items()):
        rel = Path("schemas") / "legacy" / f"{name}.json"
        target = dist / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        written.append(rel.as_posix())
    return written


def _git(root: Path, *args: str) -> str | None:
    try:
        out = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=10)
        if out.returncode != 0:
            return None
        return out.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def build_release_manifest(
    root: Path,
    dist: Path,
    version: str,
    entries: list[dict[str, Any]],
    schema_files: list[str],
) -> dict[str, Any]:
    import forge_doctor_data.api as api

    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    return {
        "kind": MANIFEST_KIND,
        "schema_version": "1",
        "name": "forge-doctor-data",
        "version": version,
        "git": {
            "head": _git(root, "rev-parse", "HEAD"),
            "remote": _git(root, "config", "--get", "remote.origin.url"),
            "dirty": bool(_git(root, "status", "--porcelain")),
        },
        "contracts": {
            "forge-contracts": "forge-contracts/1",
            "scan-report": api.SCAN_SCHEMA_VERSION,
            "artifact-family": api.SCHEMA_VERSION,
        },
        "artifacts": entries,
        "schemas": schema_files,
        "generated": {
            "tool": "tools/release_candidate.py",
            "source_date_epoch": int(epoch) if epoch else None,
        },
    }


def build_provenance(root: Path, entries: list[dict[str, Any]]) -> dict[str, Any]:
    """in-toto statement with a SLSA-lite provenance predicate."""
    return {
        "_type": PROVENANCE_TYPE,
        "subject": [{"name": e["file"], "digest": {"sha256": e["sha256"]}} for e in entries],
        "predicateType": PROVENANCE_PREDICATE,
        "predicate": {
            "buildType": "forge-doctor-data/release-candidate",
            "builder": {"id": "tools/release_candidate.py"},
            "materials": [
                {
                    "uri": _git(root, "config", "--get", "remote.origin.url") or "",
                    "digest": {"sha1": _git(root, "rev-parse", "HEAD") or ""},
                }
            ],
        },
    }


def _build_sbom(root: Path, dist: Path) -> Path:
    from forge_doctor_data.core.context import ProjectContext
    from forge_doctor_data.core.sbom import build_sbom

    out = dist / "sbom.json"
    bom = build_sbom(ProjectContext(root=root))
    out.write_text(json.dumps(bom, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def _check_dirty(root: Path, allow_dirty: bool) -> None:
    """Phase 8.4: a dirty tree means unreviewed state in the artifacts —
    refuse unless the caller explicitly opts out (local dry runs)."""
    if allow_dirty:
        return
    dirty = _git(root, "status", "--porcelain")
    if dirty:
        raise ValueError(
            "working tree is dirty — commit or stash before building RC "
            "artifacts (pass --allow-dirty for a local dry run)"
        )


def _check_artifact_kinds(entries: list[dict[str, Any]]) -> None:
    """Phase 8.5: the set must contain both a wheel and an sdist — a lone
    wheel means the sdist was never built or was lost."""
    names = {e["file"] for e in entries}
    if not any(n.endswith(".whl") for n in names):
        raise ValueError("distribution set has no wheel (*.whl)")
    if not any(n.endswith(".tar.gz") for n in names):
        raise ValueError("distribution set has no sdist (*.tar.gz)")


def _verify_digests(dist: Path, sums_file: Path) -> None:
    """Phase 8.3: re-hash every listed artifact against SHA256SUMS — the
    digest file must describe the bytes on disk, not a prior build."""
    for line in sums_file.read_text(encoding="utf-8").splitlines():
        digest, _, name = line.partition("  ")
        target = dist / name
        if not target.is_file() or sha256_file(target) != digest:
            raise ValueError(f"SHA256SUMS mismatch for {name}")


def _build_env(root: Path) -> dict[str, str]:
    """Phase 8.2: honor SOURCE_DATE_EPOCH; when unset, derive it from the
    HEAD commit timestamp so the same checkout builds reproducibly."""
    env = dict(os.environ)
    if "SOURCE_DATE_EPOCH" not in env:
        stamp = _git(root, "show", "-s", "--format=%ct", "HEAD")
        if stamp and stamp.isdigit():
            env["SOURCE_DATE_EPOCH"] = stamp
    return env


def run(
    root: Path, dist: Path, *, build: bool = True, allow_dirty: bool = False
) -> dict[str, Path]:
    """Full RC pipeline; returns the written artifact paths."""
    _check_dirty(root, allow_dirty)
    version = verify_release.verify(root)
    if build:
        subprocess.run(["poetry", "build"], cwd=root, check=True, env=_build_env(root))
    if not dist.is_dir() or not any(dist.glob("forge_doctor_data-*")):
        raise ValueError(f"no distribution artifacts in {dist} (build first?)")
    verify_release.verify(root, dist)

    outputs: dict[str, Path] = {}
    outputs["sbom"] = _build_sbom(root, dist)
    entries = artifact_entries(dist)
    _check_artifact_kinds(entries)
    outputs["sha256sums"] = write_sha256sums(dist, entries)
    _verify_digests(dist, outputs["sha256sums"])
    schema_files = export_schemas(dist)
    manifest = build_release_manifest(root, dist, version, entries, schema_files)
    outputs["manifest"] = dist / "release-manifest.json"
    outputs["manifest"].write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    outputs["provenance"] = dist / "provenance.json"
    outputs["provenance"].write_text(
        json.dumps(build_provenance(root, entries), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    outputs["env"] = dist / "env-manifest.json"
    outputs["env"].write_text(
        json.dumps(env_manifest.build_manifest(root), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--dist", type=Path, default=None, help="artifact dir (default: <root>/dist)"
    )
    parser.add_argument("--no-build", action="store_true", help="reuse existing dist/")
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="skip the clean-tree gate (local dry runs only)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    dist = (args.dist or root / "dist").resolve()
    try:
        outputs = run(root, dist, build=not args.no_build, allow_dirty=args.allow_dirty)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"release-candidate failed: {exc}", file=sys.stderr)
        return 1
    for name, path in sorted(outputs.items()):
        print(f"  {name:12} {path.relative_to(root)}")
    print("release candidate artifacts ready (dry-run; nothing published)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
