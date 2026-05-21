"""Code Generator template tests."""

from src.agents.code_generator.agent import CodeGeneratorAgent, PipelinePlan


def test_generate_cdc_template():
    gen = CodeGeneratorAgent()
    plan = PipelinePlan(
        objective="Ingest CDC events",
        target_runtime="sql",
        environment="staging",
        metadata={
            "template_id": "cdc_ingestion",
            "source_connection": "db1",
            "primary_key": ["id"],
            "pii_columns": ["ssn"],
        },
    )
    artifacts = gen.generate(plan)
    assert "transform.sql" in artifacts.source_files
    assert "mask" in artifacts.source_files["transform.sql"].lower()
    assert artifacts.airflow_task_graph["metadata"]["source_connection"] == "db1"


def test_revise_adds_compliance_fields():
    gen = CodeGeneratorAgent()
    plan = PipelinePlan(
        objective="CDC",
        target_runtime="sql",
        environment="prod",
        metadata={"template_id": "cdc_ingestion"},
    )
    artifacts = gen.generate(plan)
    revised = gen.revise(plan, artifacts, ["sox.audit_trail: missing keys"])
    meta = revised.airflow_task_graph["metadata"]
    assert meta.get("audit_trail") is True
    assert meta.get("lineage_id")
