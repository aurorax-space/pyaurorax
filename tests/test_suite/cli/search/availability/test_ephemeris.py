import pytest
from pyaurorax.cli.cli import cli


@pytest.mark.cli
def test_help(cli_runner):
    result = cli_runner.invoke(cli, "search availability --help")
    assert result.exit_code == 0
    assert "Usage:" in result.output


@pytest.mark.cli
def test_ephemeris_help(cli_runner):
    result = cli_runner.invoke(cli, "search availability ephemeris --help")
    assert result.exit_code == 0
    assert "Usage:" in result.output


@pytest.mark.cli
@pytest.mark.parametrize("test_dict", [
    {
        "start": "2022/01/01",
        "end": "2022/01/01"
    },
    {
        "start": "2022-01-01",
        "end": "2022-01-01"
    },
    {
        "start": "20220101",
        "end": "20220101"
    },
])
def test_ephemeris_basic(cli_runner, test_dict):
    result = cli_runner.invoke(cli, "search availability ephemeris %s %s" % (test_dict["start"], test_dict["end"]))
    assert result.exit_code == 0
    assert "Available Records" in result.output


@pytest.mark.cli
@pytest.mark.parametrize("test_dict", [
    {
        "start": "2022/01/01",
        "end": "202201",
        "message": "Error parsing end date, make sure it is in a valid format shown in help menu",
    },
    {
        "start": "202201",
        "end": "2022-01-01",
        "message": "Error parsing start date, make sure it is in a valid format shown in help menu",
    },
])
def test_ephemeris_bad_date_format(cli_runner, test_dict):
    result = cli_runner.invoke(cli, "search availability ephemeris %s %s" % (test_dict["start"], test_dict["end"]))
    assert result.exit_code == 1
    assert test_dict["message"] in result.output


@pytest.mark.cli
def test_ephemeris_no_data(cli_runner):
    result = cli_runner.invoke(cli, "search availability ephemeris 2022/01/01 2022/01/01 --program=something-that-doesnt-exist")
    assert result.exit_code == 0
    assert "No ephemeris availability information found" in result.output


@pytest.mark.cli
def test_ephemeris_with_program(cli_runner):
    result = cli_runner.invoke(cli, "search availability ephemeris 2022/01/01 2022/01/01 --program=swarm")
    assert result.exit_code == 0
    assert "Available Records" in result.output


@pytest.mark.cli
def test_ephemeris_with_platform(cli_runner):
    result = cli_runner.invoke(cli, "search availability ephemeris 2022/01/01 2022/01/01 --platform=gillam")
    assert result.exit_code == 0
    assert "Available Records" in result.output


@pytest.mark.cli
def test_ephemeris_with_instrument_type(cli_runner):
    result = cli_runner.invoke(cli, "search availability ephemeris 2022/01/01 2022/01/01 --instrument-type='RGB ASI'")
    assert result.exit_code == 0
    assert "Available Records" in result.output


@pytest.mark.cli
def test_ephemeris_with_source_type(cli_runner):
    result = cli_runner.invoke(cli, "search availability ephemeris 2022/01/01 2022/01/01 --source-type=heo")
    assert result.exit_code == 0
    assert "Available Records" in result.output


@pytest.mark.cli
@pytest.mark.parametrize("order_value", [
    "identifier",
    "program",
    "platform",
    "instrument_type",
    "source_type",
    "display_name",
])
def test_ephemeris_order(cli_runner, order_value):
    result = cli_runner.invoke(cli, "search availability ephemeris 2022/01/01 2022/01/01 --order=%s" % (order_value))
    assert result.exit_code == 0
    assert "Available Records" in result.output


@pytest.mark.cli
def test_ephemeris_reversed(cli_runner):
    result = cli_runner.invoke(cli, "search availability ephemeris 2022/01/01 2022/01/01 --order=identifier --reversed")
    assert result.exit_code == 0
    assert "Available Records" in result.output
