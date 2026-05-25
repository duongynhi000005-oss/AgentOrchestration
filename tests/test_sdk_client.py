from unittest.mock import patch

from src.sdk.client import OrchestratorClient


class _Response:
    def __init__(self, payload: bytes, status: int = 200):
        self.payload = payload
        self.status = status

    def read(self) -> bytes:
        return self.payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_request_returns_empty_result_for_204_response():
    client = OrchestratorClient(base_url="https://example.test", api_key="token")
    with patch("src.sdk.client.urlopen", return_value=_Response(b"", status=204)):
        assert client.delete_agent("agent-123") == {}


def test_request_decodes_json_response_body():
    client = OrchestratorClient(base_url="https://example.test", api_key="token")
    with patch("src.sdk.client.urlopen", return_value=_Response(b'{\"ok\": true}')):
        assert client.get_agent("agent-123") == {"ok": True}
