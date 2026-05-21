"""Orchestration workflow: plan → generate → compliance review."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.agents.code_generator.agent import CodeGeneratorAgent, GeneratedArtifacts, PipelinePlan
from src.agents.compliance_guard.agent import ComplianceGuardAgent
from src.agents.compliance_guard.models import ComplianceReport, ComplianceStatus


@dataclass
class PlanSubmission:
    objective: str
    target_runtime: str = "sql"
    environment: str = "dev"
    metadata: dict[str, Any] | None = None


@dataclass
class PlanExecutionResult:
    plan: PipelinePlan
    artifacts: GeneratedArtifacts
    compliance_report: ComplianceReport
    revised: bool


def execute_plan(
    submission: PlanSubmission,
    *,
    code_generator: CodeGeneratorAgent | None = None,
    compliance_guard: ComplianceGuardAgent | None = None,
    auto_revise_on_fail: bool = True,
) -> PlanExecutionResult:
    """
    Run the Phase 1 happy path: generate artifacts, review, optionally revise once.
    """
    generator = code_generator or CodeGeneratorAgent()
    guard = compliance_guard or ComplianceGuardAgent()

    plan = PipelinePlan(
        objective=submission.objective,
        target_runtime=submission.target_runtime,
        environment=submission.environment,
        metadata=submission.metadata,
    )
    artifacts = generator.generate(plan)
    report = guard.review(artifacts)
    revised = False

    if auto_revise_on_fail and report.status != ComplianceStatus.PASS:
        artifacts = generator.revise(plan, artifacts, report.remediation_hints)
        report = guard.review(artifacts)
        revised = True

    return PlanExecutionResult(
        plan=plan,
        artifacts=artifacts,
        compliance_report=report,
        revised=revised,
    )
