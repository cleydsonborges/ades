# Contributing to ADES

Thank you for your interest in **ADES (Autonomous Data Engineering System)**, powered by Agentic AI. This project aims to raise the bar for autonomous, compliant, and self-healing data pipelines. Contributions from data engineers, AI researchers, and compliance experts are welcome.

## Code of Conduct

Participate respectfully and professionally. Harassment or discriminatory behavior is not tolerated.

## How to Contribute

1. **Fork** the repository and create a feature branch from `main`.
2. **Discuss** significant changes via an issue before large refactors.
3. **Follow** existing module layout under `src/agents/` and `src/core/`.
4. **Document** public APIs with clear docstrings and update `docs/` when behavior changes.
5. **Test** with `pytest`; maintain or improve coverage for touched modules.
6. **Submit** a pull request with a concise description and test plan.

## Development Setup

```bash
git clone <your-fork-url>
cd ades
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
docker compose up -d   # optional local stack
pytest tests/ -v
```

## Coding Standards

| Area | Standard |
|------|----------|
| Python | 3.11+, type hints on public APIs |
| Style | `ruff` (CI enforced) |
| Commits | Imperative mood, scoped messages (e.g., `feat(sentinel): add volume baseline`) |
| Secrets | Never commit credentials or API keys |

## Test coverage map

When adding features, extend the matching tests:

| Area | Test file |
|------|-----------|
| API / workflow | `tests/test_orchestration.py`, `tests/test_health.py` |
| Code Generator | `tests/test_code_generator.py` |
| Compliance Guard | `tests/test_compliance_guard.py` |
| Sentinel | `tests/test_sentinel.py` |
| Genetic Optimizer | `tests/test_genetic_optimizer.py` |
| Stubs (predictive, metadata, telemetry) | `tests/test_stubs.py` |

See [docs/for-expert-review.md](docs/for-expert-review.md) for reviewer-oriented mapping.

## Agent & Compliance Changes

Changes to **Compliance Guard** rule packs or **Sentinel** detection logic require:

- Updated documentation in `docs/compliance.md` or `docs/agents.md`
- Unit tests demonstrating pass/fail cases
- Run `python scripts/validate_rules.py`
- Note in PR if behavior affects regulatory interpretations (for human review)

## Pull Request Checklist

- [ ] Tests pass locally and in CI
- [ ] Docstrings and `docs/` updated if needed
- [ ] No secrets or environment-specific paths hard-coded
- [ ] CHANGELOG entry (when the project maintains one)

## Intellectual Property

By contributing, you agree that your contributions will be licensed under the same [MIT License](LICENSE) as the project.

## Questions

Open a GitHub issue with the label `question` for architectural or compliance-related discussions.
