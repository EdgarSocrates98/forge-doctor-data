# Agent context protocol

Forge Doctor Data remains a deterministic sensor. The `agent` commands project
existing scan and graph evidence into compact, lazy payloads; no LLM or remote
service runs inside the package.

```bash
forge-doctor-data agent manifest .
forge-doctor-data agent context . --budget 8000
forge-doctor-data agent delta . --since previous-context.json
forge-doctor-data agent evidence finding:<fingerprint> .
forge-doctor-data agent evidence entity:<entity-id> .
```

The manifest contains `domains`, entity references, risk references,
capability states, and lazy `evidence_refs`. Context adds detail only while an
approximate `budget * 4` character ceiling permits it, preserving summary
fields and marking truncation. Delta compares stable finding fingerprints; it
does not compare message text or line numbers.

Payload contract: `agent-context@1`. Consumers should treat unknown or absent
evidence as unknown, not as a negative assertion.
