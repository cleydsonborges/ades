"""
Sentinel Agent — runtime monitoring for schema drift, access anomalies, and exfiltration patterns.

Feeds failure signatures to the Genetic Optimizer and escalates to Compliance Guard
when behavior deviates from established compliant baselines.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class AlertSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class FailureSignature:
    """Context package for self-healing and audit."""

    dag_id: str
    run_id: str
    task_id: str
    error_type: str
    payload: dict[str, Any]


@dataclass
class SentinelAlert:
    alert_id: str
    severity: AlertSeverity
    detection_class: str
    message: str
    failure_signature: FailureSignature | None = None


class SentinelAgent:
    """
    Monitors pipeline telemetry and data access paths in near real time.

    Integrates with Airflow callbacks, warehouse audit logs, and optional SIEM exports.
    """

    # Phase 3: Champion/Challenger fraud routing
    _volume_threshold: int = 10_000
    _off_hours_start: int = 22

    def ingest_telemetry(self, event: dict[str, Any]) -> list[SentinelAlert]:
        """
        Process a telemetry event; return alerts for anomalous patterns.

        Phase 1: rule-based stubs (volume spike, off-hours access).
        """
        alerts: list[SentinelAlert] = []
        event_type = event.get("event_type", "access")
        row_count = event.get("row_count", 0)
        hour = event.get("hour_utc", 12)

        if event_type == "data_access" and row_count > self._volume_threshold:
            alerts.append(
                SentinelAlert(
                    alert_id=str(uuid.uuid4()),
                    severity=AlertSeverity.HIGH,
                    detection_class="volume_spike",
                    message=f"Row count {row_count} exceeds threshold {self._volume_threshold}",
                )
            )

        if event_type == "data_access" and hour >= self._off_hours_start:
            alerts.append(
                SentinelAlert(
                    alert_id=str(uuid.uuid4()),
                    severity=AlertSeverity.MEDIUM,
                    detection_class="off_hours_access",
                    message=f"Access at hour_utc={hour} outside business window",
                )
            )

        return alerts

    def on_task_failure(
        self,
        dag_id: str,
        run_id: str,
        task_id: str,
        context: dict[str, Any],
    ) -> FailureSignature:
        """Build a FailureSignature for Genetic Optimizer / Code Generator."""
        return FailureSignature(
            dag_id=dag_id,
            run_id=run_id,
            task_id=task_id,
            error_type=context.get("error_type", "unknown"),
            payload=context,
        )
