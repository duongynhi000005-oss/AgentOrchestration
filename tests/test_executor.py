import pytest

from src.agent.executor import AgentExecutor


class TestAgentExecutor:
    def test_init_rejects_non_positive_max_concurrent(self):
        with pytest.raises(ValueError, match="positive integer"):
            AgentExecutor(max_concurrent=0)

        with pytest.raises(ValueError, match="positive integer"):
            AgentExecutor(max_concurrent=-1)

    def test_init_accepts_positive_max_concurrent(self):
        executor = AgentExecutor(max_concurrent=2)
        assert executor.max_concurrent == 2
