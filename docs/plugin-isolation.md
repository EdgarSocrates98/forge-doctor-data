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

