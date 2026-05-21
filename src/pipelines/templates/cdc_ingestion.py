"""
CDC ingestion template — change-data-capture to curated zone.

Template consumed by Code Generator when objectives match CDC patterns.
Includes partitioning, deduplication, and Compliance Guard PII hooks.
"""

TEMPLATE_ID = "cdc_ingestion"
DESCRIPTION = "Autonomous CDC from operational DB to lakehouse curated layer."

DEFAULT_OBJECTIVE = (
    "Ingest CDC events from source, deduplicate by key, apply SCD Type 2, load to curated."
)

PARAMETERS_SCHEMA = {
    "source_connection": "str",
    "target_dataset": "str",
    "primary_key": "list[str]",
    "pii_columns": "list[str]",
}
