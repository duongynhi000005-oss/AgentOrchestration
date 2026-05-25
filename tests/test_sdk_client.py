import json

from src.sdk.client import OrchestratorClient


class DummyResponse:
    def __init__(self, status, payload):
        self.status = status
        self._payload = payload

    def read(self):
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_request_handles_204_without_json_decode(monkeypatch):
    def fake_urlopen(_):
        return DummyResponse(204, b"")

    monkeypatch.setattr("src.sdk.client.urlopen", fake_urlopen)
    client = OrchestratorClient(base_url="https://example.test", api_key="k")

    assert client.delete_agent("agent-1") == {}


def test_request_decodes_json_payload(monkeypatch):
    def fake_urlopen(_):
        return DummyResponse(200, json.dumps({"ok": True}).encode())

    monkeypatch.setattr("src.sdk.client.urlopen", fake_urlopen)
    client = OrchestratorClient(base_url="https://example.test", api_key="k")

    assert client.get_agent("agent-1") == {"ok": True}
