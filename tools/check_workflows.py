"""Small, offline workflow policy check used by the security gate."""

from __future__ import annotations

import re
import sys
from pathlib import Path

USES_RE = re.compile(r"^\s*-\s*uses:\s*([^\s#]+)")
ALLOWED_TAGS = {"actions/checkout@v4", "actions/setup-python@v5"}


def main() -> int:
    violations: list[str] = []
    for path in sorted(Path(".github/workflows").glob("*.y*ml")):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            match = USES_RE.match(line)
            if not match:
                continue
            ref = match.group(1)
            if "@" not in ref:
                violations.append(f"{path}:{lineno}: action reference missing @ref")
                continue
            owner_action, action_ref = ref.rsplit("@", 1)
            if len(action_ref) != 40 and ref not in ALLOWED_TAGS:
                violations.append(
                    f"{path}:{lineno}: {owner_action} uses mutable ref {action_ref!r}; pin SHA"
                )
    if violations:
        print("workflow policy findings:", file=sys.stderr)
        print("\n".join(violations), file=sys.stderr)
        return 1
    print("workflow policy clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
