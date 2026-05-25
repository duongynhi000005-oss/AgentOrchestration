import json

import pytest

from src.sdk.client import OrchestratorClient


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self._payload).encode()


def test_register_agent_rejects_blank_name(monkeypatch):
    called = False

    def fake_urlopen(_req):
        nonlocal called
        called = True
        return _FakeResponse({})

    monkeypatch.setattr("src.sdk.client.urlopen", fake_urlopen)
    client = OrchestratorClient(base_url="https://example.test", api_key="token")

    with pytest.raises(ValueError, match="agent name is required"):
        client.register_agent("   ", "worker.processor")

    assert called is False


def test_register_agent_trims_name_before_submit(monkeypatch):
    captured = {}

    def fake_urlopen(req):
        captured["url"] = req.full_url
        captured["method"] = req.method
        captured["body"] = json.loads(req.data.decode())
        return _FakeResponse({"agent_id": "agent-1", "status": "registered"})

    monkeypatch.setattr("src.sdk.client.urlopen", fake_urlopen)
    client = OrchestratorClient(base_url="https://example.test", api_key="token")

    result = client.register_agent("  test-agent  ", "worker.processor", {"foo": "bar"})

    assert result == {"agent_id": "agent-1", "status": "registered"}
    assert captured["url"] == "https://example.test/api/v2/agents"
    assert captured["method"] == "POST"
    assert captured["body"] == {
        "name": "test-agent",
        "agent_type": "worker.processor",
        "config": {"foo": "bar"},
    }

def test_register_agent_rejects_non_mapping_config(monkeypatch):
    called = False

    def fake_urlopen(_req):
        nonlocal called
        called = True
        return _FakeResponse({})

    monkeypatch.setattr("src.sdk.client.urlopen", fake_urlopen)
    client = OrchestratorClient(base_url="https://example.test", api_key="token")

    with pytest.raises(ValueError, match="agent config must be a mapping"):
        client.register_agent("test-agent", "worker.processor", ["bad"])

    with pytest.raises(ValueError, match="agent config must be a mapping"):
        client.register_agent("test-agent", "worker.processor", "bad")

    assert called is False


def test_register_agent_defaults_config_to_empty_object(monkeypatch):
    captured = {}

    def fake_urlopen(req):
        captured["body"] = json.loads(req.data.decode())
        return _FakeResponse({"agent_id": "agent-2", "status": "registered"})

    monkeypatch.setattr("src.sdk.client.urlopen", fake_urlopen)
    client = OrchestratorClient(base_url="https://example.test", api_key="token")

    result = client.register_agent("test-agent", "worker.processor")

    assert result == {"agent_id": "agent-2", "status": "registered"}
    assert captured["body"]["config"] == {}
