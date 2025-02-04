import os
import random
import string
import pytest
from pyaurorax.cli.cli import cli


@pytest.mark.cli
def test_help(cli_runner):
    result = cli_runner.invoke(cli, "search data_products search_template --help")
    assert result.exit_code == 0
    assert "Usage:" in result.output


@pytest.mark.cli
def test_simple(cli_runner):
    # get the data
    result = cli_runner.invoke(cli, "search data_products search_template")
    assert result.exit_code == 0
    assert result.stdout != ""


@pytest.mark.cli
def test_with_outfile(cli_runner):
    # get the data
    output_filename = "/tmp/pyaurorax_testing_%s_data.json" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    result = cli_runner.invoke(cli, "search data_products search_template --outfile=%s" % (output_filename))
    assert result.exit_code == 0
    assert result.stdout != ""

    # cleanup
    if (os.path.exists(output_filename)):
        os.remove(output_filename)


@pytest.mark.cli
def test_with_indent(cli_runner):
    # get the data
    result = cli_runner.invoke(cli, "search data_products search_template --indent=2")
    assert result.exit_code == 0
    assert result.stdout != ""
