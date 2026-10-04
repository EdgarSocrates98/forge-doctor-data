"""Compatibility facade — prefer ``forge_doctor_data.core.experiments``.

P12 consolidation: this module's implementation moved to
``core/experiments/measured.py``. Kept so existing internal imports
keep resolving; new code should import from the ``experiments``
package.
"""

from forge_doctor_data.core.experiments.measured import (
    ExperimentMetric,
    ExperimentPlanV2,
    ExperimentReportV2,
    ExperimentVerdict,
    MetricComparison,
    compare_bundles,
    evaluate,
    load_bundle,
    measure_bundle,
    synthetic_workload,
)

__all__ = [
    "ExperimentMetric",
    "ExperimentPlanV2",
    "ExperimentReportV2",
    "ExperimentVerdict",
    "MetricComparison",
    "compare_bundles",
    "evaluate",
    "load_bundle",
    "measure_bundle",
    "synthetic_workload",
]
