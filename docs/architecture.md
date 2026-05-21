# ADES Architecture

**Autonomous Data Engineering System (ADES)** — *powered by Agentic AI*

## Design Principles

ADES is structured as an **enterprise-grade, modular framework**—not a monolithic application. Each pillar (pipelines, security, compliance) maps to isolated packages with explicit contracts, enabling independent evolution, testing, and deployment.

| Principle | Implementation |
|-----------|----------------|
| **Agentic decomposition** | Specialized agents with narrow responsibilities and tool access |
| **Policy before execution** | Compliance Guard gates all generated artifacts |
| **Observable by default** | Sentinel + orchestration hooks emit structured telemetry |
| **Self-healing** | Genetic Optimizer explores repair candidates on failure signatures |
| **Orchestrator-agnostic core** | Business logic in `src/`; Airflow adapters in `core/orchestration` |

## Logical Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Natural Language Interface                       │
│                    (objectives, SLAs, regulatory scope)                  │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
┌─────────────────────────────────▼───────────────────────────────────────┐
│                    core/orchestration (Agentic DAG Layer)                │
│         LangGraph / AutoGen coordination · Airflow DAG materialization   │
└─────┬───────────────────┬───────────────────────┬─────────────────────┘
      │                   │                       │
      ▼                   ▼                       ▼
┌─────────────┐   ┌───────────────┐       ┌─────────────────┐
│ code_       │   │ compliance_   │       │ sentinel        │
│ generator   │   │ guard         │       │ (runtime watch) │
└──────┬──────┘   └───────┬───────┘       └────────┬────────┘
       │                  │                          │
       └──────────┬───────┴──────────────────────────┘
                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              pipelines/ (templates) · PySpark · dbt · SQL              │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
       ┌──────────────────────────┼──────────────────────────┐
       ▼                          ▼                          ▼
┌─────────────┐           ┌─────────────┐            ┌─────────────┐
│ Data Lake / │           │ Warehouse   │            │ Streaming   │
│ Object Store│           │ (BQ, SF, …) │            │ (Kafka, …)  │
└─────────────┘           └─────────────┘            └─────────────┘

         Failure / drift ──► core/genetic_optimizer ──► code_generator
```

## Component Reference

### `src/agents/code_generator`

Translates natural language and structured plans into executable **PySpark**, **dbt**, and **SQL** artifacts. Maintains versioned prompts, validation hooks, and integration with the Compliance Guard before any deploy.

### `src/agents/compliance_guard`

Implements **Compliance-as-Code**: static and dynamic analysis of generated pipelines against HIPAA, SOX, and organization-specific rule packs. Outputs pass/fail decisions, lineage annotations, and remediation guidance.

### `src/agents/sentinel`

Runtime **cybersecurity and data-quality** agent. Consumes access logs, row-level statistics, and DAG task events. Correlates anomalies (unusual volume, off-hours access, PII leakage patterns) and triggers containment workflows.

### `src/core/genetic_optimizer`

Encodes pipeline repair as an **evolutionary search** over parameter and code mutation spaces. Fitness functions combine SLA recovery time, data correctness checks, and compliance score from the Compliance Guard.

### `src/core/orchestration`

Bridges agent decisions to **Apache Airflow**: dynamic DAG generation, sensor wiring, and callback hooks for Sentinel and Genetic Optimizer feedback loops.

### `src/pipelines`

Curated **templates** for common autonomous patterns: CDC ingestion, PII anonymization flows, regulatory reporting marts, and multi-tenant isolation patterns.

## Data Flow (Happy Path)

1. User or API submits an objective to the orchestration layer.
2. Planner decomposes into tasks; Code Generator produces artifacts.
3. Compliance Guard validates; failures return to Generator with constraints.
4. Orchestration materializes Airflow DAG; execution begins.
5. Sentinel streams telemetry; no intervention required.

## Data Flow (Self-Healing Path)

1. Airflow task fails or Sentinel raises drift/anomaly alert.
2. Failure signature (stack trace, schema diff, access pattern) packaged for Genetic Optimizer.
3. Optimizer proposes population of repair candidates; Compliance Guard filters infeasible variants.
4. Winning candidate redeployed via orchestration; Sentinel confirms recovery.

## Technology Integration Matrix

| Concern | Primary integration | ADES role |
|---------|---------------------|-----------|
| Batch compute | PySpark | Generated + repaired jobs |
| Transform modeling | dbt | Generated models + tests |
| Workflow engine | Airflow | Agentic DAGs, callbacks |
| LLM orchestration | LangGraph, AutoGen | Multi-agent planning |
| Container runtime | Docker, K8s | Local and prod packaging |

## Security & Compliance Boundaries

- **Secrets**: Never embedded in generated code; resolved via orchestrator secret backends.
- **PII**: Default-deny generation paths; Compliance Guard enforces tokenization/masking.
- **Audit**: All agent decisions logged with correlation IDs tied to Airflow `run_id`.
- **Least privilege**: Sentinel and agents operate with scoped IAM roles per environment.

## Extension Points

| Extension | Hook location |
|-----------|---------------|
| Custom regulatory packs | `compliance_guard/rules/` |
| New source connectors | `pipelines/templates/` + Generator tool registry |
| Alternate orchestrators | `core/orchestration/adapters/` |
| Custom fitness functions | `genetic_optimizer/fitness/` |

## Implementation Status vs Roadmap

See [ROADMAP.md](../ROADMAP.md) for phase definitions and delivery status.

| Roadmap phase | Deliverable | Repo status |
|---------------|-------------|-------------|
| Phase 1 (M1–6) | Template codegen, YAML compliance, genetic optimizer, `/plans` API | **Implemented** (MVP) |
| Phase 1 (M1–6) | Metadata lake vector backend | **Stub** (`core/metadata_lake`) |
| Phase 1 (M1–6) | Airflow in local compose | **Planned** |
| Phase 2 (M7–12) | LLM + RAG code generation | **Planned** |
| Phase 3 (M13–18) | Champion/Challenger fraud routing | **Stub** (`agents/predictive`) |
| Phase 4 (M19–24) | Plugins, workshops | **Planned** |

Extension directories now present: `orchestration/adapters/`, `genetic_optimizer/fitness/`, `compliance_guard/rules/custom/`.

## Related Documents

- [Getting started](getting-started.md)
- [For expert review](for-expert-review.md)
- [Agents](agents.md)
- [Compliance](compliance.md)
- [Deployment](deployment.md)
- [Limitations](../LIMITATIONS.md)
- [ROADMAP](../ROADMAP.md)
