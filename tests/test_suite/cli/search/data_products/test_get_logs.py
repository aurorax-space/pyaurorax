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
    result = cli_runner.invoke(cli, "search data_products get_logs --help")
    assert result.exit_code == 0
    assert "Usage:" in result.output


@pytest.mark.cli
def test_simple(cli_runner, api_url, data_products_search_id):
    # get the data
    result = cli_runner.invoke(cli, "--api-base-url=%s search data_products get_logs %s" % (api_url, data_products_search_id))
    assert result.exit_code == 0
    assert result.stdout != ""


@pytest.mark.cli
def test_bad_request_id(cli_runner):
    # get the data
    result = cli_runner.invoke(cli, "search data_products get_logs some-bad-request-id")
    assert result.exit_code == 1
    assert "request ID not found" in result.stdout


@pytest.mark.cli
@pytest.mark.parametrize("filter_param", ["debug", "info", "warn", "error"])
def test_filter_logs(cli_runner, api_url, data_products_search_id, filter_param):
    # get the data
    result = cli_runner.invoke(cli, "--api-base-url=%s search data_products get_logs %s --filter=%s" % (
        api_url,
        data_products_search_id,
        filter_param,
    ))
    assert result.exit_code == 0
    assert result.stdout != ""


@pytest.mark.cli
def test_table_max_width(cli_runner, api_url, data_products_search_id):
    # get the data
    result = cli_runner.invoke(cli, "--api-base-url=%s search data_products get_logs %s --table-max-width=100" % (
        api_url,
        data_products_search_id,
    ))
    assert result.exit_code == 0
    assert result.stdout != ""
