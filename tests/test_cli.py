import pytest

from src.cli.main import cli


def test_cli_rejects_unsupported_output_mode(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["ao", "--output", "xml", "status"],
    )

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 2
