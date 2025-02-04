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

import pytest
from pyaurorax.cli.cli import cli


@pytest.mark.cli
def test_help(cli_runner):
    result = cli_runner.invoke(cli, "search conjunctions describe --help")
    assert result.exit_code == 0
    assert "Usage:" in result.output


@pytest.mark.cli
@pytest.mark.parametrize("json_filename", [
    "example1.json",
    "example2.json",
    "example3.json",
    "example4.json",
    "example5.json",
    "example6.json",
    "example7.json",
])
def test_simple(cli_runner, json_filename):
    result = cli_runner.invoke(cli, "search conjunctions describe examples/queries/search/conjunctions/%s" % (json_filename))
    assert result.exit_code == 0
    assert len(result.stdout) > 0


@pytest.mark.cli
def test_bad_file(cli_runner):
    result = cli_runner.invoke(cli, "search ephemeris describe some-bad-file.json")
    assert result.exit_code == 1
    assert "infile doesn't exist" in result.stdout
