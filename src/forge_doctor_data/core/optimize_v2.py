"""Compatibility facade — prefer ``forge_doctor_data.core.optimization``.

P12 consolidation: this module's implementation moved to
``core/optimization/evidence.py``. Kept so existing internal imports
keep resolving; new code should import from the ``optimization``
package.
"""

from forge_doctor_data.core.optimization.evidence import (
    ExperimentPlan,
    GuardrailStatus,
    Objective,
    OptimizationFamily,
    OptimizationOpportunity,
    opportunities,
    opportunity_facts,
)

__all__ = [
    "ExperimentPlan",
    "GuardrailStatus",
    "Objective",
    "OptimizationFamily",
    "OptimizationOpportunity",
    "opportunities",
    "opportunity_facts",
]
