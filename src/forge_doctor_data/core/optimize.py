"""Compatibility facade — prefer ``forge_doctor_data.core.optimization``.

P12 consolidation: this module's implementation moved to
``core/optimization/static.py``. Kept so existing internal imports keep
resolving; new code should import from the ``optimization`` package.
"""

from forge_doctor_data.core.optimization.static import OptimizationCandidate, optimize

__all__ = ["OptimizationCandidate", "optimize"]
