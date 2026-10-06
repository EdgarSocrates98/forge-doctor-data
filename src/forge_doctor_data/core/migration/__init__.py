"""Migration intelligence: same-platform plans + cross-platform concepts.

``platform`` plans version/format upgrades within one platform (Glue
3→4, Parquet→Delta, Lambda runtimes). ``cross_platform`` maps services
onto vendor-neutral concepts with lossiness + readiness assessment.

P12: the former ``migration.py`` / ``migration_v2.py`` pair is now this
package; ``migration_v2`` remains as a compatibility facade.
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
from forge_doctor_data.core.migration.platform import MigrationPlan, plan_migrations

__all__ = [
    "Lossiness",
    "MappingKind",
    "MigrationConcept",
    "MigrationPlan",
    "MigrationReadiness",
    "ReadinessStatus",
    "assess_readiness",
    "concept_for_abstraction",
    "concept_implementations",
    "detect_runtime_sources",
    "explain_concept",
    "map_service",
    "plan_migrations",
    "platform_kind_for",
]
