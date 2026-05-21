"""Shared types for Compliance Guard."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class ComplianceStatus(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    REVIEW = "review"


@dataclass
class RuleResult:
    rule_id: str
    passed: bool
    severity: str
    message: str


@dataclass
class ComplianceReport:
    """Audit-ready output attached to each deploy attempt."""

    report_id: str
    status: ComplianceStatus
    artifact_hash: str
    rules_evaluated: list[RuleResult] = field(default_factory=list)
    lineage_nodes: list[dict[str, Any]] = field(default_factory=list)
    lineage_edges: list[dict[str, Any]] = field(default_factory=list)
    remediation_hints: list[str] = field(default_factory=list)
    risk_score: float = 0.0
