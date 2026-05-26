import pytest

from src.sdk.client import OrchestratorClient


class TestOrchestratorClient:
    def test_register_agent_rejects_non_mapping_config(self):
        client = OrchestratorClient(base_url="http://example.com", api_key="k")

        with pytest.raises(TypeError):
            client.register_agent("agent", "worker.processor", config=["bad"])

    def test_register_agent_maps_none_to_empty_object(self, monkeypatch):
        client = OrchestratorClient(base_url="http://example.com", api_key="k")

        captured = {}

        def fake_request(method, path, data=None):
            captured["method"] = method
            captured["path"] = path
            captured["data"] = data
            return {"ok": True}

        client._request = fake_request

        client.register_agent("agent", "worker.processor", config=None)

        assert captured["data"]["config"] == {}
