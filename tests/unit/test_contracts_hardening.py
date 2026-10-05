"""Spec 266: forge-contracts/1 hardening - null semantics, x-* extensions,
round-trip/fuzz corpus, bounded handoffs, version-range negotiation.
"""

from __future__ import annotations

import json

import pytest

from forge_doctor_data.contracts import (
    CURRENT,
    SUPPORTED_MAX,
    SUPPORTED_MIN,
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
    negotiate,
    within_range,
)

# ---------------------------------------------------------------------------
# Null semantics: required null raises; collections tolerate null -> empty
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "model,payload,missing_key",
    [
        (Finding, {"check_id": None}, "check_id"),
        (Entity, {"id": "e:1", "kind": "k", "domain": None}, "domain"),
        (Relationship, {"src": None, "dst": "b", "kind": "k"}, "src"),
        (Evidence, {"ref": "r", "kind": "k", "source": None}, "source"),
        (Capability, {"id": "c", "domain": "d", "status": None}, "status"),
        (UnknownFact, {"subject": "s", "kind": "k", "reason": None}, "reason"),
        (MigrationPlan, {"id": "m", "source": "a", "target": "b", "kind": None}, "kind"),
    ],
)
def test_explicit_null_required_field_raises(model, payload, missing_key) -> None:
    """``null`` for a required field is an error, never a conflated value."""
    base = {
        "check_id": "X",
        "title": "t",
        "severity": "info",
        "category": "c",
        "message": "m",
    }
    merged = {**base, **payload}
    with pytest.raises(ValueError, match=missing_key):
        model.from_dict(merged)


@pytest.mark.parametrize(
    "model,payload",
    [
        (Finding, {"check_id": "X", "title": "t", "severity": "info", "category": "c"}),
        (Entity, {"id": "e:1", "kind": "k"}),
        (Relationship, {"src": "a", "dst": "b"}),
        (Evidence, {"ref": "r", "kind": "k"}),
        (Capability, {"id": "c", "domain": "d"}),
        (UnknownFact, {"subject": "s", "kind": "k"}),
        (MigrationPlan, {"id": "m", "source": "a", "target": "b"}),
        (RemediationPlan, {"id": "r", "check_id": "c"}),
    ],
)
def test_missing_required_field_raises(model, payload) -> None:
    with pytest.raises(ValueError, match="missing required field"):
        model.from_dict(payload)


def test_null_and_missing_collections_decode_to_empty() -> None:
    payload = {
        "check_id": "X",
        "title": "t",
        "severity": "info",
        "category": "c",
        "message": "m",
        "tags": None,
    }
    assert Finding.from_dict(payload).tags == ()
    del payload["tags"]
    assert Finding.from_dict(payload).tags == ()
    payload["tags"] = []
    assert Finding.from_dict(payload).tags == ()


def test_collection_with_wrong_type_raises() -> None:
    with pytest.raises(ValueError, match="must be an array"):
        Finding.from_dict(
            {
                "check_id": "X",
                "title": "t",
                "severity": "info",
                "category": "c",
                "message": "m",
                "tags": "oops",
            }
        )


def test_optional_scalar_null_vs_empty_string() -> None:
    """Explicit null decodes to None (emits absent); empty string is a value."""
    base = {
        "check_id": "X",
        "title": "t",
        "severity": "info",
        "category": "c",
        "message": "m",
    }
    null_file = Finding.from_dict({**base, "file": None})
    assert null_file.file is None
    assert "file" not in null_file.to_dict()
    empty_file = Finding.from_dict({**base, "file": ""})
    assert empty_file.file == ""
    assert empty_file.to_dict()["file"] == ""


def test_non_integer_line_raises() -> None:
    with pytest.raises(ValueError, match="integer"):
        Finding.from_dict(
            {
                "check_id": "X",
                "title": "t",
                "severity": "info",
                "category": "c",
                "message": "m",
                "line": "not-an-int",
            }
        )


# ---------------------------------------------------------------------------
# x-* extension survival (forward compatibility)
# ---------------------------------------------------------------------------


def test_x_extension_roundtrip() -> None:
    payload = {
        "id": "e:1",
        "kind": "k",
        "domain": "d",
        "x-forge-data": {"partitioned": True},
        "x-future": [1, 2],
    }
    entity = Entity.from_dict(payload)
    assert entity.extensions == {"x-forge-data": {"partitioned": True}, "x-future": [1, 2]}
    emitted = entity.to_dict()
    assert emitted["x-forge-data"] == {"partitioned": True}
    assert emitted["x-future"] == [1, 2]


def test_non_x_unknown_keys_are_dropped() -> None:
    """Non-namespaced unknowns are not contract - they don't survive."""
    entity = Entity.from_dict({"id": "e:1", "kind": "k", "domain": "d", "made_up_field": 1})
    assert "made_up_field" not in entity.to_dict()


# ---------------------------------------------------------------------------
# Round-trip corpus (B.6/B.7): model -> dict -> JSON -> dict -> model
# ---------------------------------------------------------------------------

_CORPUS = [
    # missing optionals
    {"check_id": "X", "title": "t", "severity": "info", "category": "c", "message": "m"},
    # explicit nulls on optionals
    {
        "check_id": "X",
        "title": "t",
        "severity": "warning",
        "category": "c",
        "message": "m",
        "file": None,
        "line": None,
        "tags": None,
    },
    # full finding
    {
        "check_id": "SPARK001",
        "title": "collect()",
        "severity": "error",
        "category": "spark",
        "message": "collect called",
        "file": "job.py",
        "line": 3,
        "tags": ["perf", "driver"],
        "x-forge-data": {"plan": "lazy"},
    },
]


@pytest.mark.parametrize("payload", _CORPUS)
def test_finding_json_roundtrip(payload) -> None:
    wire = json.loads(json.dumps(payload))
    model = Finding.from_dict(wire)
    assert Finding.from_dict(json.loads(model.to_json())).to_dict() == model.to_dict()


def test_empty_and_large_graph_roundtrip() -> None:
    empty = HandoffBundle.from_dict(
        {
            "tool": {"name": "forge-doctor-data", "version": "0.9.0"},
            "project": {"name": "p"},
            "summary": {"passed": 0, "info": 0, "warnings": 0, "errors": 0},
            "results": [],
            "graph": {"entities": [], "relationships": []},
            "capabilities": {},
            "plans": [],
        }
    )
    assert empty.entities == () and empty.relationships == ()

    big = HandoffBundle(
        entities=tuple(
            Entity(id=f"e:{i}", kind="k", domain="d", identifier=str(i)) for i in range(500)
        ),
        relationships=tuple(
            Relationship(src=f"e:{i}", dst=f"e:{i + 1}", kind="R") for i in range(499)
        ),
    )
    restored = HandoffBundle.from_dict(json.loads(big.to_json()))
    assert len(restored.entities) == 500
    assert restored.entities[42].id == "e:42"
    assert len(restored.relationships) == 499


def test_unknown_capability_status_preserved() -> None:
    """An unrecognized status stays honest - never coerced to a guess."""
    cap = Capability.from_dict({"id": "c", "domain": "d", "status": "unknown"})
    assert cap.status == "unknown"
    assert cap.to_dict()["status"] == "unknown"
    weird = Capability.from_dict({"id": "c", "domain": "d", "status": "degraded"})
    assert weird.status == "degraded"


def test_partial_remediation_plan() -> None:
    plan = RemediationPlan.from_dict(
        {
            "id": "r1",
            "check_id": "SPARK001",
            "problem": "collect()",
            "actions": [{"id": "a1", "description": "repartition first"}],
        }
    )
    assert plan.actions == ("repartition first",)
    assert plan.targets == () and plan.risks == ()


def test_handoff_null_members_tolerated() -> None:
    """Explicit-null member arrays decode to empty (regression: ba165d6)."""
    bundle = HandoffBundle.from_dict(
        {
            "results": None,
            "graph": {"entities": None, "relationships": None},
            "capabilities": None,
            "plans": None,
            "unknowns": None,
        }
    )
    assert bundle.findings == ()
    assert bundle.entities == ()
    assert bundle.relationships == ()
    assert bundle.capabilities == ()
    assert bundle.plans == ()
    assert bundle.unknowns == ()


def test_unknown_fact_roundtrip() -> None:
    fact = UnknownFact(
        subject="metric:spark.duration",
        kind="metric",
        reason="no runtime evidence attached",
        source="runtime-collector",
    )
    restored = UnknownFact.from_dict(json.loads(fact.to_json()))
    assert restored.to_dict() == fact.to_dict()


def test_handoff_bundle_with_unknowns_roundtrip() -> None:
    bundle = HandoffBundle(
        unknowns=(UnknownFact(subject="s", kind="k", reason="r"),),
        entities=(Entity(id="e:1", kind="k", domain="d", identifier="i"),),
    )
    restored = HandoffBundle.from_dict(json.loads(bundle.to_json()))
    assert restored.to_dict() == bundle.to_dict()
    assert restored.unknowns[0].reason == "r"


# ---------------------------------------------------------------------------
# Bounded handoff (context economy)
# ---------------------------------------------------------------------------


def test_bounded_handoff_truncates_and_notes() -> None:
    bundle = HandoffBundle(
        findings=tuple(
            Finding(check_id=f"C{i}", title="t", severity="info", category="c", message="m")
            for i in range(10)
        ),
        entities=tuple(
            Entity(id=f"e:{i}", kind="k", domain="d", identifier=str(i)) for i in range(20)
        ),
        unknowns=(UnknownFact(subject="s", kind="k", reason="r"),),
    )
    bounded = bundle.bounded(findings=3, entities=5)
    assert len(bounded.findings) == 3
    assert len(bounded.entities) == 5
    reasons = {(u.subject, u.kind) for u in bounded.unknowns}
    assert ("findings", "truncated") in reasons
    assert ("entities", "truncated") in reasons
    # original unknown survives the bound
    assert any(u.subject == "s" for u in bounded.unknowns)


def test_bounded_handoff_no_truncation_keeps_order() -> None:
    bundle = HandoffBundle(
        entities=tuple(
            Entity(id=f"e:{i}", kind="k", domain="d", identifier=str(i)) for i in range(3)
        ),
    )
    assert bundle.bounded(entities=10).entities == bundle.entities


# ---------------------------------------------------------------------------
# Version window + negotiation
# ---------------------------------------------------------------------------


def test_supported_min_max_window() -> None:
    assert SUPPORTED_MIN.major == 1 and SUPPORTED_MAX.major >= SUPPORTED_MIN.major
    assert within_range("forge-contracts/1")
    assert not within_range("forge-contracts/99")
    assert not within_range("other/1")


def test_negotiate_still_exact() -> None:
    assert negotiate("forge-contracts/1") == CURRENT
    assert negotiate("forge-contracts/2") is None


def test_int_contract_version_normalizes() -> None:
    entity = Entity.from_dict({"contract_version": 1, "id": "e", "kind": "k", "domain": "d"})
    assert entity.contract_version == str(CURRENT)


def test_manifest_unknown_count() -> None:
    manifest = DiagnosticManifest(unknown_count=3)
    assert manifest.to_dict()["unknown_count"] == 3
    assert DiagnosticManifest.from_dict({"unknown_count": 2}).unknown_count == 2
