"""MCP protocol-version adapters (P7).

The server speaks one canonical result internally; the adapter chosen
during ``initialize`` shapes what older clients see, so legacy clients
keep working while modern ones get the current wire surface:

- ``tool_annotations`` — ``annotations.readOnlyHint`` on ``tools/list``
  entries (arrived in spec 2025-03-26).
- ``tool_titles`` + ``structured_content`` — ``title`` on tools and
  ``structuredContent`` on ``tools/call`` results (2025-06-18+).
- modern clients additionally get ``instructions`` in ``initialize``.

Versions are negotiated, never silently dropped: an unsupported request
gets the newest supported version back and the client decides.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

LEGACY_VERSIONS = ("2024-11-05", "2025-03-26", "2025-06-18")
MODERN_VERSION = "2025-11-25"
SUPPORTED_PROTOCOLS = (*LEGACY_VERSIONS, MODERN_VERSION)
# What the server falls back to when the client asks for something unknown.
DEFAULT_VERSION = MODERN_VERSION

_INSTRUCTIONS = (
    "Read-only diagnostics server. Call tools/list, then tools/call with "
    "tool names and argument objects; filesystem paths are confined to the "
    "server's --root when one is configured."
)


@dataclass(frozen=True)
class ProtocolAdapter:
    """Wire-shape decisions for one negotiated protocol version."""

    version: str
    tier: str  # "legacy" | "modern"
    tool_annotations: bool = False
    tool_titles: bool = False
    structured_content: bool = False
    instructions: bool = False


_FEATURES: dict[str, dict[str, Any]] = {
    "2024-11-05": {},
    "2025-03-26": {"tool_annotations": True},
    "2025-06-18": {
        "tool_annotations": True,
        "tool_titles": True,
        "structured_content": True,
    },
    MODERN_VERSION: {
        "tool_annotations": True,
        "tool_titles": True,
        "structured_content": True,
        "instructions": True,
    },
}

_ADAPTERS = {
    version: ProtocolAdapter(
        version=version,
        tier="legacy" if version in LEGACY_VERSIONS else "modern",
        **features,
    )
    for version, features in _FEATURES.items()
}

DEFAULT_ADAPTER = _ADAPTERS[DEFAULT_VERSION]


def adapter_for(version: str) -> ProtocolAdapter:
    return _ADAPTERS[version]


def negotiate(client_version: str) -> ProtocolAdapter:
    """Echo the client's version when supported, else offer our newest."""
    return _ADAPTERS.get(client_version, DEFAULT_ADAPTER)


def tool_defs(base_defs: list[dict[str, Any]], adapter: ProtocolAdapter) -> list[dict[str, Any]]:
    """``tools/list`` shaped for the negotiated version."""
    defs: list[dict[str, Any]] = []
    for tool in base_defs:
        entry = dict(tool)
        if adapter.tool_titles:
            entry["title"] = tool["name"].replace("_", " ").title()
        if adapter.tool_annotations:
            entry["annotations"] = {
                "readOnlyHint": True,
                "destructiveHint": False,
                "openWorldHint": False,
            }
        defs.append(entry)
    return defs


def tool_result(output: Any, adapter: ProtocolAdapter) -> dict[str, Any]:
    """``tools/call`` result shaped for the negotiated version."""
    import json

    result: dict[str, Any] = {
        "content": [
            {
                "type": "text",
                "text": json.dumps(output, indent=2, ensure_ascii=False),
            }
        ],
    }
    if adapter.structured_content:
        result["structuredContent"] = output
    return result


def initialize_result(adapter: ProtocolAdapter, server_name: str, version: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "protocolVersion": adapter.version,
        "capabilities": {"tools": {"listChanged": False}, "resources": {"listChanged": False}},
        "serverInfo": {"name": server_name, "version": version},
    }
    if adapter.instructions:
        result["instructions"] = _INSTRUCTIONS
    return result
