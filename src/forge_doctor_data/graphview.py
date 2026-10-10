"""Forge Doctor Data → ForgeGraphView/v1 adapter.

Builds the real ``ProjectGraph`` evidence graph on demand
(``core.graph.build_graph`` — repo/jobs/orchestrators/datasets with
contains/triggers/reads/writes edges) and projects it onto the view
contract. Evidence is recorded at build time; edges are declared
static-extraction findings, never inferred.
"""

from __future__ import annotations

from pathlib import Path

from forge_doctor_data._graphview import (
    ForgeGraphView,
    GraphEdgeView,
    GraphNodeView,
    new_descriptor,
)

PROVIDER = "forge-doctor-data"


def build_view(root: str | Path = ".") -> ForgeGraphView | None:
    """Project's evidence graph → view. None when nothing is detected."""
    from forge_doctor_data.core.context import ProjectContext
    from forge_doctor_data.core.graph import build_graph

    try:
        ctx = ProjectContext(root=Path(root).resolve())
        g = build_graph(ctx)
    except Exception:
        return None
    if not g.nodes:
        return None
    desc = new_descriptor(
        provider_id=PROVIDER,
        domain="data-diagnostics",
        graph_id="evidence-graph",
        capabilities=(
            "node_inspect",
            "edge_inspect",
            "neighbors",
            "dependency_traversal",
            "search",
            "filter",
            "export",
        ),
        limitations=("built on demand from static evidence; no snapshots",),
    )
    object.__setattr__(desc, "node_count", len(g.nodes))
    object.__setattr__(desc, "edge_count", len(g.edges))
    object.__setattr__(
        desc, "available_layers", tuple(sorted({n.kind for n in g.nodes.values()}))
    )
    nodes = tuple(
        GraphNodeView(
            id=n.id,
            kind=n.kind,
            label=n.label,
            domain="data-diagnostics",
            source_provider=PROVIDER,
            attributes=({"detail": n.detail} if n.detail else {}),
            epistemic_state="declared",
        )
        for n in g.nodes.values()
    )
    edges = tuple(
        GraphEdgeView(
            id=f"{e.source}|{e.kind}|{e.target}",
            source=e.source,
            target=e.target,
            kind=e.kind,
            provenance="declared",
            epistemic_state="declared",
        )
        for e in g.edges
    )
    return ForgeGraphView(descriptor=desc, nodes=nodes, edges=edges)
