import pytest

from src.sdk.agent import BaseAgent


class DummyAgent(BaseAgent):
    async def setup(self) -> None:
        return None

    async def handle_task(self, task):
        return task

    async def cleanup(self) -> None:
        return None


class TestBaseAgentMetadata:
    def test_set_metadata_rejects_empty_key(self):
        agent = DummyAgent("id-1", "demo")

        with pytest.raises(ValueError):
            agent.set_metadata("", "value")

    def test_set_metadata_accepts_non_empty_key(self):
        agent = DummyAgent("id-1", "demo")

        agent.set_metadata("role", "worker")

        assert agent.get_metadata("role") == "worker"
