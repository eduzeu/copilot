"""Best-effort, privacy-safe product metrics for Datadog."""

from datadog import DogStatsd

from app.core.config import settings


_client = DogStatsd(
    host=settings.dd_agent_host,
    port=settings.dd_dogstatsd_port,
    namespace="career_copilot",
    constant_tags=[
        f"service:{settings.dd_service}",
        f"env:{settings.dd_env}",
    ],
)


def increment(metric: str, *, tags: list[str] | None = None, value: int = 1) -> None:
    """Increment a counter without allowing telemetry failures to affect requests."""
    if not settings.metrics_enabled:
        return
    try:
        _client.increment(metric, value=value, tags=tags or [])
    except Exception:
        return


def gauge(metric: str, value: float, *, tags: list[str] | None = None) -> None:
    """Record a gauge without allowing telemetry failures to affect requests."""
    if not settings.metrics_enabled:
        return
    try:
        _client.gauge(metric, value, tags=tags or [])
    except Exception:
        return
