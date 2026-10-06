"""Compatibility facade — prefer ``forge_doctor_data.core.migration``.

P12 consolidation: this module's implementation moved to
``core/migration/cross_platform.py``. Kept so existing internal imports
keep resolving; new code should import from the ``migration`` package.
"""

from forge_doctor_data.core.migration.cross_platform import (
    Lossiness,
    MappingKind,
    MigrationConcept,
    MigrationReadiness,
    ReadinessStatus,
    assess_readiness,
    concept_for_abstraction,
    concept_implementations,
    detect_runtime_sources,
    explain_concept,
    map_service,
    platform_kind_for,
)

__all__ = [
    "Lossiness",
    "MappingKind",
    "MigrationConcept",
    "MigrationReadiness",
    "ReadinessStatus",
    "assess_readiness",
    "concept_for_abstraction",
    "concept_implementations",
    "detect_runtime_sources",
    "explain_concept",
    "map_service",
    "platform_kind_for",
]
