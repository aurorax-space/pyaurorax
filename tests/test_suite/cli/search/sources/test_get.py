import pytest
from pyaurorax.cli.cli import cli


@pytest.mark.cli
def test_help(cli_runner):
    result = cli_runner.invoke(cli, "search sources get --help")
    assert result.exit_code == 0
    assert "Usage:" in result.output


@pytest.mark.cli
@pytest.mark.parametrize("program,platform,instrument_type", [
    ["swarm", "swarma", "footprint"],
    ["themis-asi", "gillam", "'panchromatic ASI'"],
])
def test_simple(cli_runner, program, platform, instrument_type):
    result = cli_runner.invoke(cli, "search sources get %s %s %s" % (program, platform, instrument_type))
    assert result.exit_code == 0
    assert result.output != ""


@pytest.mark.cli
@pytest.mark.parametrize("format_value", ["basic_info", "with_metadata", "identifier_only", "full_record"])
def test_format(cli_runner, format_value):
    result = cli_runner.invoke(cli, "search sources get swarm swarma footprint --format=%s" % (format_value))
    assert result.exit_code == 0
    assert result.output != ""


@pytest.mark.cli
def test_include_stats(cli_runner):
    result = cli_runner.invoke(cli, "search sources get swarm swarma footprint --include-stats")
    assert result.exit_code == 0
    assert result.output != ""
