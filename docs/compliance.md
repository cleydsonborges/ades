# Compliance-as-Code in ADES

**Autonomous Data Engineering System (ADES)** — *powered by Agentic AI*

> **Phase 1 note:** Rule packs under `compliance_guard/rules/` are **illustrative samples** (YAML). Evaluation uses metadata and artifact substring checks—not a full AST engine or catalog integration. Runtime re-scoring via Sentinel is **roadmap**. See [LIMITATIONS.md](../LIMITATIONS.md) and [for-expert-review.md](for-expert-review.md).

The **Compliance Guard** agent embeds policy into the data engineering lifecycle—evaluating artifacts **at generation time** via `review()`. Continuous runtime enforcement is the target design.

## Philosophy

Traditional compliance reviews occur **after** pipelines ship, creating rework and audit risk. ADES inverts this model:

1. Policies are codified as machine-readable rule packs.
2. Every generated artifact receives a `ComplianceReport` before deploy.
3. Runtime drift triggers re-evaluation and optional auto-remediation.

## Supported Frameworks (Extensible)

| Framework | Scope in ADES | Rule pack location |
|-----------|---------------|-------------------|
| **HIPAA** | PHI identification, encryption, access logging | `compliance_guard/rules/hipaa/` |
| **SOX** | Financial data integrity, change control evidence | `compliance_guard/rules/sox/` |
| **Custom** | Tenant-specific policies | `compliance_guard/rules/custom/` |

> Rule packs ship as templates; organizations extend with jurisdiction-specific requirements.

## Policy Evaluation Pipeline

**Target pipeline** (full static analysis planned):

```
Artifact → static analysis → lineage → rule engine → ComplianceReport
```

**Phase 1 implementation:** YAML rules with `artifact_contains` and `metadata_required` checks; basic lineage nodes from plan metadata. See `src/agents/compliance_guard/evaluator.py`.

## HIPAA-Oriented Controls (Illustrative)

| Control | Automated check |
|---------|-----------------|
| Minimum necessary | Block SELECT * on PHI tables without justification tag |
| De-identification | Require hashing/tokenization functions on configured columns |
| Audit | Ensure sink tables include `accessed_at`, `job_run_id` |
| Encryption | Flag tables lacking encryption metadata in target catalog |

## SOX-Oriented Controls (Illustrative)

| Control | Automated check |
|---------|-----------------|
| Segregation of duties | DAG roles cannot combine approver + deployer in prod |
| Immutable history | Raw financial zones must be append-only |
| Change evidence | Generated code hash stored with Airflow `run_id` |

## Lineage & Audit Trail

Each `ComplianceReport` includes:

- `report_id`, `timestamp`, `artifact_hash`
- `rules_evaluated[]` with pass/fail and severity
- `lineage_nodes[]` and `lineage_edges[]`
- `remediation_hints[]` for Code Generator revision

Reports are designed for export to enterprise GRC tools or data catalogs (Collibra, Alation, etc.) via future adapter modules.

## Integration with Sentinel

Sentinel learns **normal access and volume profiles** per compliant baseline. When behavior deviates:

1. Sentinel raises alert with severity.
2. Compliance Guard may re-score affected datasets.
3. Genetic Optimizer optionally proposes pipeline rollback or patch.

## Human-in-the-Loop

ADES is powered by Agentic AI but is not fully unsupervised for high-risk domains:

| Risk tier | Behavior |
|-----------|----------|
| Low | Auto-deploy after Compliance pass |
| Medium | Auto-deploy + async human notification |
| High | Hold deploy until manual approval in orchestration UI |

Configure tiers via `ADES_COMPLIANCE_TIER` and per-dataset tags.

## Expert Review Note

For third-party assessors: the module layout (`agent.py`, `evaluator.py`, `rules_loader.py`, `rules/*/`), tests in `tests/test_compliance_guard.py`, and CI rule validation (`scripts/validate_rules.py`) demonstrate an **extensible Compliance-as-Code architecture** suitable for enterprise rule packs. Sample rules are **demonstrative**, not a certified control baseline. Full assessor guide: [for-expert-review.md](for-expert-review.md).
