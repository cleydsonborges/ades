# Deployment Guide

**Autonomous Data Engineering System (ADES)** — *powered by Agentic AI*

ADES supports **local development** via Docker Compose and **production** deployment on Kubernetes with Apache Airflow as the workflow engine.

## Environments

| Environment | Purpose | Typical stack |
|-------------|---------|-----------------|
| `local` | Developer laptop | Docker Compose (API + Postgres + Redis); Airflow optional |
| `staging` | Integration & policy tuning | K8s, managed Airflow, Spark |
| `prod` | Regulated workloads | K8s, HA Airflow, enterprise IAM |

## Local Setup (Docker Compose)

```bash
# From repository root
docker compose up -d
```

Services (see `docker-compose.yml`):

| Service | Port | Role |
|---------|------|------|
| `ades-api` | 8000 | Orchestration API (`/health`, `/plans`, `/dags/preview`) |
| `postgres` | 5432 | Reserved for future Airflow metadata DB |
| `redis` | 6379 | Reserved for future Celery broker |

**Note:** Airflow is not included in the default `docker-compose.yml` (Phase 1 MVP). Install Airflow via `pip install -r requirements.txt` for `build_agentic_dag()` DAG objects, or use `/dags/preview` dict output without Airflow.

### Environment variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ADES_ENV` | Runtime environment | `local` |
| `ADES_LOG_LEVEL` | Logging verbosity | `INFO` |
| `ADES_COMPLIANCE_TIER` | Risk tier (`low`/`medium`/`high`) | `medium` |
| `OPENAI_API_KEY` | LLM provider (if used) | — |

Never commit secrets; use `.env` (gitignored) or a secret manager.

## Python Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Install ADES modules in editable mode when packaging is finalized:

```bash
pip install -e .
```

## Airflow Integration

1. Mount `src/` into Airflow workers or bake into a custom image.
2. Register ADES callbacks in `airflow.cfg` or DAG `default_args`.
3. Place generated DAGs under the Airflow `dags_folder` via orchestration output.

### Agentic DAG pattern

```python
# Conceptual — see src/core/orchestration/dag_factory.py
with DAG("ades_autonomous_ingest", ...) as dag:
    plan = PlanObjectiveOperator(task_id="plan", objective="{{ params.objective }}")
    generate = CodeGeneratorOperator(task_id="generate")
    compliance = ComplianceGuardSensor(task_id="compliance_gate")
    execute = SparkSubmitOperator(task_id="execute")
    monitor = SentinelCallback(on_failure_callback=genetic_repair_handler)

    plan >> generate >> compliance >> execute >> monitor
```

## Kubernetes (Production Sketch)

```
Namespace: ades-prod
├── Deployment: ades-orchestrator (HPA)
├── Deployment: airflow-scheduler / webserver / workers
├── StatefulSet: spark (optional)
├── Secret: llm-keys, db-credentials (External Secrets Operator)
└── ConfigMap: compliance rule packs
```

Recommended practices:

- **Network policies** isolating Spark workers from public ingress
- **Pod identity** for cloud warehouse authentication
- **Separate node pools** for compliance-heavy workloads

## Observability

| Signal | Tooling |
|--------|---------|
| Metrics | Prometheus-compatible endpoints (planned) |
| Logs | Structured JSON → ELK / CloudWatch |
| Traces | OpenTelemetry across agent calls |
| Alerts | Sentinel → PagerDuty / Slack |

## CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`) runs:

- Lint (`ruff`)
- Unit tests (`pytest`)
- Optional compliance rule pack validation

Promotion to staging/prod should require manual approval for `ADES_COMPLIANCE_TIER=high` environments.

## Health Checks

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/plans -H "Content-Type: application/json" \
  -d '{"objective": "CDC ingest", "metadata": {"pii_columns": ["email"]}}'
```

When Airflow is deployed separately:

```bash
curl http://localhost:8080/health   # Airflow webserver
```

## Troubleshooting

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| Compliance always fails | Missing rule pack config | Verify `compliance_guard/rules/` paths |
| DAG not visible | Sync path wrong | Check Airflow `dags_folder` mount |
| Sentinel no alerts | Telemetry not wired | Enable Airflow callbacks in DAG |
