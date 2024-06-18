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
import glob
import shutil
import pytest
import pyaurorax
from pathlib import Path
from dotenv import load_dotenv


def pytest_addoption(parser):
    parser.addoption("--api-url", action="store", default="https://api.staging.aurorax.space", help="A specific API URL to use")
    parser.addoption("--api-key", type=str, help="A specific API key to use")


@pytest.fixture(scope="session")
def api_url(request):
    return request.config.getoption("--api-url")


@pytest.fixture
def api_key(request):
    return request.config.getoption("--api-key")


@pytest.fixture(scope="function")
def aurorax(api_url, api_key):
    if (api_key is None):
        load_dotenv("%s/.env" % (os.path.dirname(os.path.realpath(__file__))))
        api_key = os.environ["AURORAX_API_KEY"]
    return pyaurorax.PyAuroraX(api_base_url=api_url, api_key=api_key)


def pytest_sessionstart(session):
    """
    Called before any test is done
    """
    # initial setup
    api_url = session.config.getoption("--api-url")
    api_key = session.config.getoption("--api-key")
    if (api_key is None):
        load_dotenv("%s/.env" % (os.path.dirname(os.path.realpath(__file__))))
        api_key = os.environ["AURORAX_API_KEY"]
    aurorax = pyaurorax.PyAuroraX(api_base_url=api_url, api_key=api_key)

    # create the generic data source that will be used for
    # ephemeris and data products upload/delete tests
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    display_name = "PyAuroraX testing"
    source_type = pyaurorax.search.SOURCE_TYPE_GROUND
    try:
        ds = aurorax.search.sources.get(program, platform, instrument_type)
    except pyaurorax.AuroraXNotFoundError:
        # no data source, need to create it
        ds = pyaurorax.search.DataSource(program=program,
                                         platform=platform,
                                         instrument_type=instrument_type,
                                         display_name=display_name,
                                         source_type=source_type)
        aurorax.search.sources.add(ds)


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    # delete all data testing dirs
    glob_str = "%s/pyaurorax_data_*testing*" % (str(Path.home()))
    path_list = sorted(glob.glob(glob_str))
    for p in path_list:
        shutil.rmtree(p)
