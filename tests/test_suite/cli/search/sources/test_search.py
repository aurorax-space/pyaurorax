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
    result = cli_runner.invoke(cli, "search sources search --help")
    assert result.exit_code == 0
    assert "Usage:" in result.output


@pytest.mark.cli
def test_simple(cli_runner):
    result = cli_runner.invoke(cli, "search sources search")
    assert result.exit_code == 0
    assert result.output != ""


@pytest.mark.cli
def test_reversed(cli_runner):
    result = cli_runner.invoke(cli, "search sources search --reversed")
    assert result.exit_code == 0
    assert result.output != ""


@pytest.mark.cli
@pytest.mark.parametrize("test_dict", [
    {
        "programs": "swarm,themis"
    },
    {
        "programs": "swarm"
    },
    {
        "platforms": "gillam"
    },
    {
        "platforms": "'gillam,rabbit lake'"
    },
    {
        "instrument_types": "footprint"
    },
    {
        "instrument_types": "'RGB ASI,footprint'"
    },
])
def test_filters(cli_runner, test_dict):
    # construct args
    args = []
    if ("programs" in test_dict):
        args.append("--programs=%s" % (test_dict["programs"]))
    if ("platforms" in test_dict):
        args.append("--platforms=%s" % (test_dict["platforms"]))
    if ("instrument_types" in test_dict):
        args.append("--instrument-types=%s" % (test_dict["instrument_types"]))

    # do command
    result = cli_runner.invoke(cli, "search sources search %s" % (' '.join(args)))
    assert result.exit_code == 0
    assert result.output != ""


@pytest.mark.cli
@pytest.mark.parametrize("order_value", ["identifier", "program", "platform", "instrument_type", "display_name", "owner"])
def test_order(cli_runner, order_value):
    result = cli_runner.invoke(cli, "search sources search --order=%s" % (order_value))
    assert result.exit_code == 0
    assert result.output != ""


@pytest.mark.cli
def test_include_stats(cli_runner):
    result = cli_runner.invoke(cli, "search sources search --include-stats")
    assert result.exit_code == 0
    assert result.output != ""


@pytest.mark.cli
def test_stats_and_owner(cli_runner):
    result = cli_runner.invoke(cli, "search sources search --include-stats --order=owner")
    assert result.exit_code == 0
    assert result.output != ""
