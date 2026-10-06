"""Phase 5 hardening: what-if + migration honesty, determinism, no-mutation.

Pins the release-candidate contract:
- a valid hypothetical change produces a deterministic, evidence-carrying report
- the same scenario evaluated twice is byte-identical
- evaluating a change never mutates the observed state (graph/files)
- unsupported/lost capabilities, missing evidence, and unknowns are explicit
- migration mappings are honest: UNKNOWN / REDESIGN_REQUIRED / NO_EQUIVALENT
  / APPROXIMATE never collapse into DIRECT when equivalence is unproven
- readiness aggregates carry an explicit unknown budget
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from forge_doctor_data.core.context import ProjectContext
from forge_doctor_data.core.migration.cross_platform import (
    Lossiness,
    MappingKind,
    MigrationConcept,
    ReadinessStatus,
    assess_readiness,
    map_service,
)
from forge_doctor_data.core.whatif import (
    WhatIfChange,
    WhatIfReport,
    evaluate_change,
    parse_change,
)


def make_context(tmp_path: Path, files: dict[str, str]) -> ProjectContext:
    for name, source in files.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding="utf-8")
    return ProjectContext(root=tmp_path)


TF_GLUE4 = """
resource "aws_glue_job" "etl" {
  name         = "etl"
  glue_version = "4.0"
}
"""


def _report_dict(report: WhatIfReport) -> dict:
    return {
        "change": {
            "target": report.change.target,
            "property": report.change.property,
            "from": report.change.from_,
            "to": report.change.to,
            "assumptions": list(report.change.assumptions),
        },
        "affected_entities": list(report.affected_entities),
        "impacts": [
            {
                "category": i.category,
                "severity": i.severity,
                "detail": i.detail,
                "evidence": list(i.evidence),
            }
            for i in report.impacts
        ],
        "unsupported_now": list(report.unsupported_now),
        "supported_now": list(report.supported_now),
        "unknown": list(report.unknown),
    }


# -- Phase 5.1: valid hypothetical change ------------------------------------


def test_parse_change_valid_target(tmp_path: Path) -> None:
    change = parse_change("glue-version=5.0")
    assert change.target == "glue"
    assert change.property == "glue_version"
    assert change.to == "5.0"


def test_parse_change_rejects_unknown_target_deterministically() -> None:
    with pytest.raises(ValueError, match="unknown change target"):
        parse_change("snowmobile=9.9")


def test_parse_change_rejects_malformed_spec() -> None:
    with pytest.raises(ValueError, match="malformed"):
        parse_change("glue-version")


def test_valid_change_produces_affected_entities_and_impacts(tmp_path: Path) -> None:
    ctx = make_context(tmp_path, {"main.tf": TF_GLUE4})
    report = evaluate_change(ctx, parse_change("glue-version=5.0"))
    assert report.change.from_ == "4.0"  # observed from terraform evidence
    assert report.affected_entities  # the glue job entity is touched
    assert report.impacts  # evaluated consequences exist
    severities = {i.severity for i in report.impacts}
    assert severities <= {"blocker", "warn", "info"}
    for impact in report.impacts:
        assert impact.detail  # every consequence explains itself


def test_report_byte_identical_for_same_scenario(tmp_path: Path) -> None:
    ctx = make_context(tmp_path, {"main.tf": TF_GLUE4})
    one = json.dumps(_report_dict(evaluate_change(ctx, parse_change("glue-version=5.0"))))
    two = json.dumps(_report_dict(evaluate_change(ctx, parse_change("glue-version=5.0"))))
    assert one == two


def test_impacts_sorted_by_severity_then_detail(tmp_path: Path) -> None:
    ctx = make_context(tmp_path, {"main.tf": TF_GLUE4})
    report = evaluate_change(ctx, parse_change("glue-version=3.0"))
    rank = {"blocker": 0, "warn": 1, "info": 2}
    keys = [(rank.get(i.severity, 3), i.category, i.detail) for i in report.impacts]
    assert keys == sorted(keys)


# -- Phase 5.2: what-if never mutates observed state --------------------------


def test_whatif_leaves_state_unchanged(tmp_path: Path) -> None:
    """current state before == current state after what-if."""
    ctx = make_context(tmp_path, {"main.tf": TF_GLUE4})
    from forge_doctor_data.analyzers.platform_graph_builder import build_platform_graph

    before_graph = build_platform_graph(ctx).to_dict()
    before_files = set(ctx.files)
    evaluate_change(ctx, parse_change("glue-version=5.0"))
    evaluate_change(ctx, parse_change("platform=snowflake"))
    after_graph = build_platform_graph(ctx).to_dict()
    assert before_graph == after_graph
    assert set(ctx.files) == before_files
    assert (tmp_path / "main.tf").read_text() == TF_GLUE4


# -- Phase 5.3: unsupported capability / missing evidence / unknowns ---------


def test_no_evidence_marks_from_unverified(tmp_path: Path) -> None:
    ctx = make_context(tmp_path, {"README.md": "nothing here\n"})
    report = evaluate_change(ctx, parse_change("glue-version=5.0"))
    assert any("unverified" in u for u in report.unknown)


def test_unknown_platform_has_no_capability_facts(tmp_path: Path) -> None:
    ctx = make_context(tmp_path, {"main.tf": TF_GLUE4})
    report = evaluate_change(
        ctx, WhatIfChange(target="iceberg", property="format_version", from_="", to="3")
    )
    # Either capability facts exist or the gap is declared - never silent.
    assert report.impacts or report.unknown


# -- Phase 5.4/5.5: migration mapping honesty ---------------------------------


def test_identity_mapping_is_direct_and_lossless() -> None:
    concept = map_service("s3", "s3")
    assert concept.mapping == MappingKind.DIRECT
    assert concept.lossiness == Lossiness.LOSSLESS


def test_unknown_source_is_unknown_never_direct() -> None:
    concept = map_service("not-a-service", "s3")
    assert concept.mapping == MappingKind.UNKNOWN
    assert concept.confidence == "low"
    assert concept.missing_evidence


def test_unmapped_target_is_no_equivalent() -> None:
    concept = map_service("s3", "")
    assert concept.mapping == MappingKind.NO_EQUIVALENT
    assert concept.operational_gap


def test_schema_incompatibility_is_approximate_not_direct() -> None:
    """s3 -> adls_gen2: hierarchical namespace vs flat store (schema-level)."""
    concept = map_service("s3", "adls_gen2")
    assert concept.mapping == MappingKind.APPROXIMATE
    assert concept.lossiness == Lossiness.SEMANTIC_CHANGE
    assert concept.semantic_gap


def test_runtime_difference_is_approximate_operational() -> None:
    """redshift -> snowflake: dist/sort keys + credits compute model."""
    concept = map_service("redshift", "snowflake")
    assert concept.mapping != MappingKind.DIRECT
    assert concept.lossiness in (
        Lossiness.OPERATIONAL_CHANGE,
        Lossiness.SEMANTIC_CHANGE,
        Lossiness.UNKNOWN,
        Lossiness.MANUAL_REDESIGN,
    )
    assert concept.operational_gap or concept.semantic_gap or concept.capability_gaps


def test_governance_difference_surfaces_capability_evidence() -> None:
    """glue catalog -> purview: governance capabilities must be proven."""
    concept = map_service("glue", "purview")
    assert concept.mapping != MappingKind.DIRECT or not concept.missing_evidence
    if concept.missing_evidence or concept.capability_gaps:
        assert concept.mapping in (
            MappingKind.APPROXIMATE,
            MappingKind.REDESIGN_REQUIRED,
            MappingKind.UNKNOWN,
        )


def test_missing_evidence_never_yields_direct() -> None:
    """Exhaustive over the concept registry: any mapping carrying
    missing_evidence or capability_gaps must not claim DIRECT."""
    from forge_doctor_data.core.migration.cross_platform import concept_implementations

    for concept_name in (
        "columnar_mpp_warehouse",
        "object_store",
        "managed_stream",
        "managed_spark",
        "orchestrator",
        "catalog_governance",
        "operational_kv",
        "lakehouse_format",
    ):
        impls = concept_implementations(concept_name)
        for source in impls:
            for target in impls:
                if source == target:
                    continue
                concept = map_service(source, target)
                if concept.mapping == MappingKind.DIRECT:
                    assert not concept.missing_evidence, (
                        f"{source}->{target}: DIRECT despite missing evidence "
                        f"{concept.missing_evidence}"
                    )
                    assert not concept.capability_gaps
                    assert not concept.semantic_gap
                    assert not concept.operational_gap


# -- Phase 5.6: readiness verdicts + unknown budget ---------------------------


def _concept(
    mapping: MappingKind, missing: tuple[str, ...] = (), gaps: tuple[str, ...] = ()
) -> MigrationConcept:
    return MigrationConcept(
        logical_concept="c",
        source_implementation="s",
        target_implementation="t",
        mapping=mapping,
        lossiness=Lossiness.UNKNOWN,
        missing_evidence=missing,
        capability_gaps=gaps,
    )


def test_readiness_ready_when_all_direct() -> None:
    ready = assess_readiness([_concept(MappingKind.DIRECT), _concept(MappingKind.DIRECT)], [])
    assert ready.status == ReadinessStatus.READY
    assert ready.unknown_count == 0


def test_readiness_partial_on_approximate() -> None:
    ready = assess_readiness([_concept(MappingKind.DIRECT), _concept(MappingKind.APPROXIMATE)], [])
    assert ready.status == ReadinessStatus.PARTIAL


@pytest.mark.parametrize("kind", [MappingKind.NO_EQUIVALENT, MappingKind.REDESIGN_REQUIRED])
def test_readiness_blocked_on_unmappable(kind: MappingKind) -> None:
    assert assess_readiness([_concept(kind)], []).status == ReadinessStatus.BLOCKED


def test_readiness_blocked_on_lost_capability() -> None:
    ready = assess_readiness([_concept(MappingKind.DIRECT)], ["FEATURE_X"])
    assert ready.status == ReadinessStatus.BLOCKED


def test_readiness_insufficient_on_empty_and_unknown() -> None:
    empty = assess_readiness([], [])
    assert empty.status == ReadinessStatus.INSUFFICIENT_EVIDENCE
    assert empty.required_evidence
    unknown = assess_readiness([_concept(MappingKind.UNKNOWN)], [])
    assert unknown.status == ReadinessStatus.INSUFFICIENT_EVIDENCE
    assert unknown.unknown_count == 1


def test_readiness_unknown_budget_counts_missing_evidence() -> None:
    ready = assess_readiness([_concept(MappingKind.DIRECT, missing=("CAP_A", "CAP_B"))], [])
    assert ready.unknown_count == 2
    assert any("CAP_A" in u for u in ready.unknowns)
    assert any("CAP_A" in r for r in ready.required_evidence)
