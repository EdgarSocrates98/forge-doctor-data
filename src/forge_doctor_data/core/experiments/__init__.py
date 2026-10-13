"""Experiment intelligence: fixture transforms + measured evidence.

``fixture`` compares finding fingerprints before/after a deterministic
file transform on a scenario copy (P-240 spec 239). ``measured``
compares exported execution bundles on declared metrics with
protected-constraint overrides (spec 240). Neither executes runtimes.

P12: the former ``experiments.py`` / ``experiments_v2.py`` pair is now
this package; ``experiments_v2`` remains as a compatibility facade.
"""

from forge_doctor_data.core.experiments.fixture import (
    HYPOTHESES,
    ExperimentResult,
    Hypothesis,
    run_experiment,
)
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
    "HYPOTHESES",
    "ExperimentMetric",
    "ExperimentPlanV2",
    "ExperimentReportV2",
    "ExperimentResult",
    "ExperimentVerdict",
    "Hypothesis",
    "MetricComparison",
    "compare_bundles",
    "evaluate",
    "load_bundle",
    "measure_bundle",
    "run_experiment",
    "synthetic_workload",
]
