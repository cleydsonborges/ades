"""
Metadata lake interface for semantic schema indexing.

Phase 1: in-memory stub. Phase 2+: Pinecone or other vector DB backend.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class SchemaRecord:
    connection: str
    table: str
    columns: list[dict[str, Any]]
    embedding: list[float] | None = None


class MetadataLake:
    """In-memory metadata store with optional vector placeholder."""

    def __init__(self) -> None:
        self._records: dict[str, SchemaRecord] = {}
        self._vectors: dict[str, list[float]] = {}

    def index(self, record: SchemaRecord) -> str:
        key = f"{record.connection}.{record.table}"
        self._records[key] = record
        if record.embedding:
            self._vectors[key] = record.embedding
        return key

    def search(self, query: str, limit: int = 5) -> list[SchemaRecord]:
        """Keyword search stub; vector similarity deferred to Phase 2."""
        q = query.lower()
        matches = [
            r
            for k, r in self._records.items()
            if q in k.lower() or q in r.table.lower()
        ]
        return matches[:limit]

    def get(self, key: str) -> SchemaRecord | None:
        return self._records.get(key)
