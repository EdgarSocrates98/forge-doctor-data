---
id: 256
title: Real-World Validation — versioned OSS corpus
agent: claude
risk: medium
verification:
  - python -m pytest tests/ -x -q
  - ruff check src tests && ruff format --check src tests && mypy
---

# Program V1 - Phase 9: Real-World Validation (prompt_evo_step10 §10.4, P6)

## Context

Fixtures prove intent; real projects prove the engine works on
structures it did not author.

## Problem

No versioned corpus of real OSS project shapes; risk of overfitting
detectors to synthetic labs.

## Objectives

- Corpus manifest pinning real projects by URL+commit (vendored slices,
  not network fetch at test time).
- Corpus scan produces recorded expected findings — drift is a diff.

## Non-Objectives

- Crawling arbitrary repos in CI; corpus is versioned and minimal.

## Compatibility

- Test corpus only.

## Tests

- Corpus scan snapshot stable; documented review path for updates.
