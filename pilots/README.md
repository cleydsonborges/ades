# Sector pilots

Sample objectives for healthcare and banking verticals. Use with the orchestration API (see [docs/getting-started.md](../docs/getting-started.md)):

```bash
curl -X POST http://localhost:8000/plans \
  -H "Content-Type: application/json" \
  -d '{"objective": "...", "metadata": {"template_id": "cdc_ingestion", ...}}'
```

See `healthcare/objective.yaml` and `banking/objective.yaml`.
