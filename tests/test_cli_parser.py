import pytest

from src.cli.main import build_parser


def test_cli_parser_accepts_supported_output_mode():
    parser = build_parser()
    args = parser.parse_args(["--output", "json", "status"])
    assert args.output == "json"
    assert args.command == "status"


def test_cli_parser_rejects_unsupported_output_mode():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["--output", "xml", "status"])
