# Deprecation policy

Deprecations are explicit, documented, and reversible within a major line.

| Surface | Notice | Removal |
|---|---|---|
| CLI command or flag | warning in the next minor release | next major release at earliest |
| Python API name or argument | `DeprecationWarning` plus docs entry | next major release at earliest |
| JSON field or enum value | additive replacement and schema note | major contract version |
| Plugin SDK member | compatibility note and migration example | next major SDK version |
| MCP method or protocol | legacy adapter remains available | after announced major boundary |

Rules:

- Never remove a public command, field, check id, or plugin member silently.
- Keep old and new forms working during the warning window when feasible.
- Record replacement, first deprecated version, removal target, and migration
  example in the changelog and relevant contract document.
- Unknown and unsupported states remain explicit; deprecation never changes an
  evidence value silently.
