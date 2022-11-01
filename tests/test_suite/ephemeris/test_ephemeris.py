import pytest
import datetime
import time
import pyaurorax
from pyaurorax.ephemeris import Ephemeris

# globals
MAX_WAIT_TIME = 30


@pytest.mark.ephemeris
def test_create_ephemeris_object():
    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    epoch = datetime.datetime(2020, 1, 1, 0, 0)
    location_geo = pyaurorax.Location(lat=51.049999, lon=-114.066666)
    nbtrace = pyaurorax.Location(lat=1.23, lon=45.6)
    sbtrace = pyaurorax.Location(lat=7.89, lon=101.23)
    metadata = {}

    # get identifier
    data_source = pyaurorax.sources.get(program, platform, instrument_type)

    # create Ephemeris object
    e = pyaurorax.ephemeris.Ephemeris(data_source=data_source,
                                      epoch=epoch,
                                      location_geo=location_geo,
                                      nbtrace=nbtrace,
                                      sbtrace=sbtrace,
                                      metadata=metadata)

    assert type(e) is pyaurorax.ephemeris.Ephemeris \
        and e.data_source.instrument_type == "test-instrument-type"


@pytest.mark.ephemeris
def test_create_ephemeris_search_object():
    s = pyaurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                   datetime.datetime(2020, 1, 10, 0, 0, 0),
                                   programs=["swarm"],
                                   platforms=["swarma"],
                                   instrument_types=["footprint"])

    assert type(s) is pyaurorax.ephemeris.Search \
        and s.end == datetime.datetime(2020, 1, 10, 0, 0, 0)


@pytest.mark.ephemeris
def test_search_ephemeris_synchronous():
    s = pyaurorax.ephemeris.search(datetime.datetime(2019, 1, 1, 0, 0, 0),
                                   datetime.datetime(2019, 1, 1, 0, 59, 59),
                                   programs=["swarm"],
                                   platforms=["swarma"],
                                   instrument_types=["footprint"])

    assert type(s.data) is list and type(s.data[0]) is Ephemeris


@pytest.mark.ephemeris
def test_search_ephemeris_asynchronous():
    s = pyaurorax.ephemeris.search(datetime.datetime(2019, 1, 1, 0, 0, 0),
                                   datetime.datetime(2019, 1, 1, 0, 59, 59),
                                   programs=["swarm"],
                                   platforms=["swarma"],
                                   instrument_types=["footprint"],
                                   return_immediately=True)

    s.execute()
    s.update_status()
    tries = 0
    while not s.completed and tries < MAX_WAIT_TIME:
        time.sleep(1)
        s.update_status()
        tries += 1

    if tries == MAX_WAIT_TIME:
        # search is taking too long to complete
        assert False

    s.get_data()

    assert type(s.data) is list and type(s.data[0]) is Ephemeris


@pytest.mark.ephemeris
def test_search_ephemeris_response_format_asynchronous():
    s = pyaurorax.ephemeris.search(datetime.datetime(2019, 1, 1, 0, 0, 0),
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
                                       "metadata": True},
                                   return_immediately=True)

    s.execute()
    s.update_status()
    tries = 0
    while not s.completed and tries < MAX_WAIT_TIME:
        time.sleep(1)
        s.update_status()
        tries += 1

    if tries == MAX_WAIT_TIME:
        # search is taking too long to complete
        assert False

    s.get_data()

    assert type(s.data) is list \
        and type(s.data[0]) is dict \
        and "nbtrace" not in s.data[0].keys()


@pytest.mark.ephemeris
def test_search_ephemeris_logs():
    s = pyaurorax.ephemeris.Search(datetime.datetime(2019, 1, 1, 0, 0, 0),
                                   datetime.datetime(2019, 1, 1, 0, 59, 59),
                                   programs=["swarm"],
                                   platforms=["swarma"],
                                   instrument_types=["footprint"])

    s.execute()
    s.update_status()
    tries = 0
    while not s.completed and tries < MAX_WAIT_TIME:
        time.sleep(1)
        s.update_status()
        tries += 1

    if tries == MAX_WAIT_TIME:
        # search is taking too long to complete
        assert False

    assert len(s.logs) > 0


@pytest.mark.ephemeris
def test_search_ephemeris_status():
    s = pyaurorax.ephemeris.Search(datetime.datetime(2019, 1, 1, 0, 0, 0),
                                   datetime.datetime(2019, 1, 1, 0, 59, 59),
                                   programs=["swarm"],
                                   platforms=["swarma"],
                                   instrument_types=["footprint"])

    s.execute()
    s.update_status()
    tries = 0
    while not s.completed and tries < MAX_WAIT_TIME:
        time.sleep(1)
        s.update_status()
        tries += 1

    if tries == MAX_WAIT_TIME:
        # search is taking too long to complete
        assert False

    assert s.completed


@pytest.mark.ephemeris
def test_upload_ephemeris():
    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "pytest"
    metadata = {
        "test_meta1": "testing1",
        "test_meta2": "testing2",
    }
    epoch = datetime.datetime(2020, 1, 1, 0, 0)
    location_geo = pyaurorax.Location(lat=51.049999, lon=-114.066666)
    location_gsm = pyaurorax.Location(lat=150.25, lon=-10.75)
    nbtrace = pyaurorax.Location(lat=1.23, lon=45.6)
    sbtrace = pyaurorax.Location(lat=7.89, lon=101.23)

    # get the data source ID
    source = pyaurorax.sources.get(program, platform, instrument_type)

    # create Ephemeris object
    e = pyaurorax.ephemeris.Ephemeris(data_source=source,
                                      epoch=epoch,
                                      location_geo=location_geo,
                                      location_gsm=location_gsm,
                                      nbtrace=nbtrace,
                                      sbtrace=sbtrace,
                                      metadata=metadata)

    epoch2 = datetime.datetime(2020, 1, 1, 0, 1)
    metadata2 = {
        "test_meta1": "testing12",
        "test_meta2": "testing22",
    }
    e2 = pyaurorax.ephemeris.Ephemeris(data_source=source,
                                       epoch=epoch2,
                                       location_geo=location_geo,
                                       location_gsm=location_gsm,
                                       nbtrace=nbtrace,
                                       sbtrace=sbtrace,
                                       metadata=metadata2)

    # set records array
    records = [e, e2]

    # upload record
    result = pyaurorax.ephemeris.upload(source.identifier, records, True)

    # retrieve uploaded record
    s = pyaurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                   datetime.datetime(2020, 1, 1, 23, 59, 59),
                                   programs=["test-program"],
                                   platforms=["test-platform"],
                                   instrument_types=["pytest"])

    s.execute()
    s.wait()
    s.check_for_data()
    s.get_data()

    assert result == 0 and len(s.data) > 0


@pytest.mark.ephemeris
def test_delete_ephemeris():
    program = "test-program"
    platform = "test-platform"
    instrument_type = "pytest"
    start = datetime.datetime(2020, 1, 1, 0, 0)
    end = datetime.datetime(2020, 1, 1, 0, 2)
    source = pyaurorax.sources.get(program, platform, instrument_type)

    if not source:
        assert False

    # do synchronous search for existing records
    s = pyaurorax.ephemeris.search(start,
                                   end,
                                   programs=[program],
                                   platforms=[platform],
                                   instrument_types=[instrument_type])

    if len(s.data) == 0:
        print("No ephemeris records exist to delete. Waiting 10s to try again ...")
        time.sleep(10)

        # repeat search
        # do synchronous search for existing records
        s = pyaurorax.ephemeris.search(start,
                                       end,
                                       programs=[program],
                                       platforms=[platform],
                                       instrument_types=[instrument_type])

        if len(s.data) == 0:
            assert False
    else:
        print(f"{len(s.data)} records found to be deleted")

    # delete records
    pyaurorax.ephemeris.delete(source, start, end)
    time.sleep(5)

    # search ephemeris again to see if they were deleted
    s = pyaurorax.ephemeris.search(start,
                                   end,
                                   programs=[program],
                                   platforms=[platform],
                                   instrument_types=[instrument_type])

    assert len(s.data) == 0


@pytest.mark.ephemeris
def test_cancel_ephemeris_search():
    start_dt = datetime.datetime(2018, 1, 1, 0, 0, 0)
    end_dt = datetime.datetime(2021, 12, 31, 23, 59, 59)
    programs = ["themis"]

    s = pyaurorax.ephemeris.Search(start=start_dt,
                                   end=end_dt,
                                   programs=programs)
    s.execute()

    result = s.cancel(wait=True)

    assert result == 0


@pytest.mark.ephemeris
def test_describe_ephemeris_search():
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
    s = pyaurorax.ephemeris.Search(start,
                                   end,
                                   programs=programs,
                                   platforms=platforms,
                                   instrument_types=instrument_types)

    # get describe string
    describe_str = pyaurorax.ephemeris.describe(s)
    print(describe_str)

    # test response
    if (describe_str is not None and describe_str == expected_response_str):
        assert True
    else:
        assert False


@pytest.mark.ephemeris
def test_get_request_url():
    request_id = "testing-request-id"
    expected_url = pyaurorax.api.get_base_url() + "/api/v1/ephemeris/requests/" + request_id
    returned_url = pyaurorax.ephemeris.get_request_url(request_id)
    assert returned_url == expected_url
