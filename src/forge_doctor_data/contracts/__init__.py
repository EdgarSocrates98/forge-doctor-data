"""Forge contracts — shared versioned wire models (P16).

The vocabulary every Forge product speaks: ``Entity``, ``Relationship``,
``Evidence``, ``Finding``, ``Capability``, ``MigrationPlan``,
``RemediationPlan``, ``HandoffBundle``, ``DiagnosticManifest`` plus
``ContractVersion`` negotiation. Dependency-free and JSON-native so
consumers never import engine internals. The engine converts via
``core/contract_adapters.py``; JSON Schemas in ``core.schemas`` remain
the wire source of truth.
"""

from forge_doctor_data.contracts.models import (
    CONTRACT_VERSION,
    Capability,
    DiagnosticManifest,
    Entity,
    Evidence,
    Finding,
    HandoffBundle,
    MigrationPlan,
    Relationship,
    RemediationPlan,
)
from forge_doctor_data.contracts.version import (
    CURRENT,
    SUPPORTED,
    ContractVersion,
    negotiate,
)

__all__ = [
    "CONTRACT_VERSION",
    "CURRENT",
    "SUPPORTED",
    "Capability",
    "ContractVersion",
    "DiagnosticManifest",
    "Entity",
    "Evidence",
    "Finding",
    "HandoffBundle",
    "MigrationPlan",
    "Relationship",
    "RemediationPlan",
    "negotiate",
]
