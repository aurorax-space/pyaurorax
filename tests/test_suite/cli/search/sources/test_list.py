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
