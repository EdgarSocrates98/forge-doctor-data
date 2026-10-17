# PyPI patch plan — forge-doctor-data

Cycle 11.2 (P1-004 + P1-006). Prepared for maintainer approval; nothing here
publishes, tags or uploads anything.

## Current state (audited in cycle 11.2)

| Signal | Value |
|---|---|
| PyPI published | `forge-doctor-data 1.0.0` (only release) |
| `pyproject.toml` | `1.0.0` — aligned |
| Git tag / GitHub release | `v1.0.0` — aligned |
| `requires-python` | `>=3.11` |
| CI matrix (`ci.yml`, `unit-tests`) | 3.11 / 3.12 / 3.13 — complete per audit |
| Classifiers | 3.11 / 3.12 / 3.13 (+ generic `Python :: 3`) — coherent |
| License metadata | `license = "MIT"` → PyPI already shows `License-Expression: MIT` ✓ |
| Published `project_urls` | only `Changelog`, `Repository` — the 1.0.0 wheel predates the full `[project.urls]` block (Homepage/Documentation/Issues now declared) |

**No version drift**: PyPI = pyproject = tag = GitHub release.

## What changes in this PR

Nothing in `pyproject.toml` was broken — metadata is already coherent:
SPDX license, classifiers matching the tested range, complete
`[project.urls]`, all referenced files (`CHANGELOG.md`,
`docs/architecture.md`) present. This PR adds only this plan.

The **published** metadata gap (PyPI page missing Homepage/Documentation/
Issues URLs) self-corrects on the next upload — no code change needed.

Not changed: version, CI matrix (no gap; 3.14 is inside `>=3.11` but
untested — candidate for a future cycle alongside siblings).

## Proposed next release: `1.0.1` (patch)

Only needed when an actual change lands — currently there is nothing to
republish for. If the maintainer cuts a patch for any reason, this is the
checklist:

### Provenance checklist for the maintainer

- [ ] `poetry run pytest -q` (or `python -m pytest -q`), `ruff check .`,
      `mypy`, `poetry run python tools/verify_release.py --dist dist`.
- [ ] Bump `version = "1.0.1"` in `pyproject.toml` at release time.
- [ ] Tag `v1.0.1` after merge; publish via `publish-pypi.yml` /
      `release.yml`.
- [ ] Verify PyPI `project_urls` now shows Homepage/Documentation/Issues.

## Local smoke evidence (this PR)

- Interpreters: system `python3.12` (3.12.3); uv-managed 3.11.16, 3.13.15,
  3.14.7.
- Wheel builds via `poetry-core`; `forge-doctor-data --help` smoke OK.

## Blockers

None.
