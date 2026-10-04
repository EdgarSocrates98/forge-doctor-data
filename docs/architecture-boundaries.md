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
