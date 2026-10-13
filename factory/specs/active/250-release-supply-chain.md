---
id: 250
title: Release & Supply Chain — security gate, verified release, SBOM
agent: claude
risk: high
verification:
  - python -m pytest tests/ -x -q
  - ruff check src tests && ruff format --check src tests && mypy
---

# Program V1 - Phase 3: Release & Supply Chain (prompt_evo_step10 §22-24, P18-P20)

## Context

A publishable product needs provenance: security policy, dependency
automation, verified release pipeline, deterministic SBOM.

## Problem

- No SECURITY.md / CODEOWNERS / dependabot / security workflow.
- Release did not verify tag==version, install the built wheel, or emit
  an SBOM; SBOM contained a volatile timestamp (non-reproducible).

## Objectives

- SECURITY.md, CODEOWNERS, dependabot.yml, `security.yml` workflow
  (workflow policy check + pip-audit).
- `tools/verify_release.py`: tag/version/artifact agreement; release
  pipeline runs it, installs the wheel, runs `doctor`, emits SBOM.
- CycloneDX output byte-stable (timestamp removed).

## Non-Objectives

- PyPI Trusted Publishing wiring (needs repo-level OIDC admin); the
  publisher remains a documented manual gate.

## Compatibility

- SBOM drops `metadata.timestamp` — documented; serial remains stable.

## Tests

- `test_sbom_is_deterministic`; release verify against `dist/`.
