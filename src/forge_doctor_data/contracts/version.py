"""Contract versioning and negotiation (P16).

Every contract family is ``<name>/<major>`` — e.g. ``forge-contracts/1``.
Two versions are wire-compatible when family *and* major match; additive
fields never bump major, removed/renamed fields always do. Negotiation
picks the newest shared version or fails explicitly - never a silent
partial decode.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class ContractVersion:
    """An opaque ``family/major`` contract identifier."""

    family: str
    major: int

    def __str__(self) -> str:
        return f"{self.family}/{self.major}"

    @staticmethod
    def parse(text: str) -> ContractVersion:
        family, sep, major = text.rpartition("/")
        if not sep or not family or not major.isdigit():
            raise ValueError(f"invalid contract version: {text!r} (expected <family>/<major>)")
        return ContractVersion(family, int(major))

    def compatible_with(self, other: ContractVersion) -> bool:
        return self.family == other.family and self.major == other.major


# The shared contract surface shipped by this package.
CURRENT = ContractVersion("forge-contracts", 1)
SUPPORTED: tuple[ContractVersion, ...] = (CURRENT,)


def negotiate(
    offered: str | ContractVersion,
    supported: tuple[ContractVersion, ...] = SUPPORTED,
) -> ContractVersion | None:
    """Return the common version for ``offered`` or ``None`` when disjoint."""
    version = offered if isinstance(offered, ContractVersion) else ContractVersion.parse(offered)
    candidates = [v for v in supported if v.compatible_with(version)]
    return max(candidates) if candidates else None
