"""Forge contracts — shared versioned wire models (P16).

The vocabulary every Forge product speaks: ``Entity``, ``Relationship``,
``Evidence``, ``Finding``, ``Capability``, ``UnknownFact``,
``MigrationPlan``, ``RemediationPlan``, ``HandoffBundle``,
``DiagnosticManifest`` plus ``ContractVersion`` negotiation.
Dependency-free and JSON-native so consumers never import engine
internals. The engine converts via ``core/contract_adapters.py``; the
published JSON Schemas in ``contracts.schemas`` are the wire source of
truth for ``forge-contracts/1`` payloads.
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
    UnknownFact,
)
from forge_doctor_data.contracts.version import (
    CURRENT,
    SUPPORTED,
    SUPPORTED_MAX,
    SUPPORTED_MIN,
    ContractVersion,
    negotiate,
    within_range,
)

__all__ = [
    "CONTRACT_VERSION",
    "CURRENT",
    "SUPPORTED",
    "SUPPORTED_MAX",
    "SUPPORTED_MIN",
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
    "UnknownFact",
    "negotiate",
    "within_range",
]
