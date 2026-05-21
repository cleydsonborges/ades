"""Evaluate generated artifacts against loaded YAML rules."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from src.agents.code_generator.agent import GeneratedArtifacts
from src.agents.compliance_guard.models import ComplianceStatus, RuleResult


def artifact_hash(artifacts: GeneratedArtifacts) -> str:
    payload = json.dumps(
        {
            "source_files": artifacts.source_files,
            "test_stubs": artifacts.test_stubs,
            "airflow_task_graph": artifacts.airflow_task_graph,
        },
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def evaluate_rule(rule: dict[str, Any], artifacts: GeneratedArtifacts) -> RuleResult:
    rule_id = rule["id"]
    check = rule.get("check", {})
    check_type = check.get("type", "")

    if check_type == "artifact_contains":
        return _check_artifact_contains(rule_id, check, artifacts, rule)
    if check_type == "metadata_required":
        return _check_metadata_required(rule_id, check, artifacts, rule)
    return RuleResult(
        rule_id=rule_id,
        passed=False,
        severity=rule.get("severity", "medium"),
        message=f"Unknown check type: {check_type}",
    )


def _check_artifact_contains(
    rule_id: str,
    check: dict[str, Any],
    artifacts: GeneratedArtifacts,
    rule: dict[str, Any],
) -> RuleResult:
    required = check.get("required_substrings", [])
    file_suffix = check.get("file_suffix", "")
    sources = artifacts.source_files
    matched_any = False
    for name, content in sources.items():
        if file_suffix and not name.endswith(file_suffix):
            continue
        if all(sub in content.lower() for sub in required):
            matched_any = True
            break
    passed = matched_any if required else True
    return RuleResult(
        rule_id=rule_id,
        passed=passed,
        severity=rule.get("severity", "high"),
        message="Required patterns found in artifacts"
        if passed
        else f"Missing required patterns {required} in {file_suffix or 'any'} files",
    )


def _check_metadata_required(
    rule_id: str,
    check: dict[str, Any],
    artifacts: GeneratedArtifacts,
    rule: dict[str, Any],
) -> RuleResult:
    keys = check.get("keys", [])
    meta = artifacts.airflow_task_graph.get("metadata", {})
    missing = [k for k in keys if k not in meta]
    passed = not missing
    return RuleResult(
        rule_id=rule_id,
        passed=passed,
        severity=rule.get("severity", "medium"),
        message="Metadata complete" if passed else f"Missing metadata keys: {missing}",
    )


def aggregate_status(results: list[RuleResult]) -> ComplianceStatus:
    if any(not r.passed and r.severity in ("high", "critical") for r in results):
        return ComplianceStatus.FAIL
    if any(not r.passed for r in results):
        return ComplianceStatus.REVIEW
    return ComplianceStatus.PASS


def risk_score(results: list[RuleResult]) -> float:
    if not results:
        return 0.0
    weights = {"low": 0.1, "medium": 0.3, "high": 0.7, "critical": 1.0}
    failed = [r for r in results if not r.passed]
    if not failed:
        return 0.0
    return min(1.0, sum(weights.get(r.severity, 0.5) for r in failed) / len(failed))
