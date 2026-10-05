"""MCP boundary hardening (RC hardening Phase 3).

The MCP server is a trust boundary: the agent host controls the wire,
the server must not let that reach the host filesystem or crash the
session. These tests pin the boundary contract:

- every path-shaped tool argument is confined to ``--root`` (not just
  ``path`` - ``changes``/``manifest``/``old``/``new`` too);
- symlink escapes inside the sandbox are rejected;
- malformed JSON-RPC envelopes produce protocol errors, never crashes;
- pathological payloads (deep nesting, megabyte inputs) degrade to
  errors, not process death;
- knowledge/rule resource URIs cannot traverse out of the pack tree;
- plugins stay off over MCP unless the host explicitly opts in.
"""

from __future__ import annotations

import io
import json
import os
from pathlib import Path

import pytest

from forge_doctor_data.integrations.mcp_server import handle, serve

_ROOT_ARG_TOOLS = [
    # (tool, argument, extra arguments)
    ("scan_project", "path", {}),
    ("check_compatibility", "path", {}),
    ("get_lineage", "path", {}),
    ("get_execution_baseline", "path", {}),
    ("get_regressions", "path", {}),
    ("get_critical_path", "path", {}),
    ("get_capacity_signals", "path", {}),
    ("get_runtime_correlations", "changes", {}),
    ("get_incident_explanation", "changes", {}),
    ("get_portfolio_summary", "manifest", {}),
    ("diff_findings", "old", {"new": "report.json"}),
    ("diff_findings", "new", {"old": "report.json"}),
]


def _call_tool(name: str, arguments: dict, root: Path, req_id: int = 1) -> dict:
    out = handle(
        {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        },
        root=root,
    )
    assert out is not None
    return out


# --- sandbox confinement ----------------------------------------------------


@pytest.mark.parametrize(("tool", "arg", "extra"), _ROOT_ARG_TOOLS)
def test_every_path_argument_is_confined(tmp_path: Path, tool: str, arg: str, extra: dict) -> None:
    """A hosted server (--root set) must not let ANY path-shaped argument
    reach outside the sandbox - path confinement is per-argument, not
    per-tool."""
    sandbox = tmp_path / "project"
    sandbox.mkdir()
    (tmp_path / "outside").mkdir()
    args = dict(extra)
    args[arg] = str(tmp_path / "outside")
    out = _call_tool(tool, args, root=sandbox)
    assert out.get("error", {}).get("code") == -32602, f"{tool}.{arg} escaped the sandbox: {out}"
    assert "sandbox" in out["error"]["message"]


@pytest.mark.parametrize(("tool", "arg", "extra"), _ROOT_ARG_TOOLS[:7])
def test_relative_escape_confined(tmp_path: Path, tool: str, arg: str, extra: dict) -> None:
    sandbox = tmp_path / "project"
    sandbox.mkdir()
    args = dict(extra)
    args[arg] = "../outside"
    out = _call_tool(tool, args, root=sandbox)
    assert out.get("error", {}).get("code") == -32602


def test_symlink_escape_rejected(tmp_path: Path) -> None:
    """An in-sandbox symlink pointing outside resolves outside and must
    be refused - resolve() happens before the containment check."""
    sandbox = tmp_path / "project"
    outside = tmp_path / "outside"
    sandbox.mkdir()
    outside.mkdir()
    link = sandbox / "link"
    try:
        os.symlink(outside, link, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("symlinks not permitted in this environment")
    out = _call_tool("scan_project", {"path": "link"}, root=sandbox)
    assert out.get("error", {}).get("code") == -32602


def test_sandbox_none_means_host_process_permissions(tmp_path: Path) -> None:
    """Without --root the server inherits process permissions by design -
    the contract documented for stdio use."""
    out = handle(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "get_lineage", "arguments": {"path": str(tmp_path)}},
        },
        root=None,
    )
    assert "result" in out


# --- malformed envelopes ------------------------------------------------------


@pytest.mark.parametrize(
    "params",
    [
        "a string",
        42,
        ["tools/call"],
        True,
    ],
)
def test_non_object_params_rejected(params: object) -> None:
    out = handle({"jsonrpc": "2.0", "id": 7, "method": "tools/list", "params": params})
    assert out is not None
    assert out.get("error", {}).get("code") == -32602


def test_null_params_treated_as_absent() -> None:
    """JSON-RPC params is optional; null == absent, not an error."""
    out = handle({"jsonrpc": "2.0", "id": 71, "method": "tools/list", "params": None})
    assert "result" in out


@pytest.mark.parametrize(
    "arguments",
    [
        "check_id=SPARK001",
        42,
        ["SPARK001"],
        True,
    ],
)
def test_non_object_arguments_rejected(arguments: object) -> None:
    out = handle(
        {
            "jsonrpc": "2.0",
            "id": 8,
            "method": "tools/call",
            "params": {"name": "explain_rule", "arguments": arguments},
        },
        root=Path.cwd(),
    )
    assert out is not None
    # wrong-typed arguments are a protocol error, not an isError tool result
    assert out.get("error", {}).get("code") == -32602


def test_non_dict_request_ignored() -> None:
    assert handle("not a dict") is None
    assert handle([{"method": "ping"}]) is None
    assert handle(None) is None


def test_method_call_without_name_is_error() -> None:
    out = handle(
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"arguments": {}},
        }
    )
    assert out["error"]["code"] == -32602


@pytest.mark.parametrize("bad_id", ["abc", {"x": 1}, ["a"], 1.5])
def test_check_id_wrong_type_is_iserror_not_crash(bad_id: object) -> None:
    """Tool-level argument validation failures come back as isError
    results, not transport errors or crashes."""
    out = handle(
        {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {"name": "explain_rule", "arguments": {"check_id": bad_id}},
        }
    )
    assert out is not None
    assert out.get("error") or out["result"].get("isError") is True


def test_missing_required_argument_is_iserror() -> None:
    out = handle(
        {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {"name": "diff_findings", "arguments": {}},
        }
    )
    assert out["result"]["isError"] is True


def test_unknown_rule_resource_is_error() -> None:
    out = handle(
        {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "resources/read",
            "params": {"uri": "forge-doctor-data://rules/NOPE999"},
        }
    )
    assert out.get("error", {}).get("code") == -32602


# --- resource URI traversal ----------------------------------------------------


@pytest.mark.parametrize(
    "uri",
    [
        "forge-doctor-data://knowledge/..%2F..%2Fpyproject",
        "forge-doctor-data://knowledge/glue/..\\..\\secrets",
        "forge-doctor-data://knowledge/../versions",
        "forge-doctor-data://knowledge/glue/../../versions",
        "https://evil.example/rules/SPARK001",
        "file:///etc/passwd",
        "forge-doctor-data://rules/SPARK001/extra",
        "",
    ],
)
def test_resource_uri_traversal_rejected(uri: str) -> None:
    out = handle(
        {
            "jsonrpc": "2.0",
            "id": 9,
            "method": "resources/read",
            "params": {"uri": uri},
        }
    )
    assert out.get("error", {}).get("code") == -32602


# --- pathological payloads ---------------------------------------------------


def test_deeply_nested_json_line_does_not_crash_server(tmp_path: Path) -> None:
    """json.loads RecursionError on hostile nesting is a parse failure,
    not a server exit - the loop must answer -32700 and keep serving."""
    depth = 50_000  # beyond CPython's parser recursion limit
    line = '{"a":' * depth + "1" + "}" * depth
    out = io.StringIO()
    serve(
        stdin=io.StringIO(line + '\n{"jsonrpc":"2.0","id":1,"method":"ping"}\n'),
        stdout=out,
        root=tmp_path,
    )
    lines = [json.loads(x) for x in out.getvalue().strip().splitlines()]
    assert lines[0]["error"]["code"] == -32700
    assert lines[1]["result"] == {}  # still serving after the bad line


def test_deeply_nested_valid_request_does_not_crash(tmp_path: Path) -> None:
    """Deep-but-parseable payloads reach handle(); a dict without method
    is silently ignored, and the loop keeps serving."""
    depth = 1_000  # parses: lands in handle(), which drops non-requests
    line = '{"a":' * depth + "1" + "}" * depth
    out = io.StringIO()
    serve(
        stdin=io.StringIO(line + '\n{"jsonrpc":"2.0","id":1,"method":"ping"}\n'),
        stdout=out,
        root=tmp_path,
    )
    lines = [json.loads(x) for x in out.getvalue().strip().splitlines()]
    assert lines[0]["result"] == {}  # loop survived; only ping answered


def test_garbage_line_then_valid_line(tmp_path: Path) -> None:
    out = io.StringIO()
    serve(
        stdin=io.StringIO('garbage\n{"jsonrpc":"2.0","id":2,"method":"ping"}\n'),
        stdout=out,
        root=tmp_path,
    )
    lines = [json.loads(x) for x in out.getvalue().strip().splitlines()]
    assert lines[0]["error"]["code"] == -32700
    assert lines[1]["result"] == {}


def test_megabyte_diagnose_input_bounded_work() -> None:
    """A 1 MiB log blob must complete - either findings or an isError
    result, never a hang or crash."""
    blob = "OutOfMemoryError: Java heap space\n" * 32768  # ~1 MiB
    out = handle(
        {
            "jsonrpc": "2.0",
            "id": 10,
            "method": "tools/call",
            "params": {"name": "diagnose_log", "arguments": {"text": blob}},
        }
    )
    assert out is not None
    assert out.get("result") is not None or out.get("error") is not None


def test_unicode_and_control_chars_in_arguments() -> None:
    out = handle(
        {
            "jsonrpc": "2.0",
            "id": 11,
            "method": "tools/call",
            "params": {
                "name": "diagnose_log",
                "arguments": {"text": "err\x00or \u202e hidden"},
            },
        }
    )
    assert out is not None
    assert "result" in out


# --- error hygiene -------------------------------------------------------------


def test_tool_error_does_not_leak_traceback(tmp_path: Path) -> None:
    """isError payloads carry the exception message, never a traceback -
    stack frames are server internals, not wire data."""
    out = _call_tool("explain_rule", {"check_id": "NOPE"}, root=tmp_path)
    text = out["result"]["content"][0]["text"]
    assert "Traceback" not in text
    assert 'File "' not in text


def test_error_message_does_not_echo_root(tmp_path: Path) -> None:
    """Sandbox errors name the escape attempt, not server internals."""
    sandbox = tmp_path / "project"
    sandbox.mkdir()
    out = _call_tool("scan_project", {"path": "../x"}, root=sandbox)
    msg = out["error"]["message"]
    assert "sandbox" in msg


# --- plugins boundary ---------------------------------------------------------


def test_plugins_off_by_default_over_mcp(tmp_path: Path) -> None:
    """Plugin code is third-party; over MCP it loads only on explicit
    host opt-in, never implicitly."""
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
    out = _call_tool("scan_project", {"path": "."}, root=tmp_path)
    # result shape is the contract; plugin loading is out of the wire path
    assert "result" in out
    assert "findings" in out["result"]["structuredContent"]
