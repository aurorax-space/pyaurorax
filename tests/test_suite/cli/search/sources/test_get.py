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
    result = cli_runner.invoke(cli, "search sources get --help")
    assert result.exit_code == 0
    assert "Usage:" in result.output


@pytest.mark.cli
@pytest.mark.parametrize("program,platform,instrument_type", [
    ["swarm", "swarma", "footprint"],
    ["themis-asi", "gillam", "'panchromatic ASI'"],
])
def test_simple(cli_runner, program, platform, instrument_type):
    result = cli_runner.invoke(cli, "search sources get %s %s %s" % (program, platform, instrument_type))
    assert result.exit_code == 0
    assert result.output != ""


@pytest.mark.cli
@pytest.mark.parametrize("format_value", ["basic_info", "with_metadata", "identifier_only", "full_record"])
def test_format1(cli_runner, format_value):
    result = cli_runner.invoke(cli, "search sources get swarm swarma footprint --format=%s" % (format_value))
    assert result.exit_code == 0
    assert result.output != ""


@pytest.mark.cli
@pytest.mark.parametrize("format_value", ["basic_info", "with_metadata", "identifier_only", "full_record"])
def test_format_and_stats1(cli_runner, format_value):
    result = cli_runner.invoke(cli, "search sources get swarm swarma footprint --format=%s --include-stats" % (format_value))
    assert result.exit_code == 0
    assert result.output != ""


@pytest.mark.cli
@pytest.mark.parametrize("format_value", ["basic_info", "with_metadata", "identifier_only", "full_record"])
def test_format_and_stats2(cli_runner, format_value):
    result = cli_runner.invoke(cli, "search sources get auroramax yellowknife 'DSLR' --format=%s --include-stats" % (format_value))
    assert result.exit_code == 0
    assert result.output != ""


@pytest.mark.cli
def test_include_stats1(cli_runner):
    result = cli_runner.invoke(cli, "search sources get swarm swarma footprint --include-stats")
    assert result.exit_code == 0
    assert result.output != ""


@pytest.mark.cli
def test_include_stats2(cli_runner):
    result = cli_runner.invoke(cli, "search sources get auroramax yellowknife 'DSLR' --include-stats")
    assert result.exit_code == 0
    assert result.output != ""
