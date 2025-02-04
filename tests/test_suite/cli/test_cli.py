import pytest
from pyaurorax.cli.cli import cli


@pytest.mark.cli
def test_help(cli_runner):
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert "Welcome to the PyAuroraX CLI program" in result.output


@pytest.mark.cli
def test_version(cli_runner):
    result = cli_runner.invoke(cli, "--version")
    assert result.exit_code == 0
    assert "version" in result.output


@pytest.mark.cli
def test_args_api_key(cli_runner):
    result = cli_runner.invoke(cli, "--api-key=some_API_key")
    assert result.exit_code == 0


@pytest.mark.cli
def test_args_api_base_url(cli_runner):
    result = cli_runner.invoke(cli, "--api-base-url=https://someurl.com")
    assert result.exit_code == 0


@pytest.mark.cli
def test_args_verbose(cli_runner):
    result = cli_runner.invoke(cli, "--verbose")
    assert result.exit_code == 0


@pytest.mark.cli
def test_test_connectivity(cli_runner):
    result = cli_runner.invoke(cli, "--test-connectivity")
    assert result.exit_code == 0
    assert "Connectivity to the AuroraX API looks good" in result.output


@pytest.mark.cli
def test_test_connectivity_bad(cli_runner):
    result = cli_runner.invoke(cli, "--api-base-url=https://aurora.phys.ucalgary.ca/api_testing_url --test-connectivity")
    assert result.exit_code == 1
    assert "Error connecting to AuroraX API" in result.stdout
