# Guide for Expert / Third-Party Technical Review

This document helps assessors evaluate the **ADES open-source repository** (Phase 1 MVP). It states what is implemented, how to reproduce evidence, and what should **not** be inferred from this repo alone.

## Scope of this repository

| In scope | Out of scope (not in this GitHub tree) |
|----------|----------------------------------------|
| Python agent APIs, orchestration REST API | Petition / professional-plan narrative documents |
| Sample HIPAA/SOX/FISMA YAML rule packs | Production deployment benchmarks (e.g. 35–40% efficiency claims) |
| Phase 1 tests and CI | Full LLM/RAG code generation (Phase 2 roadmap) |
| Architecture and roadmap for future phases | Managed Airflow cluster in default Docker Compose |

## Component evidence map

| Component | Primary code | Tests | Phase 1 limitation |
|-----------|--------------|-------|-------------------|
| Orchestration API | `src/core/orchestration/api.py`, `workflow.py` | `tests/test_orchestration.py`, `test_health.py` | No auth; local dev only |
| Code Generator | `src/agents/code_generator/agent.py` | `tests/test_code_generator.py` | CDC template only; not LLM-driven |
| Compliance Guard | `src/agents/compliance_guard/` | `tests/test_compliance_guard.py` | YAML substring/metadata checks; not full AST engine |
| Sentinel | `src/agents/sentinel/agent.py` | `tests/test_sentinel.py` | Rule-based telemetry stubs |
| Genetic Optimizer | `src/core/genetic_optimizer/optimizer.py` | `tests/test_genetic_optimizer.py` | Minimal evolution + compliance fitness |
| Predictive / metadata / telemetry | `src/agents/predictive/`, `core/metadata_lake/`, `core/telemetry/` | `tests/test_stubs.py` | Interface stubs only |

## Reproduce in ~10 minutes

```bash
git clone https://github.com/cleydsonborges/ades.git
cd ades
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
docker compose up -d
curl -s http://localhost:8000/health
curl -s -X POST http://localhost:8000/plans \
  -H "Content-Type: application/json" \
  -d '{"objective":"CDC ingest","metadata":{"template_id":"cdc_ingestion","pii_columns":["email"],"audit_trail":true,"lineage_id":"review-1","access_tier":"controlled"}}'
pytest tests/ -v
python scripts/validate_rules.py
```

Record the **commit SHA** when citing this repository in an expert opinion or exhibit.

## What the tests demonstrate

| Test module | Behavior verified |
|-------------|-------------------|
| `test_health.py` | API health endpoint and package version |
| `test_orchestration.py` | `POST /plans` workflow; DAG preview structure |
| `test_code_generator.py` | CDC template artifacts; revise path for compliance fields |
| `test_compliance_guard.py` | Rule pack load; schema validation; pass/fail review |
| `test_sentinel.py` | Failure signatures; volume telemetry alert |
| `test_genetic_optimizer.py` | Failure → evolve handoff with compliance scoring |
| `test_stubs.py` | Predictive router, metadata lake, metrics collector interfaces |

## Appropriate claims based on this repo

- Modular **Compliance-as-Code** architecture with extensible YAML rule packs.
- Working **vertical slice**: plan → generate → compliance review (with optional auto-revise).
- **Tested** Python APIs and CI (lint, rule validation, pytest).
- Credible **roadmap** for LLM orchestration, Airflow integration, and sector pilots.

## Claims that require evidence outside this repo

- Measured production efficiency gains (percentages, dollar savings).
- Full regulatory certification under HIPAA/SOX/FISMA (sample rules are illustrative).
- National-scale deployment or multi-employer economic impact.
- Live fraud/ML models or continuous runtime compliance on all data paths.

## Related documents

- [LIMITATIONS.md](../LIMITATIONS.md) — explicit MVP boundaries
- [getting-started.md](getting-started.md) — step-by-step tutorial
- [architecture.md](architecture.md) — target design vs delivery status
- [ROADMAP.md](../ROADMAP.md) — engineering phases
