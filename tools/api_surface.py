"""Public API surface inventory (spec 271, Phase G).

Emits a deterministic, machine-readable inventory of every public
surface the package freezes under semver, each tagged with a stability
class:

- ``stable`` - semver-bound; removals/renames need a MAJOR bump
- ``wire`` - external wire contract; follows its own version family
  (``forge-contracts/1``, ``SCAN_SCHEMA_VERSION``, ``SCHEMA_VERSION``,
  MCP protocol versions)
- ``ux`` - CLI names; deprecation policy governs changes

Usage::

    python tools/api_surface.py            # writes docs/api-surface.json
    python tools/api_surface.py --check    # fail when the file is stale
"""

from __future__ import annotations

import inspect
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

OUT = ROOT / "docs" / "api-surface.json"


def _signature(fn: Any) -> str | None:
    try:
        return str(inspect.signature(fn))
    except (TypeError, ValueError):
        return None


def collect_surface() -> dict[str, Any]:
    import forge_doctor_data.api as api
    import forge_doctor_data.contracts as contracts
    import forge_doctor_data.sdk as sdk
    from forge_doctor_data import __version__
    from forge_doctor_data.cli import app
    from forge_doctor_data.contracts.schemas import FORGE_CONTRACT_SCHEMAS
    from forge_doctor_data.core.schemas import SCHEMAS
    from forge_doctor_data.integrations import mcp_protocol
    from forge_doctor_data.integrations.mcp_server import _TOOL_DEFS

    api_entries = {
        name: {
            "kind": "constant" if not callable(getattr(api, name)) else "callable",
            "signature": _signature(getattr(api, name)),
        }
        for name in sorted(api.__all__)
    }
    contract_fixture_names = sorted(
        p.name for p in (ROOT / "src/forge_doctor_data/contracts/fixtures").glob("*.json")
    )
    return {
        "schema_version": "1",
        "package_version": __version__,
        "stability_classes": {
            "stable": "semver-bound; removal or rename requires a MAJOR bump",
            "wire": "external contract; follows its own version family",
            "ux": "CLI surface; governed by docs/deprecation.md policy",
        },
        "surfaces": {
            "python_api": {
                "stability": "stable",
                "module": "forge_doctor_data.api",
                "entries": api_entries,
            },
            "plugin_sdk": {
                "stability": "stable",
                "module": "forge_doctor_data.sdk",
                "entries": {name: {} for name in sorted(sdk.__all__)},
            },
            "contracts_vocabulary": {
                "stability": "wire",
                "module": "forge_doctor_data.contracts",
                "contract_version": str(contracts.CONTRACT_VERSION),
                "entries": {name: {} for name in sorted(contracts.__all__)},
            },
            "contracts_schemas": {
                "stability": "wire",
                "module": "forge_doctor_data.contracts.schemas",
                "entries": {
                    name: {"$id": s["$id"]} for name, s in sorted(FORGE_CONTRACT_SCHEMAS.items())
                },
            },
            "contracts_fixtures": {
                "stability": "wire",
                "module": "forge_doctor_data.contracts.fixtures",
                "entries": {name: {} for name in contract_fixture_names},
            },
            "legacy_wire_schemas": {
                "stability": "wire",
                "module": "forge_doctor_data.core.schemas",
                "scan_schema_version": api.SCAN_SCHEMA_VERSION,
                "schema_version": api.SCHEMA_VERSION,
                "entries": {name: {"$id": s.get("$id", "")} for name, s in sorted(SCHEMAS.items())},
            },
            "mcp": {
                "stability": "wire",
                "module": "forge_doctor_data.integrations.mcp_server",
                "protocols": {
                    "modern": mcp_protocol.MODERN_VERSION,
                    "legacy": sorted(mcp_protocol.LEGACY_VERSIONS),
                    "default": mcp_protocol.DEFAULT_VERSION,
                },
                "entries": {t["name"]: {} for t in sorted(_TOOL_DEFS, key=lambda t: t["name"])},
            },
            "cli": {
                "stability": "ux",
                "module": "forge_doctor_data.cli",
                "entries": {
                    "groups": sorted(
                        g.name or g.typer_instance.info.name for g in app.registered_groups
                    ),
                    "commands": sorted(
                        c.name or c.callback.__name__ for c in app.registered_commands
                    ),
                },
            },
        },
    }


def main(argv: list[str]) -> int:
    rendered = json.dumps(collect_surface(), indent=2, sort_keys=True) + "\n"
    if "--check" in argv:
        current = OUT.read_text("utf-8") if OUT.is_file() else ""
        if current != rendered:
            print("docs/api-surface.json is stale - regenerate with tools/api_surface.py")
            return 1
        print("docs/api-surface.json up to date")
        return 0
    OUT.write_text(rendered, encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
