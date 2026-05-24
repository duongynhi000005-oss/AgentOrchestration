import pytest

from src.cli.main import cli


def test_cli_rejects_unknown_output_mode(monkeypatch):
    monkeypatch.setattr("sys.argv", ["ao", "--output", "xml"])

    with pytest.raises(SystemExit):
        cli()
