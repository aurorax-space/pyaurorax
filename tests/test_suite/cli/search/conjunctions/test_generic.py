import pytest
from pyaurorax.cli.cli import cli


@pytest.mark.cli
def test_help(cli_runner):
    result = cli_runner.invoke(cli, "search conjunctions --help")
    assert result.exit_code == 0
    assert "Usage:" in result.output
