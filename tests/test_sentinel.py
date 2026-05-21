"""Sentinel agent tests."""

from src.agents.sentinel.agent import AlertSeverity, SentinelAgent


def test_on_task_failure_builds_signature():
    agent = SentinelAgent()
    sig = agent.on_task_failure("d", "r", "t", {"error_type": "timeout"})
    assert sig.dag_id == "d"
    assert sig.error_type == "timeout"


def test_ingest_telemetry_volume_alert():
    agent = SentinelAgent()
    alerts = agent.ingest_telemetry(
        {"event_type": "data_access", "row_count": 50_000, "hour_utc": 10}
    )
    assert len(alerts) == 1
    assert alerts[0].severity == AlertSeverity.HIGH
