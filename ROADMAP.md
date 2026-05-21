# ADES Roadmap

Product roadmap for the ADES open-source framework (four engineering phases).

| Phase | Timeline | Focus | Status |
|-------|----------|-------|--------|
| **1 — Genetic core** | Months 1–6 | Self-healing orchestration, metadata lake interface, template codegen, YAML compliance rules | **In progress** (Phase 1 MVP in repo) |
| **2 — Semantic agent** | Months 7–12 | LLM + RAG code generation; containerized microservices | Planned |
| **3 — Critical pilots** | Months 13–18 | Sentinel Champion/Challenger; PII circuit breakers | Planned |
| **4 — Dissemination** | Months 19–24 | Airflow plugins, white papers, workshops | Planned |

## Phase 1 deliverables (current release)

- [x] `POST /plans` orchestration: generate → compliance review
- [x] Template-based `CodeGeneratorAgent.generate()` (CDC ingestion)
- [x] `ComplianceGuardAgent.review()` with HIPAA/SOX/FISMA YAML rules
- [x] Minimal `GeneticOptimizer.evolve()` with compliance-weighted fitness
- [x] `build_agentic_dag()` skeleton (dict or Airflow DAG when installed)
- [x] Stubs: predictive analytics, metadata lake, telemetry, sector pilots
- [ ] Airflow services in Docker Compose (deferred; see [docs/deployment.md](docs/deployment.md))
- [ ] Vector DB metadata lake backend (interface only)

## GitHub milestones (suggested)

1. **phase-1-mvp** — Vertical slice (this release)
2. **phase-1-airflow** — Compose + DAG execution
3. **phase-2-llm** — LangGraph supervisor + RAG
4. **phase-3-pilots** — Healthcare/banking pilot packs
