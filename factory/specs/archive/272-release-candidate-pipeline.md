---
id: 272
title: Release-Candidate Pipeline — SBOM, SHA256SUMS, manifest, provenance
agent: claude
risk: high
verification:
  - python tools/release_candidate.py
  - python -m pytest tests/unit/test_release_candidate.py -x -q
---

# Consolidation Wave — Phase H (prompt_evo_consolidacao1 §Phase H)

A release candidate must be reproducible: same commit in, same
artifact set + hashes out. Provenance is generated, not asserted.

## Acceptance Criteria

- `tools/release_candidate.py` dry-run produces the full artifact set
  in `dist/`:
  - `SHA256SUMS` (sorted, deterministic format)
  - `SBOM` (CycloneDX-style dependency manifest)
  - release `manifest.json` (version, artifacts, digests, sizes,
    deterministic; honors `SOURCE_DATE_EPOCH`)
  - exported contract + legacy wire schemas
  - provenance subjects matching artifacts 1:1
- Refuses empty `dist/` and version-mismatched artifacts (caught a
  real stale-0.7.0 case during development).
- `release.yml` wired to produce the artifact set; PyPI job stays
  `if: false` until maintainer enables Trusted Publishing.
- Deterministic: manifest byte-identical for same inputs.

## Evidence

- Commit `d221329` — pipeline tool, tests, release-workflow wiring.
