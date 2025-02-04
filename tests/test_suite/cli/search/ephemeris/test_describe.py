import pytest
from pyaurorax.cli.cli import cli


@pytest.mark.cli
def test_help(cli_runner):
    result = cli_runner.invoke(cli, "search ephemeris describe --help")
    assert result.exit_code == 0
    assert "Usage:" in result.output


@pytest.mark.cli
@pytest.mark.parametrize("json_filename", [
    "example1.json",
    "example2.json",
])
def test_simple(cli_runner, json_filename):
    result = cli_runner.invoke(cli, "search ephemeris describe examples/queries/search/ephemeris/%s" % (json_filename))
    assert result.exit_code == 0
    assert len(result.stdout) > 0


@pytest.mark.cli
def test_bad_file(cli_runner):
    result = cli_runner.invoke(cli, "search ephemeris describe some-bad-file.json")
    assert result.exit_code == 1
    assert "infile doesn't exist" in result.stdout
