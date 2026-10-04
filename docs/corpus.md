# Validation corpus

`golden/` is the versioned regression corpus. `golden/manifest.json` is
the index: each entry vendors a repo slice under `<name>/repo/` and its
expected outputs under `<name>/expected/`.

## Provenance contract

Every manifest entry records:

- `origin` — `synthetic` (authored in-repo) or `real` (vendored from an
  upstream project);
- `url`, `commit`, `license` — required for `real` entries, `null` for
  synthetic ones;
- `shape` — one line describing the workload shape the slice covers.

Entries are vendored slices, never fetched at test time. A `real` entry
without `url`+`commit` is a manifest error, not a documentation gap.

## Review path for updates

1. Vendor the slice into `golden/<name>/repo/` (minimal files that keep
   the workload shape; strip secrets and large binaries).
2. Regenerate expected outputs via the golden update path
   (`core.golden.update_golden`) and review the diff like a code change.
3. Update the manifest entry — for `real` origins record the exact
   upstream commit and license.
4. Drift in expected findings is a reviewable diff, not a silent update.

## Current coverage

The corpus is currently synthetic-only: it proves the engine against
shapes we authored. Adding real OSS slices (dbt projects, Airflow
repos, Terraform data stacks) is the next increment — each must carry
upstream provenance in the manifest.
