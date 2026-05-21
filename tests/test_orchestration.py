"""Orchestration workflow and API tests."""

from fastapi.testclient import TestClient
from src.core.orchestration.api import app
from src.core.orchestration.dag_factory import build_agentic_dag
from src.core.orchestration.workflow import PlanSubmission, execute_plan


def test_execute_plan_happy_path():
    result = execute_plan(
        PlanSubmission(
            objective="CDC ingest with compliance",
            metadata={
                "template_id": "cdc_ingestion",
                "pii_columns": ["email"],
                "audit_trail": True,
                "lineage_id": "test-1",
                "access_tier": "controlled",
            },
        ),
        auto_revise_on_fail=True,
    )
    assert result.artifacts.source_files
    assert result.compliance_report.report_id


def test_plans_endpoint():
    client = TestClient(app)
    response = client.post(
        "/plans",
        json={
            "objective": "CDC",
            "metadata": {
                "template_id": "cdc_ingestion",
                "pii_columns": ["mrn"],
                "audit_trail": True,
                "lineage_id": "api-1",
                "access_tier": "controlled",
            },
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert "status" in body
    assert "report_id" in body


def test_dag_preview_returns_structure():
    dag = build_agentic_dag("test_dag", "ingest customers")
    if isinstance(dag, dict):
        assert dag["dag_id"] == "test_dag"
        assert len(dag["tasks"]) >= 4
    else:
        assert dag.dag_id == "test_dag"
