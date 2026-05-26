from fastapi.testclient import TestClient

from src.api.server import create_app


def test_api_v2_requires_matching_bearer_token(monkeypatch):
    monkeypatch.setenv("AO_API_KEY", "secret-token")
    client = TestClient(create_app())

    res = client.get("/api/v2/agents", headers={"Authorization": "Bearer nope"})
    assert res.status_code == 401


def test_api_v2_accepts_matching_bearer_token(monkeypatch):
    monkeypatch.setenv("AO_API_KEY", "secret-token")
    client = TestClient(create_app())

    res = client.get("/api/v2/agents", headers={"Authorization": "Bearer secret-token"})
    assert res.status_code == 200
