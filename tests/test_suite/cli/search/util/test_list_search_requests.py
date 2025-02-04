import pytest
from pyaurorax.cli.cli import cli


@pytest.mark.cli
def test_help(cli_runner):
    result = cli_runner.invoke(cli, "search util list_search_requests --help")
    assert result.exit_code == 0
    assert "Usage:" in result.output


@pytest.mark.cli
def test_simple(cli_runner, api_key):
    result = cli_runner.invoke(cli, ("--api-base-url=https://api.staging.aurorax.space --api-key=%s " +
                                     "search util list_search_requests --start=2024-01-01T00:00:00 --end=2024-01-31T23:59:59") % (api_key))
    assert result.exit_code == 0


@pytest.mark.cli
def test_active(cli_runner, api_key):
    result = cli_runner.invoke(cli, ("--api-base-url=https://api.staging.aurorax.space --api-key=%s " +
                                     "search util list_search_requests --active") % (api_key))
    assert result.exit_code == 0
