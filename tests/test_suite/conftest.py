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
import copy
import glob
import shutil
import pytest
import datetime
import pyaurorax
import threading
from click.testing import CliRunner
from pathlib import Path
from dotenv import load_dotenv

# globals
CONJUNCTION_SEARCH_REQUEST_ID = None
EPHEMERIS_SEARCH_REQUEST_ID = None
DATA_PRODUCTS_SEARCH_REQUEST_ID = None


def pytest_addoption(parser):
    parser.addoption("--api-url", action="store", default="https://api.staging.aurorax.space", help="A specific API URL to use")
    parser.addoption("--api-key", type=str, help="A specific API key to use")


#---------------------------------------------------
# Fixtures: top level
#---------------------------------------------------
@pytest.fixture(scope="session")
def api_url(request):
    return request.config.getoption("--api-url")


@pytest.fixture(scope="session")
def api_key(request):
    api_key = request.config.getoption("--api-key")
    if (api_key is None):
        load_dotenv("%s/.env" % (os.path.dirname(os.path.realpath(__file__))))
        api_key = os.environ["AURORAX_API_KEY"]
    return api_key


@pytest.fixture(scope="function")
def aurorax(api_url, api_key):
    if (api_key is None):
        load_dotenv("%s/.env" % (os.path.dirname(os.path.realpath(__file__))))
        api_key = os.environ["AURORAX_API_KEY"]
    return pyaurorax.PyAuroraX(api_base_url=api_url, api_key=api_key)


@pytest.fixture(scope="session")
def cli_runner():
    return CliRunner()


#---------------------------------------------------
# Fixtures: conjunction searching
#---------------------------------------------------
@pytest.fixture(scope="session")
def conjunction_search_id():
    return CONJUNCTION_SEARCH_REQUEST_ID


@pytest.fixture(scope="session")
def conjunction_search_input_filename():
    return "%s/../../examples/queries/search/conjunctions/example1.json" % (os.path.dirname(__file__))


@pytest.fixture(scope="session")
def conjunction_search_obj():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # create search object
    start = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end = datetime.datetime(2020, 1, 1, 6, 59, 59)
    distance = 500
    ground = [aurorax.search.GroundCriteriaBlock(programs=["themis-asi"])]
    space = [aurorax.search.SpaceCriteriaBlock(programs=["swarm"])]
    s = aurorax.search.conjunctions.search(start, end, distance, ground=ground, space=space, return_immediately=True)

    # return
    return s


@pytest.fixture(scope="session")
def conjunction_search_dict():
    return {
        "start": "2019-01-01T00:00:00.000Z",
        "end": "2019-01-03T23:59:59.000Z",
        "conjunction_types": ["nbtrace"],
        "ground": [{
            "programs": ["themis-asi"],
            "platforms": ["fort smith", "gillam"],
            "instrument_types": ["panchromatic ASI"],
            "ephemeris_metadata_filters": {}
        }],
        "space": [{
            "programs": ["swarm"],
            "platforms": [],
            "instrument_types": ["footprint"],
            "ephemeris_metadata_filters": {},
            "hemisphere": ["northern"]
        }],
        "events": [],
        "max_distances": {
            "ground1-space1": 500
        }
    }


#---------------------------------------------------
# Fixtures: ephemeris searching
#---------------------------------------------------
@pytest.fixture(scope="session")
def ephemeris_search_id():
    return EPHEMERIS_SEARCH_REQUEST_ID


@pytest.fixture(scope="session")
def ephemeris_search_input_filename():
    return "%s/../../examples/queries/search/ephemeris/example2.json" % (os.path.dirname(__file__))


@pytest.fixture(scope="session")
def ephemeris_search_obj():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # set vars
    start_dt = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end_dt = datetime.datetime(2020, 1, 10, 0, 0, 0)
    programs = ["swarm"]
    platforms = ["swarma"]
    instrument_types = ["footprint"]

    # create object
    s = pyaurorax.search.EphemerisSearch(
        aurorax,
        start_dt,
        end_dt,
        programs=programs,
        platforms=platforms,
        instrument_types=instrument_types,
    )

    # return
    return s


@pytest.fixture(scope="session")
def ephemeris_search_dict():
    return {
        "data_sources": {
            "programs": ["themis-asi"],
            "platforms": ["gillam"],
            "instrument_types": ["panchromatic ASI"],
        },
        "start": "2025-02-05T16:36:43.720Z",
        "end": "2025-02-05T16:36:43.720Z"
    }


#---------------------------------------------------
# Fixtures: data product searching
#---------------------------------------------------
@pytest.fixture(scope="session")
def data_products_search_id():
    return DATA_PRODUCTS_SEARCH_REQUEST_ID


@pytest.fixture(scope="session")
def data_products_search_input_filename():
    return "%s/../../examples/queries/search/data_products/example2.json" % (os.path.dirname(__file__))


@pytest.fixture(scope="session")
def data_products_search_obj():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # set vars
    start_dt = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end_dt = datetime.datetime(2020, 1, 1, 23, 59, 59)
    programs = ["auroramax"]

    # create search object
    s = aurorax.search.DataProductSearch(aurorax, start_dt, end_dt, programs=programs)

    # return
    return s


@pytest.fixture(scope="session")
def data_products_search_dict():
    return {
        "data_sources": {
            "programs": ["themis-asi"],
            "platforms": ["gillam"],
            "instrument_types": ["panchromatic ASI"],
        },
        "start": "2025-02-05T16:36:43.720Z",
        "end": "2025-02-05T16:36:43.720Z"
    }


#---------------------------------------------------
# Fixtures: datasets
#---------------------------------------------------
@pytest.fixture(scope="session")
def all_datasets(api_url):
    aurorax = pyaurorax.PyAuroraX(api_base_url=api_url)
    return aurorax.data.list_datasets()


def find_dataset(datasets, dataset_name):
    for d in datasets:
        if (d.name == dataset_name):
            return copy.deepcopy(d)
    return None


#---------------------------------------------------
# SETUP and TEARDOWN routines
#---------------------------------------------------
def pytest_sessionstart(session):
    """
    Called before any test is done
    """
    # init
    d1 = datetime.datetime.now()
    setup_task_dict = {}
    global CONJUNCTION_SEARCH_REQUEST_ID
    global EPHEMERIS_SEARCH_REQUEST_ID
    global DATA_PRODUCTS_SEARCH_REQUEST_ID

    # initial setup
    print("[SETUP] Setting up API URL and API key ...")
    api_url = session.config.getoption("--api-url")
    api_key = session.config.getoption("--api-key")
    if (api_key is None):
        load_dotenv("%s/.env" % (os.path.dirname(os.path.realpath(__file__))))
        api_key = os.environ["AURORAX_API_KEY"]
    aurorax = pyaurorax.PyAuroraX(api_base_url=api_url, api_key=api_key)

    def setup_task1():
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

    def setup_task2():
        # perform simple conjunction search, set the request ID
        s = aurorax.search.conjunctions.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                               datetime.datetime(2020, 1, 1, 6, 59, 59),
                                               500,
                                               ground=[aurorax.search.GroundCriteriaBlock(programs=["themis-asi"])],
                                               space=[aurorax.search.SpaceCriteriaBlock(programs=["swarm"])])
        setup_task_dict["conjunction_search_id"] = s.request_id

    def setup_task3():
        # perform simple ephemeris search, set the request ID
        s = aurorax.search.ephemeris.search(datetime.datetime(2019, 1, 1, 0, 0, 0),
                                            datetime.datetime(2019, 1, 1, 0, 9, 59),
                                            programs=["swarm"],
                                            platforms=["swarma"],
                                            instrument_types=["footprint"])
        setup_task_dict["ephemeris_search_id"] = s.request_id

    def setup_task4():
        # perform simple data product search, set the request ID
        s = aurorax.search.data_products.search(datetime.datetime(2020, 1, 1, 6, 0, 0),
                                                datetime.datetime(2020, 1, 1, 6, 59, 59),
                                                programs=["auroramax"],
                                                data_product_types=["keogram"])
        setup_task_dict["data_products_search_id"] = s.request_id

    # create and run threads for each setup task
    print("[SETUP] Running setup tasks ...")
    thread1 = threading.Thread(target=setup_task1)
    thread2 = threading.Thread(target=setup_task2)
    thread3 = threading.Thread(target=setup_task3)
    thread4 = threading.Thread(target=setup_task4)
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    CONJUNCTION_SEARCH_REQUEST_ID = setup_task_dict["conjunction_search_id"]
    EPHEMERIS_SEARCH_REQUEST_ID = setup_task_dict["ephemeris_search_id"]
    DATA_PRODUCTS_SEARCH_REQUEST_ID = setup_task_dict["data_products_search_id"]

    # complete
    print("[SETUP] Initialization completed in %s" % (datetime.datetime.now() - d1))


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    print("\n[TEARDOWN] Cleaning up all testing data dirs ...")
    # delete all data testing dirs
    glob_str = "%s/pyaurorax_data_*testing*" % (str(Path.home()))
    path_list = sorted(glob.glob(glob_str))
    for p in path_list:
        shutil.rmtree(p)
