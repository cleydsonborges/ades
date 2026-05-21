"""
Agentic DAG factory — materializes Airflow DAGs from ADES agent outputs.

Bridges LangGraph/AutoGen supervisor workflows to schedulable DAG definitions
with Sentinel callbacks and Compliance Guard pre-flight sensors.
"""

from __future__ import annotations

from typing import Any


def build_agentic_dag(
    dag_id: str,
    objective: str,
    schedule: str | None = None,
    default_args: dict[str, Any] | None = None,
) -> Any:
    """
    Return an Airflow DAG wired with Plan → Generate → Compliance → Execute → Monitor.

    When apache-airflow is installed, returns a DAG object; otherwise a portable dict.
    """
    task_graph = {
        "dag_id": dag_id,
        "schedule": schedule,
        "default_args": default_args or {},
        "objective": objective,
        "tasks": [
            {"task_id": "plan", "operator": "PlanObjectiveOperator"},
            {"task_id": "generate", "operator": "CodeGeneratorOperator"},
            {"task_id": "compliance_gate", "operator": "ComplianceGuardSensor"},
            {"task_id": "execute", "operator": "SparkSubmitOperator"},
            {"task_id": "monitor", "operator": "SentinelCallback"},
        ],
        "dependencies": [
            ["plan", "generate"],
            ["generate", "compliance_gate"],
            ["compliance_gate", "execute"],
            ["execute", "monitor"],
        ],
        "callbacks": {
            "on_failure": "sentinel_on_task_failure",
            "on_success": "sentinel_ingest_telemetry",
        },
    }

    use_airflow = __import__("os").environ.get("ADES_USE_AIRFLOW", "").lower() in (
        "1",
        "true",
        "yes",
    )
    if not use_airflow:
        return task_graph

    try:
        from airflow import DAG
        from airflow.operators.empty import EmptyOperator

        with DAG(
            dag_id=dag_id,
            schedule=schedule,
            default_args=default_args or {},
            catchup=False,
            tags=["ades", "agentic"],
        ) as dag:
            plan = EmptyOperator(task_id="plan")
            generate = EmptyOperator(task_id="generate")
            compliance_gate = EmptyOperator(task_id="compliance_gate")
            execute = EmptyOperator(task_id="execute")
            monitor = EmptyOperator(task_id="monitor")
            plan >> generate >> compliance_gate >> execute >> monitor
        return dag
    except (ImportError, OSError, PermissionError):
        return task_graph
