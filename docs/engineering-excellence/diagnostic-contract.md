# Engineering Excellence — Doctor Data Diagnostics

## Boundary

Doctor Data owns data/streaming diagnosis across SQL, HCL, JS, graph, context, evals, golden fixtures and runtime analyzers. It publishes findings and evidence; it does not become generic router.

## Reproducibility contract

Finding must identify:

- input fixture, digest and dialect;
- analyzer, rule and version;
- command, environment and bounded context;
- location, severity and expected invariant;
- evidence refs, confidence, limitation and next action;
- graph/context refs when dependency impact is known.

Golden/eval result proves covered fixture only. Missing context never becomes a passing assumption.

## Federation

The Forge consumes descriptor and receipt references. Local SQL/HCL/JS rule authority stays here. Mutation requires explicit downstream owner and policy; diagnostics default read-only.

## Verification

```text
python -m pytest tests -q
python -m ruff check .
```

Targeted suites: analyzers, graph/context, evals, golden fixtures and benchmark tools.

## Pending

- Publish diagnostic descriptor with language/dialect dimensions.
- Add receipt schema for cross-file graph evidence.
- Add benchmark baseline for one streaming, SQL and infrastructure case.
