---
id: 276
title: MCP Boundary Hardening
agent: claude
risk: high
status: accepted
commit: deb7307
verification:
  - python -m pytest tests/unit/test_mcp_boundary.py tests/unit/test_mcp_*.py -x -q
---

# RC Hardening Program (prompt_evo_rc_hardening)

53-test boundary suite; fixes: path-arg confinement for changes/manifest, strict URI segment validation, -32602 normalization, params/arguments shape guards, deep-JSON loop resilience.

## Evidence

- `tests/unit/test_mcp_boundary.py`
- `src/forge_doctor_data/integrations/mcp_server.py`
- `src/forge_doctor_data/core/knowledge.py`
- `docs/mcp.md`

## Acceptance Criteria

- Delivered per the program phase; verification commands above pass.
- Claims bounded by proof artifacts (claim-to-evidence rule).
