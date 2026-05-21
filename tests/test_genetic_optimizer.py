"""Genetic Optimizer and failure handoff tests."""

from src.agents.code_generator.agent import CodeGeneratorAgent, PipelinePlan
from src.agents.compliance_guard.agent import ComplianceGuardAgent
from src.agents.sentinel.agent import SentinelAgent
from src.core.genetic_optimizer.optimizer import GeneticOptimizer


def test_evolve_returns_improved_candidate():
    gen = CodeGeneratorAgent()
    guard = ComplianceGuardAgent()
    sentinel = SentinelAgent()
    optimizer = GeneticOptimizer(
        population_size=4,
        max_generations=3,
        compliance_guard=guard,
        code_generator=gen,
        seed=42,
    )
    plan = PipelinePlan(
        objective="CDC repair",
        target_runtime="sql",
        environment="prod",
        metadata={"template_id": "cdc_ingestion", "pii_columns": ["email"]},
    )
    seed_artifacts = gen.generate(plan)
    failure = sentinel.on_task_failure(
        "dag1",
        "run1",
        "transform",
        {"error_type": "schema_drift", "remediation_hints": ["add audit fields"]},
    )
    best = optimizer.evolve(plan, failure, seed_artifacts)
    assert best.fitness_score >= 0.0
    assert best.artifacts.source_files
