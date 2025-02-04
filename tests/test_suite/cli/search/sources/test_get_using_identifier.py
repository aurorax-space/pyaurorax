import pytest
from pyaurorax.cli.cli import cli


@pytest.mark.cli
def test_help(cli_runner):
    result = cli_runner.invoke(cli, "search sources get_using_identifier --help")
    assert result.exit_code == 0
    assert "Usage:" in result.output


@pytest.mark.cli
@pytest.mark.parametrize("identifier", [3, 30, 44, 76])
def test_simple(cli_runner, identifier):
    result = cli_runner.invoke(cli, "search sources get_using_identifier %d" % (identifier))
    assert result.exit_code == 0
    assert result.output != ""


@pytest.mark.cli
@pytest.mark.parametrize("format_value", ["basic_info", "with_metadata", "identifier_only", "full_record"])
def test_format(cli_runner, format_value):
    result = cli_runner.invoke(cli, "search sources get_using_identifier 3 --format=%s" % (format_value))
    assert result.exit_code == 0
    assert result.output != ""


@pytest.mark.cli
def test_include_stats(cli_runner):
    result = cli_runner.invoke(cli, "search sources get_using_identifier 3 --include-stats")
    assert result.exit_code == 0
    assert result.output != ""
