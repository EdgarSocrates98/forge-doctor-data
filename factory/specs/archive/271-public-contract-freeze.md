---
id: 271
title: Public Contract Freeze — stability classes, SDK inventory, pinned surface
agent: claude
risk: high
verification:
  - python tools/api_surface.py --check
  - python -m pytest tests/unit/test_public_api_freeze.py -x -q
---

# Consolidation Wave — Phase G (prompt_evo_consolidacao1 §Phase G)

v1.0 means downstream tools can program against a frozen surface. The
inventory is machine-readable; any addition, removal, or signature
change is a reviewable diff — never silent drift.

## Acceptance Criteria

- `tools/api_surface.py` emits the full inventory: Python API
  (`api.__all__` + signatures), plugin SDK, contracts vocabulary,
  contracts schemas + fixtures, MCP tools + protocol versions, CLI
  command tree, legacy wire schema versions.
- Every surface carries a declared stability class
  (stable/frozen/legacy/internal).
- `docs/api-surface.json` is the recorded freeze;
  `api_surface.py --check` + `test_public_api_freeze.py` gate drift.
- MCP surface explicit: 13 tools pinned, modern + legacy protocol
  versions recorded.
- `docs/api.md` stability rules + `docs/deprecation.md` deprecation
  policy for post-1.0 evolution.

## Evidence

- Commit `d7deed3` — freeze inventory, stability classes, pinned test.
