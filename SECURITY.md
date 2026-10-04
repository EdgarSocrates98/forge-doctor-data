# Security policy

Forge Doctor Data is an offline-first diagnostic engine. `scan` must not make
network or cloud calls, execute analyzed project code, or print secret values.

## Reporting a vulnerability

Do not open a public issue for an exploitable vulnerability. Send a private
report to the repository maintainer through GitHub Security Advisories with:

- affected version or commit;
- minimal reproduction;
- impact and prerequisites;
- proposed mitigation when available.

The maintainer acknowledges reports within 5 business days and coordinates a
fix, disclosure date, and release note with the reporter.

## Scope

Reports involving target-code execution, secret disclosure, path escape,
plugin trust-boundary bypass, dependency supply chain, or release workflow
integrity receive priority. Findings in intentionally vulnerable `labs/`
fixtures are test data, not product vulnerabilities.

## Plugin trust

Trusted plugins execute in-process. Isolated plugin execution is process
isolation, not a complete security sandbox. Run untrusted plugins in a
separate OS-level sandbox with least privilege.
