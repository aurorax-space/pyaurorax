import pytest
from pyaurorax.cli.cli import cli


@pytest.mark.cli
def test_help(cli_runner):
    result = cli_runner.invoke(cli, "search sources list --help")
    assert result.exit_code == 0
    assert "Usage:" in result.output


@pytest.mark.cli
def test_simple(cli_runner):
    result = cli_runner.invoke(cli, "search sources list")
    assert result.exit_code == 0
    assert result.output != ""


@pytest.mark.cli
def test_reversed(cli_runner):
    result = cli_runner.invoke(cli, "search sources list --reversed")
    assert result.exit_code == 0
    assert result.output != ""


@pytest.mark.cli
@pytest.mark.parametrize("test_dict", [
    {
        "program": "swarm"
    },
    {
        "platform": "gillam"
    },
    {
        "instrument_type": "'RGB ASI'"
    },
    {
        "source_type": "ground"
    },
    {
        "owner": "dchaddoc@ucalgary.ca"
    },
])
def test_filters(cli_runner, test_dict):
    # construct args
    args = []
    if ("program" in test_dict):
        args.append("--program=%s" % (test_dict["program"]))
    if ("platform" in test_dict):
        args.append("--platform=%s" % (test_dict["platform"]))
    if ("instrument_type" in test_dict):
        args.append("--instrument-type=%s" % (test_dict["instrument_type"]))
    if ("source_type" in test_dict):
        args.append("--source-type=%s" % (test_dict["source_type"]))
    if ("owner" in test_dict):
        args.append("--owner=%s" % (test_dict["owner"]))

    # do command
    result = cli_runner.invoke(cli, "search sources list %s" % (' '.join(args)))
    assert result.exit_code == 0
    assert result.output != ""


@pytest.mark.cli
@pytest.mark.parametrize("order_value", ["identifier", "program", "platform", "instrument_type", "display_name", "owner"])
def test_order(cli_runner, order_value):
    result = cli_runner.invoke(cli, "search sources list --order=%s" % (order_value))
    assert result.exit_code == 0
    assert result.output != ""


@pytest.mark.cli
def test_include_stats(cli_runner):
    result = cli_runner.invoke(cli, "search sources list --include-stats")
    assert result.exit_code == 0
    assert result.output != ""
