from pathlib import Path

import pytest

from src.agent.sandbox import AgentSandbox


def test_safe_child_path_stays_inside_sandbox(tmp_path):
    sandbox = AgentSandbox(base_path=str(tmp_path))
    sandbox_path = sandbox.create("agent-1")

    child = sandbox.safe_child_path("agent-1", "logs/output.txt")

    assert child == sandbox_path / "logs" / "output.txt"


def test_safe_child_path_rejects_escape_attempts(tmp_path):
    sandbox = AgentSandbox(base_path=str(tmp_path))
    sandbox.create("agent-1")

    with pytest.raises(ValueError):
        sandbox.safe_child_path("agent-1", "../outside.txt")
