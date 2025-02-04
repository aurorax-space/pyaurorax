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
