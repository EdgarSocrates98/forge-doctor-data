"""Portable install lifecycle for Forge Doctor Data.

Implements the shared ``forge/*`` installation contract v1 over the vendored
installkit (``forge_doctor_data._installkit``): scoped targets, approval
gating, managed ledger, receipts, drift repair and uninstall.

Forge Doctor Data ships no host skill/agent mirrors — every profile installs
the managed MCP key plus marker blocks; the profile knob stays validated so
future mirrors slot in without a contract change.
"""

from __future__ import annotations

__all__ = ["service"]
