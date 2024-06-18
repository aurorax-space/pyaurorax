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
import datetime
import time
from pyaurorax.search import Location, DataSource, EphemerisSearch, EphemerisData

# globals
MAX_WAIT_TIME = 30


@pytest.mark.search_ephemeris
def test_create_ephemeris_data_object(aurorax):
    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    epoch = datetime.datetime(2020, 1, 1, 0, 0)
    location_geo = Location(lat=51.049999, lon=-114.066666)
    nbtrace = Location(lat=1.23, lon=45.6)
    sbtrace = Location(lat=7.89, lon=101.23)
    metadata = {}

    # get identifier
    data_source = aurorax.search.sources.get(program, platform, instrument_type)

    # create Ephemeris object
    e = EphemerisData(data_source=data_source, epoch=epoch, location_geo=location_geo, nbtrace=nbtrace, sbtrace=sbtrace, metadata=metadata)

    assert isinstance(e, EphemerisData) is True
    assert isinstance(e.data_source, DataSource) is True
    assert e.data_source.program == program
    assert e.data_source.platform == platform
    assert e.data_source.instrument_type == instrument_type


@pytest.mark.search_ephemeris
def test_create_ephemeris_search_object(aurorax):
    # set vars
    start_dt = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end_dt = datetime.datetime(2020, 1, 10, 0, 0, 0)
    programs = ["swarm"]
    platforms = ["swarma"]
    instrument_types = ["footprint"]

    # create object
    s = EphemerisSearch(
        aurorax,
        start_dt,
        end_dt,
        programs=programs,
        platforms=platforms,
        instrument_types=instrument_types,
    )

    assert isinstance(s, EphemerisSearch) is True
    assert s.start == start_dt
    assert s.end == end_dt
    assert s.programs == programs
    assert s.platforms == platforms
    assert s.instrument_types == instrument_types


@pytest.mark.search_ephemeris
def test_search_ephemeris_synchronous(aurorax):
    s = aurorax.search.ephemeris.search(datetime.datetime(2019, 1, 1, 0, 0, 0),
                                        datetime.datetime(2019, 1, 1, 0, 59, 59),
                                        programs=["swarm"],
                                        platforms=["swarma"],
                                        instrument_types=["footprint"])

    assert isinstance(s.data, list) is True
    assert len(s.data) > 0
    assert isinstance(s.data[0], EphemerisData) is True


@pytest.mark.search_ephemeris
def test_search_ephemeris_asynchronous(aurorax):
    s = aurorax.search.ephemeris.search(datetime.datetime(2019, 1, 1, 0, 0, 0),
                                        datetime.datetime(2019, 1, 1, 0, 59, 59),
                                        programs=["swarm"],
                                        platforms=["swarma"],
                                        instrument_types=["footprint"],
                                        return_immediately=True)

    s.update_status()
    total_sleep_time = 0
    while (s.completed is False and total_sleep_time < MAX_WAIT_TIME):
        time.sleep(1)
        s.update_status()
        total_sleep_time += 1

    if (total_sleep_time == MAX_WAIT_TIME):
        # search is taking too long to complete
        raise AssertionError("Request took too long to complete")

    s.get_data()

    assert isinstance(s.data, list) is True
    assert len(s.data) > 0
    assert isinstance(s.data[0], EphemerisData) is True


@pytest.mark.search_ephemeris
def test_search_ephemeris_response_format_asynchronous(aurorax):
    s = aurorax.search.ephemeris.search(datetime.datetime(2019, 1, 1, 0, 0, 0),
                                        datetime.datetime(2019, 1, 1, 0, 59, 59),
                                        programs=["swarm"],
                                        platforms=["swarma"],
                                        instrument_types=["footprint"],
                                        response_format={
                                            "data_source": {
                                                "identifier": True,
                                                "program": True,
                                            },
                                            "epoch": True,
                                            "location_geo": {
                                                "lat": True,
                                                "lon": True
                                            },
                                            "metadata": True
                                        },
                                        return_immediately=True)

    s.update_status()
    total_sleep_time = 0
    while (s.completed is False and total_sleep_time < MAX_WAIT_TIME):
        time.sleep(1)
        s.update_status()
        total_sleep_time += 1

    if (total_sleep_time == MAX_WAIT_TIME):
        # search is taking too long to complete
        raise AssertionError("Request took too long to complete")

    s.get_data()

    assert isinstance(s.data, list) is True
    assert len(s.data) > 0
    assert isinstance(s.data[0], dict) is True
    assert "nbtrace" not in s.data[0].keys()


@pytest.mark.search_ephemeris
def test_search_ephemeris_logs(aurorax):
    s = EphemerisSearch(aurorax,
                        datetime.datetime(2019, 1, 1, 0, 0, 0),
                        datetime.datetime(2019, 1, 1, 0, 59, 59),
                        programs=["swarm"],
                        platforms=["swarma"],
                        instrument_types=["footprint"])

    s.execute()
    s.update_status()
    total_sleep_time = 0
    while (s.completed is False and total_sleep_time < MAX_WAIT_TIME):
        time.sleep(1)
        s.update_status()
        total_sleep_time += 1

    if (total_sleep_time == MAX_WAIT_TIME):
        # search is taking too long to complete
        raise AssertionError("Request took too long to complete")

    s.get_data()

    assert len(s.logs) > 0


@pytest.mark.search_ephemeris
def test_search_ephemeris_status(aurorax):
    s = EphemerisSearch(aurorax,
                        datetime.datetime(2019, 1, 1, 0, 0, 0),
                        datetime.datetime(2019, 1, 1, 0, 59, 59),
                        programs=["swarm"],
                        platforms=["swarma"],
                        instrument_types=["footprint"])

    s.execute()
    s.update_status()
    total_sleep_time = 0
    while (s.completed is False and total_sleep_time < MAX_WAIT_TIME):
        time.sleep(1)
        s.update_status()
        total_sleep_time += 1

    if (total_sleep_time == MAX_WAIT_TIME):
        # search is taking too long to complete
        raise AssertionError("Request took too long to complete")

    s.get_data()

    assert s.completed is True


@pytest.mark.search_ephemeris
def test_upload_and_delete_ephemeris(aurorax):
    # get the data source
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    ds = aurorax.search.sources.get(program, platform, instrument_type)

    # set values
    location_geo = Location(lat=51.049999, lon=-114.066666)
    location_gsm = Location(lat=150.25, lon=-10.75)
    nbtrace = Location(lat=1.23, lon=45.6)
    sbtrace = Location(lat=7.89, lon=101.23)
    metadata = {
        "test_meta1": "testing1",
        "test_meta2": "testing2",
    }

    # create Ephemeris objects
    e1 = EphemerisData(data_source=ds,
                       epoch=datetime.datetime(2020, 1, 1, 0, 0),
                       location_geo=location_geo,
                       location_gsm=location_gsm,
                       nbtrace=nbtrace,
                       sbtrace=sbtrace,
                       metadata=metadata)
    e2 = EphemerisData(data_source=ds,
                       epoch=datetime.datetime(2020, 1, 1, 0, 1),
                       location_geo=location_geo,
                       location_gsm=location_gsm,
                       nbtrace=nbtrace,
                       sbtrace=sbtrace,
                       metadata=metadata)

    # set records array
    records = [e1, e2]

    # upload record
    result = aurorax.search.ephemeris.upload(ds.identifier, records, True)
    assert result == 0

    # wait
    time.sleep(10)  # won't take long for it to be ingested, but we wait anyways

    # retrieve uploaded record
    s = EphemerisSearch(aurorax,
                        datetime.datetime(2020, 1, 1, 0, 0, 0),
                        datetime.datetime(2020, 1, 1, 23, 59, 59),
                        programs=[program],
                        platforms=[platform],
                        instrument_types=[instrument_type])
    s.execute()
    s.wait()
    s.get_data()
    assert len(s.data) > 0

    # cleanup by deleting the ephemeris data that was uploaded
    delete_result = aurorax.search.ephemeris.delete(
        ds,
        datetime.datetime(2020, 1, 1, 0, 0),
        datetime.datetime(2020, 1, 1, 23, 59),
    )
    assert delete_result == 0


@pytest.mark.search_ephemeris
def test_cancel_ephemeris_search(aurorax):
    start_dt = datetime.datetime(2018, 1, 1, 0, 0, 0)
    end_dt = datetime.datetime(2021, 12, 31, 23, 59, 59)
    programs = ["themis"]

    s = EphemerisSearch(aurorax, start=start_dt, end=end_dt, programs=programs)
    s.execute()

    result = s.cancel(wait=True)

    assert result == 0


@pytest.mark.search_ephemeris
def test_describe_ephemeris_search(aurorax):
    # set params
    start = datetime.datetime(2019, 1, 1, 0, 0, 0)
    end = datetime.datetime(2019, 1, 1, 0, 59, 59)
    programs = ["swarm"]
    platforms = ["swarma"]
    instrument_types = ["footprint"]
    expected_response_str = "Find ephemeris for ((program in (swarm) AND platform in (swarma) " \
        "AND instrument_type in (footprint) filtered by metadata ()) AND  ephemeris_metadata_filters " \
        "[])  AND epoch between 2019-01-01T00:00 and 2019-01-01T00:59:59 UTC"

    # create search object
    s = EphemerisSearch(aurorax, start, end, programs=programs, platforms=platforms, instrument_types=instrument_types)

    # get describe string
    describe_str = aurorax.search.ephemeris.describe(s)

    # test response
    assert describe_str is not None
    assert describe_str == expected_response_str


@pytest.mark.search_ephemeris
def test_get_request_url(aurorax):
    request_id = "testing-request-id"
    expected_url = aurorax.api_base_url + "/api/v1/ephemeris/requests/" + request_id
    returned_url = aurorax.search.ephemeris.get_request_url(request_id)
    assert returned_url == expected_url
