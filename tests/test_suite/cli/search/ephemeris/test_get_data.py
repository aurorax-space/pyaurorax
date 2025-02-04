import os
import random
import string
import pytest
from pyaurorax.cli.cli import cli


@pytest.mark.cli
def test_help(cli_runner):
    result = cli_runner.invoke(cli, "search ephemeris get_data --help")
    assert result.exit_code == 0
    assert "Usage:" in result.output


@pytest.mark.cli
def test_simple(cli_runner, ephemeris_search_id):
    # get the data
    result = cli_runner.invoke(cli, "search ephemeris get_data %s" % (ephemeris_search_id))
    assert result.exit_code == 0
    assert "Checking request status" in result.stdout

    # cleanup
    expected_output_filename = "%s_data.json" % (ephemeris_search_id)
    if (os.path.exists(expected_output_filename)):
        os.remove(expected_output_filename)


@pytest.mark.cli
def test_with_outfile(cli_runner, ephemeris_search_id):
    # get the data
    output_filename = "/tmp/pyaurorax_testing_%s_data.json" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    result = cli_runner.invoke(cli, "search ephemeris get_data %s --outfile=%s" % (ephemeris_search_id, output_filename))
    assert result.exit_code == 0
    assert "Checking request status" in result.stdout

    # cleanup
    if (os.path.exists(output_filename)):
        os.remove(output_filename)


@pytest.mark.cli
def test_with_outfile_indent(cli_runner, ephemeris_search_id):
    # get the data
    output_filename = "/tmp/pyaurorax_testing_%s_data.json" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    result = cli_runner.invoke(cli, "search ephemeris get_data %s --outfile=%s --indent=2" % (ephemeris_search_id, output_filename))
    assert result.exit_code == 0
    assert "Checking request status" in result.stdout

    # cleanup
    if (os.path.exists(output_filename)):
        os.remove(output_filename)


@pytest.mark.cli
def test_with_outfile_minify(cli_runner, ephemeris_search_id):
    # get the data
    output_filename = "/tmp/pyaurorax_testing_%s_data.json" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    result = cli_runner.invoke(cli, "search ephemeris get_data %s --outfile=%s --minify" % (ephemeris_search_id, output_filename))
    assert result.exit_code == 0
    assert "Checking request status" in result.stdout

    # cleanup
    if (os.path.exists(output_filename)):
        os.remove(output_filename)


@pytest.mark.cli
@pytest.mark.parametrize("arg_value", ["dict", "objects"])
def test_output_to_terminal(cli_runner, ephemeris_search_id, arg_value):
    # get the data
    result = cli_runner.invoke(cli, "search ephemeris get_data %s --output-to-terminal=%s" % (ephemeris_search_id, arg_value))
    assert result.exit_code == 0
    assert "Checking request status" in result.stdout
