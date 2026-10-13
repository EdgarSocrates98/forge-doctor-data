"""P7 conformance suite: legacy/modern protocol adapters + official SDK.

Wire payloads are validated against the official ``mcp.types`` models
(dev dependency only - the server itself stays zero-dependency), across
the full matrix of negotiated protocol versions:

- initialization / discovery for every supported version;
- tool listing shaped per adapter (annotations, titles);
- tool invocation (structuredContent only on 2025-06-18+);
- resources list/read;
- JSON-RPC errors, invalid params, sandbox path restrictions;
- backward compatibility (legacy clients get a usable surface).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from mcp import types as mcp_types

from forge_doctor_data.integrations.mcp_protocol import (
    DEFAULT_ADAPTER,
    DEFAULT_VERSION,
    LEGACY_VERSIONS,
    MODERN_VERSION,
    SUPPORTED_PROTOCOLS,
    adapter_for,
    negotiate,
)
from forge_doctor_data.integrations.mcp_server import _TOOL_DEFS, handle


def _call(
    method: str,
    params: dict | None = None,
    req_id: int = 1,
    adapter: Any = DEFAULT_ADAPTER,
    root: Path | None = None,
) -> dict:
    out = handle(
        {"jsonrpc": "2.0", "id": req_id, "method": method, "params": params or {}},
        root=root,
        adapter=adapter,
    )
    assert out is not None
    return out


@pytest.mark.parametrize("version", SUPPORTED_PROTOCOLS)
def test_initialize_result_matches_official_model(version: str) -> None:
    out = _call("initialize", {"protocolVersion": version})
    parsed = mcp_types.InitializeResult.model_validate(out["result"])
    assert parsed.protocolVersion == version
    assert parsed.serverInfo.name == "forge-doctor-data"


def test_unknown_version_negotiates_to_newest() -> None:
    adapter = negotiate("2099-01-01")
    assert adapter.version == DEFAULT_VERSION
    assert adapter.tier == "modern"


def test_supported_matrix_legacy_vs_modern() -> None:
    assert set(LEGACY_VERSIONS) | {MODERN_VERSION} == set(SUPPORTED_PROTOCOLS)
    for version in LEGACY_VERSIONS:
        assert adapter_for(version).tier == "legacy"
    assert adapter_for(MODERN_VERSION).tier == "modern"


@pytest.mark.parametrize("version", SUPPORTED_PROTOCOLS)
def test_tools_list_conforms_to_official_schema(version: str) -> None:
    out = _call("tools/list", adapter=adapter_for(version))
    parsed = mcp_types.ListToolsResult.model_validate(out["result"])
    names = {t.name for t in parsed.tools}
    assert names == {t["name"] for t in _TOOL_DEFS}


@pytest.mark.parametrize("version", (*LEGACY_VERSIONS, MODERN_VERSION))
def test_tool_annotations_and_titles_by_version(version: str) -> None:
    out = _call("tools/list", adapter=adapter_for(version))
    tools = out["result"]["tools"]
    expect_meta = version != "2024-11-05"
    assert all(("annotations" in t) == expect_meta for t in tools)
    if expect_meta:
        assert all(t["annotations"]["readOnlyHint"] is True for t in tools)
    expect_titles = version in ("2025-06-18", MODERN_VERSION)
    assert all(("title" in t) == expect_titles for t in tools)


@pytest.mark.parametrize("version", SUPPORTED_PROTOCOLS)
def test_tool_call_result_shape_by_version(version: str, tmp_path: Path) -> None:
    (tmp_path / "a.py").write_text("x = 1\n", encoding="utf-8")
    out = _call(
        "tools/call",
        {"name": "explain_rule", "arguments": {"check_id": "SPARK001"}},
        adapter=adapter_for(version),
        root=tmp_path,
    )
    mcp_types.CallToolResult.model_validate(out["result"])
    expected = version in ("2025-06-18", MODERN_VERSION)
    assert ("structuredContent" in out["result"]) == expected


def test_legacy_client_gets_usable_surface(tmp_path: Path) -> None:
    """A 2024-11-05 client can list, call, and read resources end-to-end."""
    adapter = adapter_for("2024-11-05")
    init = _call("initialize", {"protocolVersion": "2024-11-05"}, adapter=adapter)
    assert init["result"]["protocolVersion"] == "2024-11-05"
    listed = _call("tools/list", adapter=adapter)
    tool = listed["result"]["tools"][0]
    assert "annotations" not in tool and "title" not in tool
    called = _call(
        "tools/call",
        {"name": "explain_rule", "arguments": {"check_id": "REP001"}},
        adapter=adapter,
        root=tmp_path,
    )
    assert called["result"]["content"][0]["type"] == "text"
    assert "structuredContent" not in called["result"]


def test_modern_client_gets_instructions_and_metadata() -> None:
    adapter = adapter_for(MODERN_VERSION)
    init = _call("initialize", {"protocolVersion": MODERN_VERSION}, adapter=adapter)
    assert "instructions" in init["result"]
    tool = _call("tools/list", adapter=adapter)["result"]["tools"][0]
    assert tool["title"] and tool["annotations"]["readOnlyHint"] is True


@pytest.mark.parametrize(
    ("method", "params", "code"),
    [
        ("tools/call", {"name": "no_such_tool", "arguments": {}}, -32602),
        ("resources/read", {"uri": "forge-doctor-data://bogus/x"}, -32602),
        ("nonsense/method", {}, -32601),
    ],
)
def test_error_codes_match_jsonrpc(method: str, params: dict, code: int) -> None:
    out = _call(method, params)
    assert out["error"]["code"] == code
    mcp_types.JSONRPCError.model_validate(out)


def test_sandbox_path_restriction(tmp_path: Path) -> None:
    (tmp_path / "inside").mkdir()
    out = _call(
        "tools/call",
        {"name": "scan_project", "arguments": {"path": "../escape"}},
        root=tmp_path,
    )
    assert out["error"]["code"] == -32602


def test_notifications_produce_no_response() -> None:
    assert handle({"jsonrpc": "2.0", "method": "notifications/initialized"}) is None


def test_parse_error_surface(tmp_path: Path) -> None:
    import io
    import json

    from forge_doctor_data.integrations.mcp_server import serve

    out = io.StringIO()
    serve(stdin=io.StringIO("not json\n"), stdout=out, root=tmp_path)
    line = out.getvalue().strip()
    assert json.loads(line)["error"]["code"] == -32700
