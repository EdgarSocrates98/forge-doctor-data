# Plugin process isolation

Trusted in-process execution remains the default. Projects that need crash and
output containment can opt into subprocess execution:

```toml
[tool.forge-doctor-data.plugins]
execution = "isolated"
timeout_seconds = 30
max_output_bytes = 1000000
```

The child process uses a structured JSON protocol, applies the timeout and
stdout limit, and returns findings to the normal runner. This is process
isolation, not a complete security sandbox; run untrusted plugins with OS-level
least privilege and filesystem/network restrictions.

## Trust contract (pinned by tests)

Three proofs from `tests/unit/test_plugin_conformance_proofs.py`:

- **No import-before-trust** — `discovery._ep_trusted` gates every
  entry point *before* `ep.load()`; the isolated worker
  (`plugins/isolation.py`) documents that it re-verifies nothing —
  callers pass only pre-gated names. The AST check asserts every
  engine-side `ep.load()` sits inside a trust decision.
- **No filesystem mutation during conformance** — `plugins
  list|doctor|validate` leave the project tree byte-identical.
- **No network use during conformance** — AST scan of `plugins/`:
  discovery, manager, protocol, and isolation import no socket module.

`tests/unit/test_plugin_boundary.py` pins the hostile-plugin contract:

- **Same gate for both modes** — `execution = "isolated"` consults
  `_ep_trusted` before any worker is spawned; untrusted code never
  reaches a child process either.
- **No id shadowing** — a plugin check claiming a built-in id is
  rejected by the registry (duplicate → `plugin_errors`); the built-in
  always wins and the scan completes.
- **Crash containment** — a check raising inside `run()` becomes an
  internal-error finding; a check breaching the return contract
  (non-`CheckResult` items) degrades the same way instead of crashing
  the runner.
- **Bounded children** — `max_output_bytes` applies *while* stdout and
  stderr stream (not after they are fully buffered), the draining
  threads keep reading so the child never deadlocks on a full pipe,
  and `timeout_seconds` kills the child. Malformed worker output is a
  protocol error, not a crash.
- **Result sanitization** — isolated describe rows must carry a
  non-empty string `id` to be proxied; finding `file` claims outside
  the scanned root are dropped (the finding survives, the escape
  does not).

