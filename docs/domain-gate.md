# Domain gate — no new domains without this checklist

The project's value is *depth per domain*, not the length of a feature
list. Before adding a new domain/integration (Cassandra, Dataproc,
Fivetran, Informatica, …) every question below must have a written,
evidence-backed answer in the proposal (issue or factory spec).

## The gate

1. **Is there real demand?**
   Link user reports, downstream-consumer requests, or deployment
   evidence. "It would be nice" is not demand.
2. **Can an existing abstraction represent it?**
   Check the capability/registry model first. If the domain's entities
   already map onto `database`, `queue`, `orchestrator`, `warehouse`,
   etc., prefer enriching the abstraction over adding a domain.
3. **Is there enough evidence to detect it reliably?**
   The engine is evidence-first: configs, IaC, schemas, logs, runtime
   exports. If the domain cannot be observed deterministically, it
   produces guesses, not findings — do not add it.
4. **Is there a test corpus?**
   At minimum one `labs/` scenario with `expected.json` ground truth,
   plus fixtures covering the domain's failure modes. No corpus, no
   domain.
5. **Is the maintainer cost acceptable?**
   Knowledge packs need freshness audits; checks need fixtures; docs
   need keeping current. State who maintains the domain and what the
   ongoing cost is.
6. **Does it improve the ecosystem, or only the list?**
   A new domain should unlock new *diagnostics* (correlations,
   regressions, remediations), not only new entity kinds.

## What a passing proposal looks like

- A factory spec in `factory/specs/inbox/` answering questions 1–6
  under a `## Domain gate` heading.
- Evidence adapters or collectors specified, not implied.
- The `docs/project-status.md` registries updated by the implementation
  (the CI doc-drift check enforces it).

## What happens when the gate fails

The spec stays in `inbox/` with the unanswered questions recorded. The
loop does not dispatch ungated domains — missing answers are product
decisions, and the factory automates implementation, not product
direction.
