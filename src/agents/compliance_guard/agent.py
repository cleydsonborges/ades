"""
Compliance Guard Agent — policy evaluation and lineage for generated pipelines.

Implements Compliance-as-Code gates used in regulated U.S. healthcare and
financial data environments. Rule packs live under compliance_guard/rules/.
"""

from __future__ import annotations

import uuid

from src.agents.code_generator.agent import GeneratedArtifacts
from src.agents.compliance_guard.evaluator import (
    aggregate_status,
    artifact_hash,
    evaluate_rule,
    risk_score,
)
from src.agents.compliance_guard.models import ComplianceReport
from src.agents.compliance_guard.rules_loader import default_rule_pack_paths, load_rules


class ComplianceGuardAgent:
    """
    Validates artifacts against codified regulatory and organizational policies.

    No production deploy should bypass review() when ADES_COMPLIANCE_TIER >= medium.
    """

    def __init__(self, rule_pack_paths: list[str] | None = None) -> None:
        self._rule_pack_paths = rule_pack_paths or default_rule_pack_paths()
        self._rules = load_rules(self._rule_pack_paths)

    def reload_rules(self) -> None:
        """Reload rule packs from disk (e.g. after policy updates)."""
        self._rules = load_rules(self._rule_pack_paths)

    def review(self, artifacts: GeneratedArtifacts) -> ComplianceReport:
        """
        Static analysis + lineage inference + rule engine evaluation.

        Returns ComplianceReport with remediation_hints for Code Generator on fail.
        """
        results = [evaluate_rule(rule, artifacts) for rule in self._rules]
        status = aggregate_status(results)
        hints = [
            f"{r.rule_id}: {r.message}"
            for r in results
            if not r.passed
        ]
        meta = artifacts.airflow_task_graph.get("metadata", {})
        lineage_nodes = [
            {"id": "source", "type": meta.get("source_connection", "unknown")},
            {"id": "target", "type": meta.get("target_dataset", "unknown")},
        ]
        lineage_edges = [{"from": "source", "to": "target", "transform": "ades_pipeline"}]

        return ComplianceReport(
            report_id=str(uuid.uuid4()),
            status=status,
            artifact_hash=artifact_hash(artifacts),
            rules_evaluated=results,
            lineage_nodes=lineage_nodes,
            lineage_edges=lineage_edges,
            remediation_hints=hints,
            risk_score=risk_score(results),
        )
