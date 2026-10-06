"""Spec 266/§14: architectural drift guard for ``forge_doctor_data.contracts``.

The contract package is the ecosystem boundary. It must never import
engine internals and must never name vendor-specific concepts - a shared
contract that knows about Spark or Iceberg is coupling in disguise.
"""

from __future__ import annotations

import ast
from pathlib import Path

CONTRACTS_DIR = Path(__file__).resolve().parents[2] / "src" / "forge_doctor_data" / "contracts"

# Vendor/domain terms forbidden in contract source. "spark" etc. may appear
# in *data* at runtime (a Finding category) but never in the contract shape.
# Phase 7.3 adds the API Doctor's surface (OpenAPI/GraphQL) and runtime
# execution concepts (RequestExecution/QueryExecution) to the freeze: the
# universal vocabulary must never learn a producer's domain objects.
_FORBIDDEN_TERMS = (
    "spark",
    "iceberg",
    "kafka",
    "airflow",
    "glue",
    "dynamodb",
    "neptune",
    "snowflake",
    "bigquery",
    "redshift",
    "databricks",
    "terraform",
    "athena",
    "emr",
    "flink",
    "trino",
    "dbt",
    "lambda",
    "openapi",
    "graphql",
    "requestexecution",
    "queryexecution",
    "request_execution",
    "query_execution",
)


def _contract_files() -> list[Path]:
    return sorted(CONTRACTS_DIR.glob("*.py"))


def test_contracts_package_exists() -> None:
    assert CONTRACTS_DIR.is_dir()
    assert _contract_files()


def test_contracts_never_import_engine() -> None:
    """No import of forge_doctor_data outside the contracts package itself."""
    for path in _contract_files():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            for name in names:
                assert name.startswith("forge_doctor_data.contracts") or not name.startswith(
                    "forge_doctor_data"
                ), f"{path.name}: imports engine module {name!r}"


def test_contracts_are_domain_neutral() -> None:
    for path in _contract_files():
        # Docstrings may name consumers ("Spark Forge"); scan identifiers
        # and string literals in executable positions only.
        tree = ast.parse(path.read_text(encoding="utf-8"))
        # Docstrings may name consumers ("Spark Forge"); scan identifiers
        # and string literals in executable positions only.
        docstrings = {
            id(node.value)
            for node in ast.walk(tree)
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)
        }
        identifiers: set[str] = set()
        for node in ast.walk(tree):
            if id(node) in docstrings:
                continue
            if isinstance(node, ast.Name | ast.Attribute):
                identifiers.add((node.id if isinstance(node, ast.Name) else node.attr).lower())
            elif isinstance(node, ast.arg):
                identifiers.add(node.arg.lower())
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                for word in node.value.replace(":", " ").replace("_", " ").split():
                    identifiers.add(word.strip(".,'\"()[]{}|").lower())
        for term in _FORBIDDEN_TERMS:
            assert term not in identifiers, f"{path.name}: domain term {term!r} leaked"


def test_contract_models_have_no_engine_subclasses() -> None:
    """Contract classes must not subclass engine types."""
    import forge_doctor_data.contracts.models as m

    for name in dir(m):
        cls = getattr(m, name)
        if (
            isinstance(cls, type)
            and issubclass(cls, m.ContractModel)
            and cls is not m.ContractModel
        ):
            for base in cls.__mro__[1:]:
                assert base.__module__.startswith(
                    "forge_doctor_data.contracts"
                ) or base.__module__ in {"builtins", "abc"}, (
                    f"{name}: inherits from engine class {base!r}"
                )


def test_public_surface_is_frozen_vocabulary() -> None:
    """The exported vocabulary is exactly the frozen universal concept set."""
    import forge_doctor_data.contracts as contracts

    expected = {
        "CONTRACT_VERSION",
        "CURRENT",
        "SUPPORTED",
        "SUPPORTED_MAX",
        "SUPPORTED_MIN",
        "Capability",
        "ContractVersion",
        "DiagnosticManifest",
        "Entity",
        "Evidence",
        "Finding",
        "HandoffBundle",
        "MigrationPlan",
        "Relationship",
        "RemediationPlan",
        "UnknownFact",
        "negotiate",
        "within_range",
    }
    assert set(contracts.__all__) == expected
