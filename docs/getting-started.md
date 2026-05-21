# Getting Started with ADES (Phase 1)

This tutorial runs the **implemented** happy path: submit a plan, generate artifacts, and run compliance review. No Airflow or Spark cluster required.

## Glossary (short)

| Term | Meaning |
|------|---------|
| **CDC** | Change Data Capture — syncing incremental source changes |
| **Compliance-as-Code** | Policies expressed as machine-readable rules (YAML) |
| **PipelinePlan** | Structured input: objective, runtime, environment, metadata |
| **ComplianceReport** | Pass/fail result with rule details and remediation hints |
| **FailureSignature** | Context package when a pipeline task fails (for repair) |

## Prerequisites

- Python 3.11+
- Docker and Docker Compose (for the API container)
- `curl` or any HTTP client

## 1. Clone and install

```bash
git clone https://github.com/cleydsonborges/ades.git
cd ades
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Start the API

```bash
docker compose up -d
```

Wait a few seconds, then check health:

```bash
curl -s http://localhost:8000/health
```

Expected:

```json
{"status":"ok","service":"ades-orchestration"}
```

## 3. Submit a pipeline plan (passing example)

```bash
curl -s -X POST http://localhost:8000/plans \
  -H "Content-Type: application/json" \
  -d '{
    "objective": "CDC ingest with PHI masking for curated zone",
    "metadata": {
      "template_id": "cdc_ingestion",
      "source_connection": "ehr_primary",
      "target_dataset": "curated.encounters",
      "primary_key": ["encounter_id"],
      "pii_columns": ["email", "mrn"],
      "audit_trail": true,
      "lineage_id": "demo-001",
      "access_tier": "controlled"
    }
  }' | python -m json.tool
```

You should see `"status": "pass"` (or `"review"` if a non-critical rule fails), plus `report_id`, `rules_evaluated`, and artifact file names.

## 4. Submit a plan that fails compliance (optional)

Omit audit metadata to trigger SOX rule failure before auto-revise:

```bash
curl -s -X POST http://localhost:8000/plans \
  -H "Content-Type: application/json" \
  -d '{
    "objective": "CDC ingest minimal",
    "metadata": {"template_id": "cdc_ingestion", "pii_columns": ["email"]},
    "auto_revise_on_fail": true
  }' | python -m json.tool
```

Check `"revised": true` and updated `rules_evaluated` after the generator applies remediation hints.

## 5. Preview an agentic DAG (structure only)

```bash
curl -s -X POST http://localhost:8000/dags/preview \
  -H "Content-Type: application/json" \
  -d '{"dag_id": "ades_demo", "objective": "CDC ingest"}' | python -m json.tool
```

Returns a task graph (`plan` → `generate` → `compliance_gate` → `execute` → `monitor`). Airflow DAG objects require `ADES_USE_AIRFLOW=true` and a local Airflow install.

## 6. Run tests locally

```bash
pytest tests/ -v
python scripts/validate_rules.py
```

## 7. Try a sector pilot config

See sample objectives (not auto-loaded by the API):

- [pilots/healthcare/objective.yaml](../pilots/healthcare/objective.yaml)
- [pilots/banking/objective.yaml](../pilots/banking/objective.yaml)

Copy `metadata` and `objective` fields into your `POST /plans` body.

## Next steps

| Topic | Document |
|-------|----------|
| Architecture (target vs today) | [architecture.md](architecture.md) |
| Agent APIs | [agents.md](agents.md) |
| Compliance rules | [compliance.md](compliance.md) |
| Known gaps | [../LIMITATIONS.md](../LIMITATIONS.md) |
| Expert / third-party review | [for-expert-review.md](for-expert-review.md) |
