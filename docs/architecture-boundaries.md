# Bounded contexts and migration boundaries

The current module layout remains compatible while ownership becomes explicit:

```text
analysis/      semantic index, checks, findings
platform/      ontology, graph, capabilities, digital twin
runtime/       evidence, history, regression, incidents, reliability, capacity
decisions/     remediation, optimization, migration, experiments
governance/    policy, contracts, knowledge, plugins
estate/        workspace, fleet, portfolio
integrations/  MCP, LSP, collectors, exports
```

This is a dependency direction, not a blind mass rename. New code should add a
facade at the boundary, characterization tests before moving a module, and no
imports from CLI/renderers into analyzers or checks. `_v2` modules remain
compatibility facades until their consumers migrate; removal requires the
deprecation policy.

## Consolidated generational modules (P12)

The three `foo.py` / `foo_v2.py` pairs are now packages whose submodules
name the *concept*, not the generation:

```text
core/experiments/    fixture.py (transform-diff engine) + measured.py (bundle metrics)
core/migration/      platform.py (same-platform plans) + cross_platform.py (concepts)
core/optimization/   static.py (finding/graph candidates) + evidence.py (guardrailed opportunities)
```

`experiments_v2`, `migration_v2`, `optimize`, and `optimize_v2` survive
as thin re-export facades for external consumers; all internal imports
use the canonical package paths. Removing a facade follows
`docs/deprecation.md`.
