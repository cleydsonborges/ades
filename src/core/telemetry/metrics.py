"""
Metrics schema aligned with professional plan KPIs (§6).

Export to Prometheus/OpenTelemetry planned for production deployments.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PlanMetrics:
    """Unified vision §6 measurable goals."""

    retrieval_efficiency_pct: float | None = None
    processing_time_reduction_pct: float | None = None
    pipeline_uptime_pct: float | None = None
    data_accuracy_pct: float | None = None
    threat_neutralization_ms: float | None = None
    manual_hours_saved: float | None = None
    labels: dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    """In-memory metrics collector for Phase 1."""

    def __init__(self) -> None:
        self._samples: list[dict[str, Any]] = []

    def record(self, metrics: PlanMetrics) -> None:
        self._samples.append(
            {
                "retrieval_efficiency_pct": metrics.retrieval_efficiency_pct,
                "processing_time_reduction_pct": metrics.processing_time_reduction_pct,
                "pipeline_uptime_pct": metrics.pipeline_uptime_pct,
                "data_accuracy_pct": metrics.data_accuracy_pct,
                "threat_neutralization_ms": metrics.threat_neutralization_ms,
                "manual_hours_saved": metrics.manual_hours_saved,
                "labels": metrics.labels,
            }
        )

    def export_prometheus_lines(self) -> list[str]:
        lines: list[str] = []
        for i, s in enumerate(self._samples):
            for key, val in s.items():
                if key == "labels" or val is None:
                    continue
                lines.append(f'ades_{key}{{sample="{i}"}} {val}')
        return lines

    @property
    def sample_count(self) -> int:
        return len(self._samples)
