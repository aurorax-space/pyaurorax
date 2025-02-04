import pytest
from pyaurorax.cli.cli import cli


@pytest.mark.cli
def test_help(cli_runner):
    result = cli_runner.invoke(cli, "search conjunctions get_logs --help")
    assert result.exit_code == 0
    assert "Usage:" in result.output


@pytest.mark.cli
def test_simple(cli_runner, conjunction_search_id):
    # get the data
    result = cli_runner.invoke(cli, "search conjunctions get_logs %s" % (conjunction_search_id))
    assert result.exit_code == 0
    assert result.stdout != ""


@pytest.mark.cli
def test_bad_request_id(cli_runner):
    # get the data
    result = cli_runner.invoke(cli, "search conjunctions get_logs some-bad-request-id")
    assert result.exit_code == 1
    assert "request ID not found" in result.stdout


@pytest.mark.cli
@pytest.mark.parametrize("filter_param", ["debug", "info", "warn", "error"])
def test_filter_logs(cli_runner, conjunction_search_id, filter_param):
    # get the data
    result = cli_runner.invoke(cli, "search conjunctions get_logs %s --filter=%s" % (conjunction_search_id, filter_param))
    assert result.exit_code == 0
    assert result.stdout != ""


@pytest.mark.cli
def test_table_max_width(cli_runner, conjunction_search_id):
    # get the data
    result = cli_runner.invoke(cli, "search conjunctions get_logs %s --table-max-width=100" % (conjunction_search_id))
    assert result.exit_code == 0
    assert result.stdout != ""


@pytest.mark.cli
def test_no_truncate(cli_runner, conjunction_search_id):
    # get the data
    result = cli_runner.invoke(cli, "search conjunctions get_logs %s --no-truncate" % (conjunction_search_id))
    assert result.exit_code == 0
    assert result.stdout != ""
