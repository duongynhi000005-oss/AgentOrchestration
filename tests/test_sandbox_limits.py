import pytest

from src.agent.sandbox import ResourceLimits


@pytest.mark.parametrize(
    "kwargs",
    [
        {"cpu_time": 0},
        {"cpu_time": -1},
        {"memory_mb": 0},
        {"disk_mb": -5},
        {"memory_mb": 1.5},
        {"disk_mb": True},
    ],
)
def test_resource_limits_reject_invalid_values(kwargs):
    with pytest.raises(ValueError):
        ResourceLimits(**kwargs)


def test_resource_limits_accepts_positive_integers():
    limits = ResourceLimits(cpu_time=10, memory_mb=256, disk_mb=128)

    assert limits.cpu_time == 10
    assert limits.memory_mb == 256
    assert limits.disk_mb == 128
