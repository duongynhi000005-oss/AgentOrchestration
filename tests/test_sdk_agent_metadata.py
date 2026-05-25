import pytest

from src.sdk.agent import BaseAgent


class _Agent(BaseAgent):
    async def setup(self) -> None:
        return None

    async def handle_task(self, task):
        return task

    async def cleanup(self) -> None:
        return None


def test_set_metadata_rejects_empty_key():
    agent = _Agent(agent_id="a1", name="agent")
    with pytest.raises(ValueError):
        agent.set_metadata("", "value")


def test_set_metadata_accepts_non_empty_key():
    agent = _Agent(agent_id="a1", name="agent")
    agent.set_metadata("env", "prod")
    assert agent.get_metadata("env") == "prod"
