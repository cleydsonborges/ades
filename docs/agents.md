# ADES Agent Modules

**Autonomous Data Engineering System (ADES)** — *powered by Agentic AI*

> **Phase 1 note:** This document describes the **target architecture** and current APIs. Today: template-based CDC generation, YAML compliance checks, rule-based Sentinel stubs, and minimal Genetic Optimizer evolution. LLM orchestration (LangGraph/AutoGen) and full Airflow deploy are **planned** (Phase 2+). See [README Implementation Status](../README.md#implementation-status), [LIMITATIONS.md](../LIMITATIONS.md), and [for-expert-review.md](for-expert-review.md).

ADES distributes intelligence across **three primary agents** and **two core engines**. Each module exposes a stable Python API; future orchestration will use LangGraph/AutoGen and Airflow.

## Agent Overview

| Module | Path | Responsibility (Phase 1) |
|--------|------|---------------------------|
| Code Generator | `src/agents/code_generator` | Objective + metadata → template-generated PySpark/SQL |
| Compliance Guard | `src/agents/compliance_guard` | Policy validation & lineage |
| Sentinel | `src/agents/sentinel` | Runtime anomaly detection |
| Genetic Optimizer | `src/core/genetic_optimizer` | Self-healing search |
| Orchestration | `src/core/orchestration` | Airflow & multi-agent coordination |

---

## Code Generator Agent

### Purpose

Converts a structured `PipelinePlan` (and objective string) into **generated artifacts** for review and deploy. Phase 1 uses the `cdc_ingestion` template; LLM-driven generation is planned for Phase 2.

### Inputs

- Objective string and structured `PipelinePlan`
- Target runtime (PySpark, dbt, pure SQL)
- Environment metadata (dev/staging/prod)
- Optional: existing codebase context for incremental edits

### Outputs

- Source files (`.py`, `.sql`, `.yml`)
- Unit test stubs
- Airflow task graph fragment
- Metadata for Compliance Guard review

### Tool Access (roadmap)

| Tool | Status |
|------|--------|
| Schema introspection | Planned (metadata lake) |
| SQL/Spark sandbox execution | Planned |
| dbt CLI | Planned |
| Repository API | Planned |

### Interaction Pattern

```
Orchestrator → CodeGenerator.generate(plan)
            → ComplianceGuard.review(artifacts)
            ← pass | fail + hints
            → (on fail) CodeGenerator.revise(hints)
            → Orchestration.deploy(artifacts)
```

---

## Compliance Guard Agent

### Purpose

Enforces **Compliance-as-Code** before and after deployment. Acts as a mandatory gate—no artifact reaches production without a recorded policy evaluation.

### Rule Categories

| Category | Examples |
|----------|----------|
| **PII / PHI** | Masking, encryption-at-rest, minimum necessary fields |
| **SOX / Financial** | Immutable audit trails, segregation of duties in DAG roles |
| **Retention** | TTL on raw zones, legal hold flags |
| **Lineage** | Source → transform → sink documentation |

See [compliance.md](compliance.md) for regulatory mapping detail.

### Outputs

- `ComplianceReport`: status, violated rules, suggested fixes
- Lineage graph fragment (JSON-LD compatible)
- Risk score used by Sentinel for baseline profiling

---

## Sentinel Agent

### Purpose

Designed for **runtime monitoring** over pipelines and data access paths. Phase 1: `on_task_failure()` and rule-based `ingest_telemetry()` (volume/off-hours thresholds).

### Signal Sources

- Airflow task logs and durations
- Warehouse query audit logs
- Row count / null rate / cardinality deltas
- IAM and network access events (when integrated)

### Detection Classes

| Class | Description |
|-------|-------------|
| **Schema drift** | Unexpected columns or type changes |
| **Volume anomaly** | Spike or drop vs. learned baseline |
| **Access anomaly** | Off-hours or new principal access to sensitive datasets |
| **Exfiltration pattern** | Unusual export volume or cross-region copies |

### Response Actions (roadmap)

1. Alert (PagerDuty, Slack, SIEM webhook) — planned
2. DAG pause / task kill — planned
3. Trigger Genetic Optimizer with failure context — **implemented** (library API)
4. Escalate to Compliance Guard — planned for runtime path

---

## Genetic Optimizer (Core Engine)

Not a conversational agent, but an **autonomous repair engine** paired with the Code Generator.

### Workflow

1. Receive `FailureSignature` from Sentinel or Airflow.
2. Seed population from last known good pipeline variant.
3. Mutate parameters (partitions, joins, filters) and code snippets.
4. Evaluate fitness: recovery success, runtime cost, compliance score.
5. Return best candidate to orchestration for redeploy.

---

## Orchestration Layer

Coordinates agent message passing, persists state, and emits **Airflow DAGs** with:

- Standardized callbacks to Sentinel
- Compliance Guard pre-flight sensors
- Genetic Optimizer on_failure hooks

Configuration lives under `src/core/orchestration/`; environment-specific values use env vars or Airflow Variables—never hard-coded secrets.

---

## Multi-Agent Coordination (LangGraph / AutoGen) — Planned

ADES will use a **supervisor pattern** (Phase 2):

- **Supervisor**: Orchestration planner
- **Workers**: Code Generator, Compliance Guard, Sentinel (on-demand)
- **Shared memory**: Plan state, artifact versions, compliance reports

This mirrors deployments consolidated from prior production systems—reducing hand-offs between siloed tools (notebook, Airflow UI, separate security scanners).
