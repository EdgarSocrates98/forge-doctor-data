---
id: 281
title: RC Pipeline Finalization
agent: claude
risk: high
status: accepted
commit: f94f161
verification:
  - python tools/release_candidate.py --allow-dirty
  - python tools/schema_freeze.py --check
  - python -m pytest tests/unit/test_release_candidate.py tests/unit/test_schema_freeze.py -x -q
---

# RC Hardening Program (prompt_evo_rc_hardening)

Dirty-tree refusal + --allow-dirty, wheel+sdist requirement, SDE from HEAD, digest re-verify; schema-freeze gate with approval trail wired into CI.

## Evidence

- `tools/release_candidate.py`
- `tools/schema_freeze.py`
- `docs/schema-freeze.json`
- `tests/unit/test_release_candidate.py`
- `tests/unit/test_schema_freeze.py`
- `.github/workflows/ci.yml`
- `docs/release.md`

## Acceptance Criteria

- Delivered per the program phase; verification commands above pass.
- Claims bounded by proof artifacts (claim-to-evidence rule).
