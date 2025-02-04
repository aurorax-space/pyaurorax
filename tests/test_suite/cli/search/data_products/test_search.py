# Copyright 2024 University of Calgary
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import random
import string
import pytest
from pyaurorax.cli.cli import cli


@pytest.mark.cli
def test_help(cli_runner):
    result = cli_runner.invoke(cli, "search data_products search --help")
    assert result.exit_code == 0
    assert "Usage:" in result.output


@pytest.mark.cli
def test_default_file_several_options(cli_runner, data_products_search_input_filename):
    # get the data
    result = cli_runner.invoke(cli, "search data_products search %s --poll-interval=1 --indent=4" % (data_products_search_input_filename))
    assert result.exit_code == 0

    # extract the filename from the output
    extracted_filename = None
    for line in result.stdout.split('\n'):
        line = line.strip()
        if ("Request ID" in line):
            line_split = line.split()
            extracted_filename = "%s_data.json" % (line_split[-1])

    # remove the file
    if (extracted_filename is not None and os.path.exists(extracted_filename)):
        os.remove(extracted_filename)


@pytest.mark.cli
def test_bad_input_file(cli_runner):
    # get the data
    result = cli_runner.invoke(cli, "search data_products search some-bad-file.json")
    assert result.exit_code == 1
    assert "infile doesn't exist" in result.stdout


@pytest.mark.cli
@pytest.mark.parametrize("arg_value", ["dict", "objects"])
def test_output_to_terminal(cli_runner, data_products_search_input_filename, arg_value):
    # get the data
    result = cli_runner.invoke(cli, "search data_products search %s --output-to-terminal=%s --quiet" % (
        data_products_search_input_filename,
        arg_value,
    ))
    assert result.exit_code == 0
    assert result.stdout != ""


@pytest.mark.cli
def test_output_file(cli_runner, data_products_search_input_filename):
    # get the data
    output_filename = "/tmp/pyaurorax_testing_%s_data.json" % (''.join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    result = cli_runner.invoke(cli, "search data_products search %s --outfile=%s --minify" % (
        data_products_search_input_filename,
        output_filename,
    ))
    assert result.exit_code == 0
    assert result.stdout != ""

    # cleanup
    if (os.path.exists(output_filename)):
        os.remove(output_filename)
