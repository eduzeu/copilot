from app.core import metrics
from app.core.config import settings


class FakeDogStatsd:
    def __init__(self):
        self.calls = []

    def increment(self, metric, value=1, tags=None):
        self.calls.append(("increment", metric, value, tags))

    def gauge(self, metric, value, tags=None):
        self.calls.append(("gauge", metric, value, tags))


def test_metrics_are_disabled_by_default(monkeypatch):
    client = FakeDogStatsd()
    monkeypatch.setattr(metrics, "_client", client)
    monkeypatch.setattr(settings, "metrics_enabled", False)

    metrics.increment("ai.requests", tags=["status:completed"])

    assert client.calls == []


def test_metrics_emit_without_sensitive_tags(monkeypatch):
    client = FakeDogStatsd()
    monkeypatch.setattr(metrics, "_client", client)
    monkeypatch.setattr(settings, "metrics_enabled", True)

    metrics.increment("coach.interactions", tags=["mode:weekly_plan", "fallback:true"])
    metrics.gauge("pipeline.size", 4, tags=["status:interview"])

    assert client.calls == [
        ("increment", "coach.interactions", 1, ["mode:weekly_plan", "fallback:true"]),
        ("gauge", "pipeline.size", 4, ["status:interview"]),
    ]
