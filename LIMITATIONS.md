# ADES Phase 1 Limitations

This list defines what the **current open-source release** does not do. See [README.md](README.md) Implementation Status and [ROADMAP.md](ROADMAP.md) for planned work.

## Code generation

- **No LLM or RAG** — artifacts come from the `cdc_ingestion` template, not natural-language reasoning.
- **Single primary template** — no full library of PII anonymization, regulatory marts, or multi-tenant templates yet.
- Generated SQL/PySpark are **stubs** for demonstration, not production-tuned jobs.

## Compliance

- Rule packs are **sample YAML** (HIPAA, SOX, FISMA) — not a complete control library for any jurisdiction.
- Checks use **metadata and substring** matching — not AST analysis, column classifiers, or catalog integration.
- **No continuous runtime re-scoring** of all datasets — generation-time `review()` is the main gate.
- Human-in-the-loop tiers (`ADES_COMPLIANCE_TIER`) are **documented** but not fully implemented in the API.

## Security and monitoring (Sentinel)

- **No** PagerDuty, Slack, SIEM, or DAG kill integration.
- Telemetry uses **simple thresholds** (e.g. row volume, off-hours) — not learned baselines or fraud ML.
- Champion/Challenger routing lives under `agents/predictive/` as a **stub**.

## Orchestration and infrastructure

- **No Airflow** in default `docker-compose.yml`.
- `build_agentic_dag()` returns a portable dict unless `ADES_USE_AIRFLOW=true` and Airflow is installed.
- **No** LangGraph/AutoGen supervisor in `src/`.
- API has **no authentication** — local development only.

## Data platform integrations

- **No** live connections to Spark clusters, warehouses, dbt Cloud, or cloud IAM.
- Metadata lake is **in-memory** — no vector database backend.
- Telemetry collector does **not** export to Prometheus/OpenTelemetry yet.

## Metrics and benchmarks

- No built-in proof of **35–40% efficiency**, **30% latency reduction**, or **$1.5M savings** — those require production deployments and measurement outside this repo.

## What this means for reviewers

ADES Phase 1 is a **reference implementation and architecture scaffold** with a working happy path and tests. It demonstrates feasibility and extension points; it is not a turnkey commercial product or certified compliance product.
