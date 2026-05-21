"""Compliance Guard agent and rule pack tests."""

from src.agents.code_generator.agent import CodeGeneratorAgent, PipelinePlan
from src.agents.compliance_guard.agent import ComplianceGuardAgent
from src.agents.compliance_guard.models import ComplianceStatus
from src.agents.compliance_guard.rules_loader import load_rules, validate_rule_schema


def test_load_rules_includes_hipaa_sox_fisma():
    rules = load_rules()
    packs = {r["pack"] for r in rules}
    assert "hipaa" in packs
    assert "sox" in packs
    assert "fisma" in packs


def test_validate_rule_schema_accepts_sample_rules():
    for rule in load_rules():
        assert validate_rule_schema(rule) == []


def test_review_passes_after_revise():
    gen = CodeGeneratorAgent()
    guard = ComplianceGuardAgent()
    plan = PipelinePlan(
        objective="CDC with PHI",
        target_runtime="sql",
        environment="prod",
        metadata={
            "template_id": "cdc_ingestion",
            "pii_columns": ["email"],
            "audit_trail": True,
            "lineage_id": "line-1",
            "access_tier": "controlled",
        },
    )
    artifacts = gen.generate(plan)
    report = guard.review(artifacts)
    assert report.status in (ComplianceStatus.PASS, ComplianceStatus.REVIEW)


def test_review_fails_without_audit_metadata():
    gen = CodeGeneratorAgent()
    guard = ComplianceGuardAgent()
    plan = PipelinePlan(
        objective="minimal",
        target_runtime="sql",
        environment="dev",
        metadata={"template_id": "cdc_ingestion"},
    )
    artifacts = gen.generate(plan)
    report = guard.review(artifacts)
    failed_ids = {r.rule_id for r in report.rules_evaluated if not r.passed}
    assert "sox.audit_trail" in failed_ids or report.status != ComplianceStatus.PASS
