import pytest

from src.cli.main import cli


def test_cli_rejects_unsupported_output_mode(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        ["ao", "--output", "xml", "status"],
    )

    with pytest.raises(SystemExit) as exc:
        cli()

    assert exc.value.code == 2
    err = capsys.readouterr().err
    assert "invalid choice" in err
