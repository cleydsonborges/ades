# Changelog

All notable changes to the ADES open-source repository are documented here.

## [0.1.0] — 2026-05-20

### Added

- Phase 1 MVP: `POST /plans`, `POST /dags/preview`, `GET /health`
- Code Generator: CDC ingestion template (`cdc_ingestion`)
- Compliance Guard: YAML rule packs (HIPAA, SOX, FISMA samples) and `review()` API
- Genetic Optimizer: minimal `evolve()` with compliance-weighted fitness
- Sentinel: `on_task_failure`, rule-based `ingest_telemetry`
- Stubs: predictive router, metadata lake, telemetry collector
- Sector pilot samples under `pilots/`
- CI: ruff, pytest, `scripts/validate_rules.py`
- Documentation: getting started, expert review guide, limitations

### Notes

- LangGraph/LLM orchestration and Airflow in Docker Compose are roadmap items (Phase 2+).
- See [LIMITATIONS.md](LIMITATIONS.md) for explicit MVP boundaries.
