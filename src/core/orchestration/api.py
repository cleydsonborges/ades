"""
FastAPI surface for local development and Phase 1 orchestration.

Full production orchestration runs through Airflow when deployed.
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

from src.core.orchestration.dag_factory import build_agentic_dag
from src.core.orchestration.workflow import PlanSubmission, execute_plan

app = FastAPI(
    title="ADES Orchestration API",
    description="Autonomous Data Engineering System — powered by Agentic AI",
    version="0.1.0",
)


class PlanRequest(BaseModel):
    objective: str
    target_runtime: str = "sql"
    environment: str = "dev"
    metadata: dict[str, Any] | None = None
    auto_revise_on_fail: bool = True


class DagRequest(BaseModel):
    dag_id: str
    objective: str
    schedule: str | None = None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ades-orchestration"}


@app.post("/plans")
def submit_plan(request: PlanRequest) -> dict[str, Any]:
    """Generate pipeline artifacts and run Compliance Guard review."""
    result = execute_plan(
        PlanSubmission(
            objective=request.objective,
            target_runtime=request.target_runtime,
            environment=request.environment,
            metadata=request.metadata,
        ),
        auto_revise_on_fail=request.auto_revise_on_fail,
    )
    report = result.compliance_report
    return {
        "status": report.status.value,
        "revised": result.revised,
        "report_id": report.report_id,
        "artifact_hash": report.artifact_hash,
        "risk_score": report.risk_score,
        "remediation_hints": report.remediation_hints,
        "rules_evaluated": [
            {
                "rule_id": r.rule_id,
                "passed": r.passed,
                "severity": r.severity,
                "message": r.message,
            }
            for r in report.rules_evaluated
        ],
        "artifacts": {
            "source_files": list(result.artifacts.source_files.keys()),
            "tasks": result.artifacts.airflow_task_graph.get("tasks", []),
        },
    }


@app.post("/dags/preview")
def preview_dag(request: DagRequest) -> dict[str, Any]:
    """Return agentic DAG structure (dict or Airflow-serialized when available)."""
    dag = build_agentic_dag(
        dag_id=request.dag_id,
        objective=request.objective,
        schedule=request.schedule,
    )
    if hasattr(dag, "dag_id"):
        return {"format": "airflow", "dag_id": dag.dag_id, "task_count": len(dag.tasks)}
    return {"format": "dict", "dag": dag}
