"""Optimization intelligence: static candidates + evidence opportunities.

``static`` derives optimization candidates from findings and the
platform graph. ``evidence`` produces guardrailed, objective-scored
opportunities from performance/cost evidence with capability
prerequisites.

P12: the former ``optimize.py`` / ``optimize_v2.py`` pair is now this
package; ``optimize`` and ``optimize_v2`` remain as compatibility
facades.
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
from forge_doctor_data.core.optimization.static import OptimizationCandidate, optimize

__all__ = [
    "ExperimentPlan",
    "GuardrailStatus",
    "Objective",
    "OptimizationCandidate",
    "OptimizationFamily",
    "OptimizationOpportunity",
    "opportunities",
    "opportunity_facts",
    "optimize",
]
