---
id: 275
title: Real OSS Corpus Expansion
agent: claude
risk: high
status: accepted
commit: dbe3084
verification:
  - forge-doctor-data golden run
  - python tools/golden_metrics.py --check
  - python -m pytest tests/unit/test_corpus_manifest.py tests/unit/test_corpus_ground_truth.py tests/unit/test_golden_metrics.py -x -q
---

# RC Hardening Program (prompt_evo_rc_hardening)

7 new vendored real-oss slices (10 real total) at pinned SHAs + LICENSE + per-file sha256; per-domain P/R; 2 real-FP engine fixes (ICE012 nested catalog keys, SRCH004 var-default resolution).

## Evidence

- `golden/repos/*`
- `golden/manifest.json`
- `golden/metrics.json`
- `tools/vendor_real_slice.py`
- `tools/golden_metrics.py`
- `tests/unit/test_corpus_manifest.py`
- `tests/unit/test_corpus_ground_truth.py`
- `docs/corpus.md`
- `src/forge_doctor_data/analyzers/iceberg_model.py`
- `src/forge_doctor_data/analyzers/search_model.py`
- `src/forge_doctor_data/checks/search.py`

## Acceptance Criteria

- Delivered per the program phase; verification commands above pass.
- Claims bounded by proof artifacts (claim-to-evidence rule).
