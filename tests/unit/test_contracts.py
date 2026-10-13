"""P16: versioned contract models — roundtrip, negotiation, adapters."""

from __future__ import annotations

import json

import pytest

from forge_doctor_data.contracts import (
    CURRENT,
    Capability,
    ContractVersion,
    DiagnosticManifest,
    Entity,
    Evidence,
    Finding,
    HandoffBundle,
    MigrationPlan,
    Relationship,
    RemediationPlan,
    negotiate,
)


class TestContractVersion:
    def test_parse_and_str(self) -> None:
        v = ContractVersion.parse("forge-contracts/1")
        assert v.family == "forge-contracts" and v.major == 1
        assert str(v) == "forge-contracts/1"

    @pytest.mark.parametrize("bad", ["", "1", "x/", "/1", "a/b"])
    def test_parse_rejects(self, bad: str) -> None:
        with pytest.raises(ValueError):
            ContractVersion.parse(bad)

    def test_compatible_requires_same_family_and_major(self) -> None:
        a = ContractVersion("forge-contracts", 1)
        assert a.compatible_with(ContractVersion("forge-contracts", 1))
        assert not a.compatible_with(ContractVersion("forge-contracts", 2))
        assert not a.compatible_with(ContractVersion("other", 1))

    def test_negotiate(self) -> None:
        assert negotiate("forge-contracts/1") == CURRENT
        assert negotiate("forge-contracts/99") is None
        assert negotiate("other/1") is None
        supported = (
            ContractVersion("forge-contracts", 1),
            ContractVersion("forge-contracts", 2),
        )
        assert negotiate("forge-contracts/2", supported).major == 2


def _all_models() -> list:
    return [
        Finding(check_id="SPARK001", title="t", severity="error", category="spark", message="m"),
        Entity(id="table:iceberg:db.t", kind="table", domain="iceberg", identifier="db.t"),
        Relationship(src="a", dst="b", kind="READS_FROM"),
        Evidence(ref="ev:1", kind="log", source="spark"),
        Capability(id="iceberg.v2", domain="iceberg", status="supported"),
        MigrationPlan(id="m1", source="glue3", target="glue4", kind="platform_upgrade"),
        RemediationPlan(id="r1", actions=("partition the table",)),
        DiagnosticManifest(domains=("spark",), finding_count=1),
        HandoffBundle(
            tool_version="0.9.0",
            findings=(
                Finding(check_id="X", title="t", severity="warning", category="c", message="m"),
            ),
            entities=(Entity(id="e:1", kind="k", domain="d", identifier="i"),),
        ),
    ]


@pytest.mark.parametrize("model", _all_models())
def test_json_roundtrip_is_deterministic(model) -> None:
    payload = model.to_dict()
    # JSON-native: what goes over the wire equals what comes back.
    wire = json.loads(json.dumps(payload))
    assert wire == payload
    restored = type(model).from_dict(wire)
    assert restored.to_dict() == payload
    assert model.to_json() == model.to_json()


def test_contract_version_field_present() -> None:
    assert Finding(check_id="a", title="t", severity="info", category="c", message="m").to_dict()[
        "contract_version"
    ] == str(CURRENT)


def test_from_dict_tolerates_missing_optional() -> None:
    f = Finding.from_dict(
        {"check_id": "X", "title": "t", "severity": "info", "category": "c", "message": "m"}
    )
    assert f.file is None and f.tags == ()


def test_engine_adapters() -> None:
    from forge_doctor_data.core.capabilities import CapabilityResult, CapabilityStatus
    from forge_doctor_data.core.contract_adapters import (
        capability_contract,
        entity_contract,
        finding_contract,
        relationship_contract,
    )
    from forge_doctor_data.core.models import CheckResult, Severity
    from forge_doctor_data.core.platform_graph import Entity as EngineEntity
    from forge_doctor_data.core.platform_graph import EntityKind, RelKind
    from forge_doctor_data.core.platform_graph import Relationship as EngineRel

    result = CheckResult(
        check_id="SPARK001",
        title="collect()",
        severity=Severity.ERROR,
        category="spark",
        message="collect called",
    )
    contract = finding_contract(result)
    assert contract.severity == "error" and contract.check_id == "SPARK001"
    assert contract.fingerprint == result.fingerprint

    entity = EngineEntity(
        kind=next(iter(EntityKind)),
        domain="iceberg",
        identifier="db.t",
    )
    ce = entity_contract(entity)
    assert ce.id == entity.id and ce.domain == "iceberg"

    rel = EngineRel(src=entity.id, dst=entity.id, kind=next(iter(RelKind)))
    cr = relationship_contract(rel)
    assert cr.src == entity.id

    cap = CapabilityResult(
        capability="iceberg.v2",
        platform="iceberg",
        status=CapabilityStatus.SUPPORTED,
        entry_id="pack-entry-1",
    )
    cc = capability_contract(cap)
    assert cc.id == "iceberg.v2" and cc.evidence_refs == ("pack-entry-1",)
