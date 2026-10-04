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
