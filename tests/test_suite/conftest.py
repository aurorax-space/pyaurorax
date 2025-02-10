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
import gc
import cv2
import time
import copy
import glob
import shutil
import pytest
import datetime
import pyaurorax
from click.testing import CliRunner
from pathlib import Path
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

# globals
MAX_INIT_WORKERS = 4
CONJUNCTION_SEARCH_REQUEST_ID = None
EPHEMERIS_SEARCH_REQUEST_ID = None
DATA_PRODUCTS_SEARCH_REQUEST_ID = None
tools_data_single_themis_file = None
tools_data_themis_movie_filenames = None
tools_data_single_trex_rgb_file = None
tools_data_bounding_box_data = None
tools_data_rego_calibration_data = None
tools_data_trex_nir_calibration_data = None
tools_data_ccd_contour_data = None
tools_data_themis_keogram_data = None
tools_data_trex_rgb_keogram_data = None


def pytest_addoption(parser):
    parser.addoption("--api-url", action="store", default="https://api.staging.aurorax.space", help="A specific API URL to use")
    parser.addoption("--api-key", type=str, help="A specific API key to use")
    parser.addoption("--do-search-tasks", action="store_true", help="Do the search initialization tasks")
    parser.addoption("--do-tools-tasks", action="store_true", help="Do the tools initialization tasks")


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
# Fixtures: tools
#---------------------------------------------------
@pytest.fixture(scope="function")
def plot_cleanup():
    yield  # do test
    gc.collect()


@pytest.fixture(scope="function")
def at():
    aurorax = pyaurorax.PyAuroraX()
    return aurorax.tools


@pytest.fixture(scope="session")
def themis_single_file():
    return tools_data_single_themis_file


@pytest.fixture(scope="session")
def trex_rgb_single_file():
    return tools_data_single_trex_rgb_file


@pytest.fixture(scope="session")
def themis_movie_filenames():
    return tools_data_themis_movie_filenames


@pytest.fixture(scope="session")
def bounding_box_data():
    return tools_data_bounding_box_data


@pytest.fixture(scope="session")
def rego_calibration_data():
    return tools_data_rego_calibration_data


@pytest.fixture(scope="session")
def trex_nir_calibration_data():
    return tools_data_trex_nir_calibration_data


@pytest.fixture(scope="session")
def ccd_contour_data():
    return tools_data_ccd_contour_data


@pytest.fixture(scope="session")
def themis_keogram_data():
    return tools_data_themis_keogram_data


@pytest.fixture(scope="session")
def trex_rgb_keogram_data():
    return tools_data_trex_rgb_keogram_data


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
    global tools_data_single_themis_file
    global tools_data_themis_movie_filenames
    global tools_data_single_trex_rgb_file
    global tools_data_bounding_box_data
    global tools_data_rego_calibration_data
    global tools_data_trex_nir_calibration_data
    global tools_data_ccd_contour_data
    global tools_data_themis_keogram_data
    global tools_data_trex_rgb_keogram_data

    # initial setup
    print("[SETUP] Setting up API URL and API key ...")
    api_url = session.config.getoption("--api-url")
    api_key = session.config.getoption("--api-key")
    if (api_key is None):
        load_dotenv("%s/.env" % (os.path.dirname(os.path.realpath(__file__))))
        api_key = os.environ["AURORAX_API_KEY"]
    aurorax = pyaurorax.PyAuroraX(api_base_url=api_url, api_key=api_key)

    def init_task_search_data_source():
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
        print("[SETUP]   Finished setting up data source")

    def init_task_search_conjunctions():
        # perform simple conjunction search, set the request ID
        s = aurorax.search.conjunctions.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                               datetime.datetime(2020, 1, 1, 6, 59, 59),
                                               500,
                                               ground=[aurorax.search.GroundCriteriaBlock(programs=["themis-asi"])],
                                               space=[aurorax.search.SpaceCriteriaBlock(programs=["swarm"])])
        setup_task_dict["conjunction_search_id"] = s.request_id
        print("[SETUP]   Finished setting up conjunction search")

    def init_task_search_ephemeris():
        # perform simple ephemeris search, set the request ID
        s = aurorax.search.ephemeris.search(datetime.datetime(2019, 1, 1, 0, 0, 0),
                                            datetime.datetime(2019, 1, 1, 0, 9, 59),
                                            programs=["swarm"],
                                            platforms=["swarma"],
                                            instrument_types=["footprint"])
        setup_task_dict["ephemeris_search_id"] = s.request_id
        print("[SETUP]   Finished setting up ephemeris search")

    def init_task_search_data_products():
        # perform simple data product search, set the request ID
        s = aurorax.search.data_products.search(datetime.datetime(2020, 1, 1, 6, 0, 0),
                                                datetime.datetime(2020, 1, 1, 6, 59, 59),
                                                programs=["auroramax"],
                                                data_product_types=["keogram"])
        setup_task_dict["data_products_search_id"] = s.request_id
        print("[SETUP]   Finished setting up data product search")

    # do search initialization tasks
    if (session.config.getoption("--do-search-tasks") is True):
        # init
        print("[SETUP] Running search setup tasks ...")

        # setup threads and wait
        tasks = [
            init_task_search_data_source,
            init_task_search_conjunctions,
            init_task_search_ephemeris,
            init_task_search_data_products,
        ]
        with ThreadPoolExecutor(max_workers=MAX_INIT_WORKERS) as executor:
            futures = [executor.submit(task) for task in tasks]
            for future in as_completed(futures):
                future.result()

        # set results
        CONJUNCTION_SEARCH_REQUEST_ID = setup_task_dict["conjunction_search_id"]
        EPHEMERIS_SEARCH_REQUEST_ID = setup_task_dict["ephemeris_search_id"]
        DATA_PRODUCTS_SEARCH_REQUEST_ID = setup_task_dict["data_products_search_id"]
    else:
        print("[SETUP] Skipping search setup tasks")

    # do tools initialization tasks
    if (session.config.getoption("--do-tools-tasks") is True):
        # init
        print("[SETUP] Running tools setup tasks ...")

        # read in single THEMIS file
        def init_task_download_read_themis_single_minute():
            # read in a minute of THEMIS raw data
            r = aurorax.data.ucalgary.download(
                "THEMIS_ASI_RAW",
                datetime.datetime(2021, 11, 4, 9, 0),
                datetime.datetime(2021, 11, 4, 9, 0),
                site_uid="atha",
                progress_bar_disable=True,
            )
            setup_task_dict["themis_single_file"] = aurorax.data.ucalgary.read(r.dataset, r.filenames)
            print("[SETUP]   Finished setting up a minute of THEMIS data")

        def init_task_download_read_trex_rgb_single_minute():
            # read in a minute of THEMIS raw data
            r = aurorax.data.ucalgary.download(
                "TREX_RGB_RAW_NOMINAL",
                datetime.datetime(2021, 11, 4, 9, 0),
                datetime.datetime(2021, 11, 4, 9, 0),
                site_uid="rabb",
                progress_bar_disable=True,
            )
            setup_task_dict["trex_rgb_single_file"] = aurorax.data.ucalgary.read(r.dataset, r.filenames)
            print("[SETUP]   Finished setting up a minute of TREx RGB data")

        def init_task_generate_themis_movie_frames():
            # read in a minute of THEMIS raw data
            r = aurorax.data.ucalgary.download(
                "THEMIS_ASI_RAW",
                datetime.datetime(2021, 11, 4, 9, 1),
                datetime.datetime(2021, 11, 4, 9, 1),
                site_uid="atha",
                progress_bar_disable=True,
            )
            data = aurorax.data.ucalgary.read(r.dataset, r.filenames)

            # process frames
            filenames = []
            for i in range(0, len(data.metadata)):
                filename = "/tmp/pyaurorax_testing_themis_movie_frames/%s_frame.png" % (data.timestamp[i].strftime("%Y%m%d_%H%M%S"))
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                cv2.imwrite(filename, data.data[:, :, i])
                filenames.append(filename)

            # set data for later
            setup_task_dict["themis_movie_filenames"] = filenames
            print("[SETUP]   Finished setting up THEMIS movie data")

        def init_task_prep_bounding_box():
            # get THEMIS data
            start_dt = datetime.datetime(2021, 11, 4, 9, 2)
            end_dt = datetime.datetime(2021, 11, 4, 9, 2)
            site_uid = "atha"
            r = aurorax.data.ucalgary.download("THEMIS_ASI_RAW", start_dt, end_dt, site_uid=site_uid, progress_bar_disable=True)
            themis_data = aurorax.data.ucalgary.read(r.dataset, r.filenames)

            # get the applicable THEMIS skymap
            r = aurorax.data.ucalgary.download_best_skymap("THEMIS_ASI_SKYMAP_IDLSAV", site_uid, start_dt)
            themis_skymap = aurorax.data.ucalgary.read(r.dataset, r.filenames).data[0]

            # get RGB data
            start_dt = datetime.datetime(2021, 11, 4, 3, 0)
            end_dt = datetime.datetime(2021, 11, 4, 3, 0)
            site_uid = "gill"
            r = aurorax.data.ucalgary.download("TREX_RGB_RAW_NOMINAL", start_dt, end_dt, site_uid=site_uid, progress_bar_disable=True)
            trex_rgb_data = aurorax.data.ucalgary.read(r.dataset, r.filenames)

            # get the applicable RGB skymap
            r = aurorax.data.ucalgary.download_best_skymap("TREX_RGB_SKYMAP_IDLSAV", site_uid, start_dt)
            trex_rgb_skymap = aurorax.data.ucalgary.read(r.dataset, r.filenames).data[0]

            # set variable for later usage
            setup_task_dict["bounding_box_data"] = {
                "themis_data": themis_data,
                "themis_skymap": themis_skymap,
                "trex_rgb_data": trex_rgb_data,
                "trex_rgb_skymap": trex_rgb_skymap,
            }
            print("[SETUP]   Finished setting up bounding box data")

        def init_task_prep_calibration_rego():
            # get raw data
            dataset_name = "REGO_RAW"
            dt = datetime.datetime(2021, 11, 4, 3, 30)
            site_uid = "gill"
            r = aurorax.data.ucalgary.download(dataset_name, dt, dt, site_uid=site_uid, progress_bar_disable=True)
            raw_data = aurorax.data.ucalgary.read(r.dataset, r.filenames)
            device_uid = raw_data.metadata[0]["Imager unique ID"][5:]

            # download rayleighs calibration
            dataset_name = "REGO_CALIBRATION_RAYLEIGHS_IDLSAV"
            r = aurorax.data.ucalgary.download_best_rayleighs_calibration(dataset_name, device_uid, dt)
            data_cal_rayleighs = aurorax.data.ucalgary.read(r.dataset, r.filenames[0])

            # download flatfield calibration
            dataset_name = "REGO_CALIBRATION_FLATFIELD_IDLSAV"
            r = aurorax.data.ucalgary.download_best_rayleighs_calibration(dataset_name, device_uid, dt)
            data_cal_flatfield = aurorax.data.ucalgary.read(r.dataset, r.filenames[0])

            # set variable for later usage
            setup_task_dict["rego_calibration_data"] = {
                "raw_data": raw_data,
                "rayleighs_data": data_cal_rayleighs,
                "flatfield_data": data_cal_flatfield,
            }
            print("[SETUP]   Finished setting up REGO calibration data")

        def init_task_prep_calibration_trex_nir():
            # get raw data
            dataset_name = "TREX_NIR_RAW"
            dt = datetime.datetime(2021, 11, 4, 3, 30)
            site_uid = "gill"
            r = aurorax.data.ucalgary.download(dataset_name, dt, dt, site_uid=site_uid, progress_bar_disable=True)
            raw_data = aurorax.data.ucalgary.read(r.dataset, r.filenames)
            device_uid = raw_data.metadata[0]["Imager unique ID"][5:]

            # download rayleighs calibration
            dataset_name = "TREX_NIR_CALIBRATION_RAYLEIGHS_IDLSAV"
            r = aurorax.data.ucalgary.download_best_rayleighs_calibration(dataset_name, device_uid, dt)
            data_cal_rayleighs = aurorax.data.ucalgary.read(r.dataset, r.filenames[0])

            # download flatfield calibration
            dataset_name = "TREX_NIR_CALIBRATION_FLATFIELD_IDLSAV"
            r = aurorax.data.ucalgary.download_best_rayleighs_calibration(dataset_name, device_uid, dt)
            data_cal_flatfield = aurorax.data.ucalgary.read(r.dataset, r.filenames[0])

            # set variable for later usage
            setup_task_dict["trex_nir_calibration_data"] = {
                "raw_data": raw_data,
                "rayleighs_data": data_cal_rayleighs,
                "flatfield_data": data_cal_flatfield,
            }
            print("[SETUP]   Finished setting up TREx NIR calibration data")

        def init_task_prep_ccd_contour():
            # download a minute of TREx RGB data from Gillam
            dataset_name = "TREX_RGB_RAW_NOMINAL"
            dt = datetime.datetime(2023, 2, 24, 6, 15)
            site_uid = "gill"
            r = aurorax.data.ucalgary.download(dataset_name, dt, dt, site_uid=site_uid, progress_bar_disable=True)
            trex_rgb_data = aurorax.data.ucalgary.read(r.dataset, r.filenames)

            # download the corresponding skymap
            dataset_name = "TREX_RGB_SKYMAP_IDLSAV"
            r = aurorax.data.ucalgary.download_best_skymap(dataset_name, site_uid, dt)
            trex_rgb_skymap = aurorax.data.ucalgary.read(r.dataset, r.filenames).data[0]

            # set variable for later usage
            setup_task_dict["ccd_contour_data"] = {
                "trex_rgb_data": trex_rgb_data,
                "trex_rgb_skymap": trex_rgb_skymap,
            }
            print("[SETUP]   Finished setting up CCD contour data")

        def init_task_prep_themis_keogram():
            # download 10 minutes of THEMIS ASI data
            dataset_name = "THEMIS_ASI_RAW"
            start_dt = datetime.datetime(2021, 11, 4, 9, 0)
            end_dt = datetime.datetime(2021, 11, 4, 9, 9)
            site_uid = "atha"
            r = aurorax.data.ucalgary.download(dataset_name, start_dt, end_dt, site_uid=site_uid, progress_bar_disable=True)
            data = aurorax.data.ucalgary.read(r.dataset, r.filenames)

            # get skymap
            r = aurorax.data.ucalgary.download_best_skymap("THEMIS_ASI_SKYMAP_IDLSAV", site_uid, start_dt)
            skymap_data = aurorax.data.ucalgary.read(r.dataset, r.filenames).data[0]

            # set variable for later usage
            setup_task_dict["themis_keogram_data"] = {
                "raw_data": data,
                "skymap": skymap_data,
            }
            print("[SETUP]   Finished setting up THEMIS keogram data")

        def init_task_prep_trex_rgb_keogram():
            # download 10 minutes of RGB data
            dataset_name = "TREX_RGB_RAW_NOMINAL"
            start_dt = datetime.datetime(2021, 11, 4, 3, 30)
            end_dt = datetime.datetime(2021, 11, 4, 3, 39)
            site_uid = "rabb"
            r = aurorax.data.ucalgary.download(dataset_name, start_dt, end_dt, site_uid=site_uid, progress_bar_disable=True)
            data = aurorax.data.ucalgary.read(r.dataset, r.filenames)

            # get skymap
            r = aurorax.data.ucalgary.download_best_skymap("TREX_RGB_SKYMAP_IDLSAV", site_uid, start_dt)
            skymap_data = aurorax.data.ucalgary.read(r.dataset, r.filenames).data[0]

            # set variable for later usage
            setup_task_dict["trex_rgb_keogram_data"] = {
                "raw_data": data,
                "skymap": skymap_data,
            }
            print("[SETUP]   Finished setting up TREx RGB keogram data")

        # start and wait for threads
        tasks = [
            init_task_download_read_themis_single_minute,
            init_task_generate_themis_movie_frames,
            init_task_download_read_trex_rgb_single_minute,
            init_task_prep_bounding_box,
            init_task_prep_calibration_rego,
            init_task_prep_calibration_trex_nir,
            init_task_prep_ccd_contour,
            init_task_prep_themis_keogram,
            init_task_prep_trex_rgb_keogram,
        ]
        with ThreadPoolExecutor(max_workers=MAX_INIT_WORKERS) as executor:
            futures = [executor.submit(task) for task in tasks]
            for future in as_completed(futures):
                future.result()

        # set results
        tools_data_single_themis_file = setup_task_dict["themis_single_file"]
        tools_data_themis_movie_filenames = setup_task_dict["themis_movie_filenames"]
        tools_data_single_trex_rgb_file = setup_task_dict["trex_rgb_single_file"]
        tools_data_bounding_box_data = setup_task_dict["bounding_box_data"]
        tools_data_rego_calibration_data = setup_task_dict["rego_calibration_data"]
        tools_data_trex_nir_calibration_data = setup_task_dict["trex_nir_calibration_data"]
        tools_data_ccd_contour_data = setup_task_dict["ccd_contour_data"]
        tools_data_themis_keogram_data = setup_task_dict["themis_keogram_data"]
        tools_data_trex_rgb_keogram_data = setup_task_dict["trex_rgb_keogram_data"]
    else:
        print("[SETUP] Skipping tools setup tasks")

    # complete
    print("[SETUP] Initialization completed in %s" % (datetime.datetime.now() - d1))


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    # delete all data testing dirs
    print("\n\n[TEARDOWN] Cleaning up all testing data dirs ...")
    glob_str = "%s/pyaurorax_data_*testing*" % (str(Path.home()))
    path_list = sorted(glob.glob(glob_str))
    for p in path_list:
        shutil.rmtree(p)

    # delete movie testing dirs
    print("[TEARDOWN] Cleaning up movie testing dirs ...")
    time.sleep(2)  # absolutely no idea why this works
    shutil.rmtree("/tmp/pyaurorax_testing_themis_movie_frames", ignore_errors=True)
