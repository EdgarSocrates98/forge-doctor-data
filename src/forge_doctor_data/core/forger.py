"""The Forger boundary (spec 267/§5): request dict in, HandoffBundle out.

Doctor Data accepts a ``ForgeRequest``-shaped payload and returns a
``forge-contracts/1`` ``HandoffBundle``. It never routes, schedules, or
calls another Doctor - orchestration belongs to The Forger. This module
is the only place a request shape is accepted, so the boundary stays
explicit and testable::

    {"kind": "scan", "path": ".", "options": {"bounded": {"findings": 12}}}

``options.bounded`` maps onto ``HandoffBundle.bounded()`` - context
economy: The Forger asks for a summary-first bundle, the truncation is
recorded as honest ``UnknownFact`` entries, and the emission is stamped
with an ``x-forge-data`` extension block (the extension mechanism doing
real work, not decoration).
"""

from __future__ import annotations

from typing import Any

from forge_doctor_data.contracts import HandoffBundle

REQUEST_KINDS = ("scan",)


class ForgerRequestError(ValueError):
    """Malformed or unsupported ForgeRequest payload."""


def accept_request(payload: dict[str, Any]) -> HandoffBundle:
    """Run a request-shaped scan and return the bounded handoff bundle.

    Raises :class:`ForgerRequestError` for anything that is not a
    well-formed ``{"kind": "scan", "path": ...}`` request.
    """
    if not isinstance(payload, dict):
        raise ForgerRequestError("request must be a JSON object")
    kind = payload.get("kind")
    if kind not in REQUEST_KINDS:
        raise ForgerRequestError(
            f"unsupported request kind {kind!r} (valid: {', '.join(REQUEST_KINDS)})"
        )
    path = payload.get("path", ".")
    if not isinstance(path, str) or not path:
        raise ForgerRequestError("request 'path' must be a non-empty string")
    options = payload.get("options") or {}
    if not isinstance(options, dict):
        raise ForgerRequestError("request 'options' must be an object")

    bundle = _scan_handoff(path)
    bounded = options.get("bounded")
    limits: dict[str, int] = {}
    if isinstance(bounded, dict):
        limits = {k: int(v) for k, v in bounded.items() if isinstance(v, int)}
        bundle = bundle.bounded(
            findings=limits.get("findings"),
            entities=limits.get("entities"),
            relationships=limits.get("relationships"),
            capabilities=limits.get("capabilities"),
            plans=limits.get("plans"),
            unknowns=limits.get("unknowns"),
        )
    bundle.extensions["x-forge-data"] = {
        "request_kind": kind,
        "bounded": bool(limits),
        **({"limits": dict(sorted(limits.items()))} if limits else {}),
    }
    return bundle


def _scan_handoff(path: str) -> HandoffBundle:
    """Scan ``path`` and normalize the emitted bundle to forge-contracts/1."""
    from pathlib import Path

    from forge_doctor_data.core.handoff import build_handoff_bundle
    from forge_doctor_data.core.service import ScanRequest, ScanService

    outcome = ScanService().run(ScanRequest(path=Path(path)))
    wire = build_handoff_bundle(outcome.report, outcome.ctx)
    return HandoffBundle.from_dict(wire)
