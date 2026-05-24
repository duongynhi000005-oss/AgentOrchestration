from src.sdk.client import OrchestratorClient


class FakeResponse:
    def __init__(self, status, body=b""):
        self.status = status
        self._body = body

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_request_returns_empty_dict_for_204(monkeypatch):
    client = OrchestratorClient(base_url="https://example.test", api_key="token")

    def fake_urlopen(_request):
        return FakeResponse(204)

    monkeypatch.setattr("src.sdk.client.urlopen", fake_urlopen)

    assert client.delete_agent("agent-123") == {}
