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
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert "Welcome to the PyAuroraX CLI program" in result.output


@pytest.mark.cli
def test_version(cli_runner):
    result = cli_runner.invoke(cli, "--version")
    assert result.exit_code == 0
    assert "version" in result.output


@pytest.mark.cli
def test_args_api_key(cli_runner):
    result = cli_runner.invoke(cli, "--api-key=some_API_key")
    assert result.exit_code == 0


@pytest.mark.cli
def test_args_api_base_url(cli_runner):
    result = cli_runner.invoke(cli, "--api-base-url=https://someurl.com")
    assert result.exit_code == 0


@pytest.mark.cli
def test_args_verbose(cli_runner):
    result = cli_runner.invoke(cli, "--verbose")
    assert result.exit_code == 0


@pytest.mark.cli
def test_test_connectivity(cli_runner):
    result = cli_runner.invoke(cli, "--test-connectivity")
    assert result.exit_code == 0
    assert "Connectivity to the AuroraX API looks good" in result.output


@pytest.mark.cli
def test_test_connectivity_bad(cli_runner):
    result = cli_runner.invoke(cli, "--api-base-url=https://aurora.phys.ucalgary.ca/api_testing_url --test-connectivity")
    assert result.exit_code == 1
    assert "Error connecting to AuroraX API" in result.stdout
