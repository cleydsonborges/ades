"""Compliance-weighted fitness component for Genetic Optimizer."""

from __future__ import annotations

from src.agents.compliance_guard.models import ComplianceReport, ComplianceStatus


def compliance_fitness_component(report: ComplianceReport) -> float:
    """
    Map compliance report to a 0.0–1.0 fitness contribution.

    PASS → 1.0, REVIEW → 0.5, FAIL → 0.0 (penalized by risk_score).
    """
    if report.status == ComplianceStatus.PASS:
        return 1.0
    if report.status == ComplianceStatus.REVIEW:
        return max(0.3, 0.5 - report.risk_score * 0.2)
    return max(0.0, 0.2 - report.risk_score)
