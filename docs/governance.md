# Repository governance — `main` is protected

`main` is not a free branch. Every change arrives through a pull request
with green required checks; nothing merges straight to `main`.

## Required branch ruleset

Configure a GitHub Ruleset (Settings → Rules → New ruleset → *New branch
ruleset*, target: `main`, enforcement: **Active**) with:

| Setting | Value |
|---|---|
| Require a pull request before merging | on |
| Required approvals | 1 |
| Dismiss stale reviews on new commits | on |
| Require conversation resolution | on |
| Require status checks to pass | on |
| Require branches to be up to date | on |
| Block force pushes | on |
| Restrict deletions | on |
| Bypass list | empty (no bypass actors) |

### Required status checks

These job `name:` values are **stable identifiers** — they are part of
the repository contract and must not be renamed without updating this
document and the ruleset in the same change:

| Check name | Workflow / job |
|---|---|
| `static-analysis` | ci.yml / ruff + format + mypy |
| `unit-tests-3.11` | ci.yml / matrix |
| `unit-tests-3.12` | ci.yml / matrix |
| `unit-tests-3.13` | ci.yml / matrix |
| `package-build` | ci.yml / wheel + sdist + inspection |
| `platform-smoke-ubuntu-latest` | ci.yml / wheel install + CLI smoke |
| `platform-smoke-windows-latest` | ci.yml / wheel install + CLI smoke |
| `platform-smoke-macos-latest` | ci.yml / wheel install + CLI smoke |
| `forge-gates` | ci.yml / contracts, doc drift, knowledge, lab, golden |
| `dependency-audit` | security.yml / pip-audit (scheduled + PRs) |
| `workflow-hygiene` | security.yml / workflow policy checks |

Optional (do not require): `extras smoke (watch/lsp/schemas)` and
`dogfood (this repo, local action)` — they validate optional surfaces
and are allowed to be advisory.

### Applying via CLI

```bash
gh api repos/{owner}/{repo}/rulesets -X POST -f name=main-protection \
  -f target=branch -f enforcement=active \
  --input ruleset.json
```

with `ruleset.json` containing `ref_name` condition `refs/heads/main`,
`pull_request`, `required_status_checks` (the table above, strict
mode), `non_fast_forward`, and `deletion` rules. Keep the JSON under
review like any other repository contract.

## Merge hygiene

- Squash-merge by default; keep commit titles imperative and scoped.
- A merge is only green when *every* required check above is green —
  "most of CI passed" is a red state.
- CI job renames are breaking changes to this contract; rename a job
  name only together with a ruleset update in the same PR.

## Release authority

- Tags `v*` are created only by maintainers and only after the
  `docs/release.md` pre-flight checklist is green.
- Publishing uses the release workflow's trusted-publishing OIDC path;
  no long-lived PyPI tokens live in repository secrets.
