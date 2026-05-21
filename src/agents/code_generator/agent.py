"""
Code Generator Agent — converts pipeline objectives into executable artifacts.

Consolidates patterns from prior deployments where LLM-assisted generation
reduced time-to-production for PySpark and dbt workloads while preserving
organizational naming and testing conventions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.pipelines.templates import cdc_ingestion


@dataclass
class PipelinePlan:
    """Structured plan produced by the orchestration layer."""

    objective: str
    target_runtime: str  # pyspark | dbt | sql
    environment: str
    metadata: dict[str, Any] | None = None


@dataclass
class GeneratedArtifacts:
    """Bundle returned to Compliance Guard and orchestration."""

    source_files: dict[str, str]
    test_stubs: dict[str, str]
    airflow_task_graph: dict[str, Any]


class CodeGeneratorAgent:
    """
    Autonomous code generation agent for data pipelines.

    Responsibilities:
        - Translate PipelinePlan / natural language into PySpark, dbt, or SQL
        - Apply revision cycles when Compliance Guard returns remediation hints
        - Emit artifacts ready for Airflow materialization
    """

    def __init__(self, model_config: dict[str, Any] | None = None) -> None:
        self._model_config = model_config or {}

    def generate(self, plan: PipelinePlan) -> GeneratedArtifacts:
        """
        Generate pipeline artifacts from a structured plan.

        Phase 1: template-based generation from pipelines/templates/.
        Phase 2+: LangGraph tool calls to schema introspection and LLM registry.
        """
        meta = plan.metadata or {}
        template_id = meta.get("template_id", cdc_ingestion.TEMPLATE_ID)

        if template_id == cdc_ingestion.TEMPLATE_ID:
            return self._generate_cdc_ingestion(plan, meta)

        return self._generate_generic(plan)

    def revise(
        self,
        plan: PipelinePlan,
        artifacts: GeneratedArtifacts,
        remediation_hints: list[str],
    ) -> GeneratedArtifacts:
        """Regenerate artifacts incorporating compliance feedback."""
        meta = dict(artifacts.airflow_task_graph.get("metadata", {}))
        meta["audit_trail"] = True
        meta["lineage_id"] = meta.get("lineage_id") or f"ades-{plan.environment}"
        meta["access_tier"] = meta.get("access_tier", "controlled")
        meta["compliance_revisions"] = remediation_hints

        revised_plan = PipelinePlan(
            objective=plan.objective,
            target_runtime=plan.target_runtime,
            environment=plan.environment,
            metadata={**meta, "template_id": cdc_ingestion.TEMPLATE_ID},
        )
        result = self.generate(revised_plan)
        sql = result.source_files.get("transform.sql", "")
        if "mask" not in sql.lower():
            pii_cols = meta.get("pii_columns", ["email", "ssn"])
            mask_lines = "\n".join(
                f"  -- compliance: mask {col}\n  {col} = sha2({col}, 256),"
                for col in pii_cols
            )
            result.source_files["transform.sql"] = sql + "\n" + mask_lines
        return result

    def _generate_cdc_ingestion(
        self,
        plan: PipelinePlan,
        meta: dict[str, Any],
    ) -> GeneratedArtifacts:
        source = meta.get("source_connection", "source_db")
        target = meta.get("target_dataset", "curated.cdc_events")
        pk = meta.get("primary_key", ["id"])
        pii = meta.get("pii_columns", [])

        pk_list = ", ".join(pk)
        mask_clause = ""
        if pii:
            mask_clause = "\n".join(
                f"  {col} = sha2(cast({col} as string), 256),  -- mask + hash PII"
                for col in pii
            )

        sql = f"""-- ADES template: {cdc_ingestion.TEMPLATE_ID}
-- Objective: {plan.objective}
-- mask: PII handling per Compliance Guard policy
SELECT
  {pk_list},
{mask_clause}
  _loaded_at = current_timestamp()
FROM {source}
"""
        pyspark = f"""# ADES generated PySpark stub — {cdc_ingestion.TEMPLATE_ID}
from pyspark.sql import functions as F

df = spark.read.format("jdbc").option("url", "{source}").load()
# dedupe by primary key: {pk_list}
df = df.dropDuplicates([{", ".join(repr(c) for c in pk)}])
df.write.mode("append").saveAsTable("{target}")
"""

        graph_meta = {
            "template_id": cdc_ingestion.TEMPLATE_ID,
            "source_connection": source,
            "target_dataset": target,
            "primary_key": pk,
            "pii_columns": pii,
            "environment": plan.environment,
            "audit_trail": meta.get("audit_trail", False),
            "lineage_id": meta.get("lineage_id", ""),
            "access_tier": meta.get("access_tier", ""),
        }

        return GeneratedArtifacts(
            source_files={
                "transform.sql": sql,
                "ingest.py": pyspark,
            },
            test_stubs={
                "test_transform.py": (
                    "def test_primary_key_present():\n"
                    f"    assert {pk!r}\n"
                ),
            },
            airflow_task_graph={
                "tasks": ["ingest", "transform", "load"],
                "dependencies": [["ingest", "transform"], ["transform", "load"]],
                "metadata": graph_meta,
            },
        )

    def _generate_generic(self, plan: PipelinePlan) -> GeneratedArtifacts:
        return GeneratedArtifacts(
            source_files={
                "pipeline.sql": f"-- Generic pipeline for: {plan.objective}\nSELECT 1;",
            },
            test_stubs={},
            airflow_task_graph={
                "tasks": ["run"],
                "metadata": {
                    "environment": plan.environment,
                    "audit_trail": False,
                    "lineage_id": "",
                    "access_tier": "",
                },
            },
        )
