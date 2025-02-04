import pytest
from pyaurorax.cli.cli import cli


@pytest.mark.cli
def test_help(cli_runner):
    result = cli_runner.invoke(cli, "search data_products search_resubmit --help")
    assert result.exit_code == 0
    assert "Usage:" in result.output


@pytest.mark.cli
def test_simple(cli_runner, data_products_search_id):
    # get the data
    result = cli_runner.invoke(cli, "search data_products search_resubmit %s" % (data_products_search_id))
    assert result.exit_code == 0
    assert result.stdout != ""


@pytest.mark.cli
def test_bad_request_id(cli_runner):
    # get the data
    result = cli_runner.invoke(cli, "search data_products search_resubmit some-bad-request-id")
    assert result.exit_code == 1
    assert "request ID not found" in result.stdout
