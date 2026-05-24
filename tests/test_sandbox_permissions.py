import os
import stat

import pytest

from src.agent.sandbox import AgentSandbox


@pytest.mark.skipif(os.name == "nt", reason="POSIX permissions only")
def test_sandbox_dirs_use_owner_only_permissions(tmp_path):
    sandbox = AgentSandbox(base_path=str(tmp_path))
    path = sandbox.create("agent-1")

    assert stat.S_IMODE(path.stat().st_mode) == 0o700
