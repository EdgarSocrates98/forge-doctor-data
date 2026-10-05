"""Schema freeze gate (phase 8.6).

Every published wire schema — the ``forge-contracts/1`` family and the
legacy artifact schemas — is digested into ``docs/schema-freeze.json``.
During the RC window any schema drift must fail this gate until someone
explicitly re-approves it:

    python tools/schema_freeze.py --check      # CI / RC gate (exit 1 on drift)
    python tools/schema_freeze.py --update --approve "name — reason"

The freeze file records the approving note so an update is a reviewable,
auditable act rather than silent drift.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

FREEZE_PATH = ROOT / "docs" / "schema-freeze.json"
FREEZE_KIND = "forge-doctor-data/schema-freeze"


def _canonical_digest(name: str, schema: dict[str, Any]) -> str:
    """Digest independent of key order and whitespace."""
    canon = json.dumps(schema, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(f"{name}:{canon}".encode()).hexdigest()


def current_digests() -> dict[str, str]:
    """``{family/name: sha256}`` over every published schema."""
    from forge_doctor_data.contracts.schemas import FORGE_CONTRACT_SCHEMAS
    from forge_doctor_data.core.schemas import SCHEMAS

    digests: dict[str, str] = {}
    for kind, schema in sorted(FORGE_CONTRACT_SCHEMAS.items()):
        digests[f"forge-contracts-1/{kind}"] = _canonical_digest(
            f"forge-contracts-1/{kind}", schema
        )
    for name, schema in sorted(SCHEMAS.items()):
        digests[f"legacy/{name}"] = _canonical_digest(f"legacy/{name}", schema)
    return digests


def _git_head(root: Path) -> str | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return out.stdout.strip() or None if out.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def load_freeze(path: Path = FREEZE_PATH) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read freeze file {path}: {exc}") from exc
    if not isinstance(payload, dict) or payload.get("kind") != FREEZE_KIND:
        raise ValueError(f"{path}: not a {FREEZE_KIND} document")
    return payload


def check(path: Path = FREEZE_PATH) -> list[str]:
    """Return drift descriptions; empty list means frozen == current."""
    frozen = load_freeze(path).get("schemas", {})
    current = current_digests()
    drift: list[str] = []
    for name in sorted(set(frozen) | set(current)):
        before, after = frozen.get(name), current.get(name)
        if before is None:
            drift.append(f"{name}: added (not in freeze)")
        elif after is None:
            drift.append(f"{name}: removed (freeze still lists it)")
        elif before != after:
            drift.append(f"{name}: content changed")
    return drift


def update(path: Path = FREEZE_PATH, approve: str = "") -> dict[str, Any]:
    if not approve.strip():
        raise ValueError('--update requires --approve "<name> — <reason>"')
    payload = {
        "kind": FREEZE_KIND,
        "schema_version": "1",
        "frozen_at_commit": _git_head(ROOT),
        "approved": approve.strip(),
        "schemas": current_digests(),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail on schema drift")
    parser.add_argument("--update", action="store_true", help="rewrite the freeze file")
    parser.add_argument("--approve", default="", help="approver — reason (required with --update)")
    parser.add_argument("--freeze", type=Path, default=FREEZE_PATH)
    args = parser.parse_args()

    try:
        if args.update:
            payload = update(args.freeze, args.approve)
            print(f"schema freeze updated: {len(payload['schemas'])} schemas")
            return 0
        drift = check(args.freeze)
    except ValueError as exc:
        print(f"schema-freeze: {exc}", file=sys.stderr)
        return 1
    if drift:
        print("schema-freeze DRIFT (explicit approval required):", file=sys.stderr)
        for line in drift:
            print(f"  {line}", file=sys.stderr)
        print(
            're-approve: python tools/schema_freeze.py --update --approve "<who> — <why>"',
            file=sys.stderr,
        )
        return 1
    print("schema-freeze: all published schemas match the approved digests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
