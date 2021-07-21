from aurorax.ephemeris import Ephemeris
import aurorax
import datetime
import os
import time

MAX_WAIT_TIME = 30

def test_create_ephemeris_object():
    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    epoch = datetime.datetime(2020, 1, 1, 0, 0)
    location_geo = aurorax.Location(lat=51.049999, lon=-114.066666)
    location_gsm = aurorax.Location(lat=150.25, lon=-10.75)
    nbtrace = aurorax.Location(lat=1.23, lon=45.6)
    sbtrace = aurorax.Location(lat=7.89, lon=101.23)
    metadata = {}

    # get identifier
    data_source = aurorax.sources.get(program, platform, instrument_type)

    # create Ephemeris object
    e = aurorax.ephemeris.Ephemeris(data_source=data_source,
                                    epoch=epoch,
                                    location_geo=location_geo,
                                    location_gsm=location_gsm,
                                    nbtrace=nbtrace,
                                    sbtrace=sbtrace,
                                    metadata=metadata)

    assert type(e) is aurorax.ephemeris.Ephemeris and e.data_source.instrument_type == "test-instrument-type"


def test_create_ephemeris_search_object():
    s = aurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                 datetime.datetime(2020, 1, 10, 0, 0, 0),
                                 programs=["swarm"],
                                 platforms=["swarma"],
                                 instrument_types=["footprint"])

    assert type(s) is aurorax.ephemeris.Search and s.end ==  datetime.datetime(2020, 1, 10, 0, 0, 0)

def test_search_ephemeris_synchronous():
    s = aurorax.ephemeris.search(datetime.datetime(2019, 1, 1, 0, 0, 0),
                                 datetime.datetime(2019, 1, 1, 0, 59, 59),
                                 programs=["swarm"],
                                 platforms=["swarma"],
                                 instrument_types=["footprint"])

    assert type(s.data) is list and type(s.data[0]) is Ephemeris

def test_search_ephemeris_asynchronous():
    s = aurorax.ephemeris.search_async(datetime.datetime(2019, 1, 1, 0, 0, 0),
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

    s.get_data()

    assert type(s.data) is list and type(s.data[0]) is Ephemeris

def test_search_ephemeris_logs():
    s = aurorax.ephemeris.Search(datetime.datetime(2019, 1, 1, 0, 0, 0),
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

def test_search_ephemeris_status():
    s = aurorax.ephemeris.Search(datetime.datetime(2019, 1, 1, 0, 0, 0),
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
    location_geo = aurorax.Location(lat=51.049999, lon=-114.066666)
    location_gsm = aurorax.Location(lat=150.25, lon=-10.75)
    nbtrace = aurorax.Location(lat=1.23, lon=45.6)
    sbtrace = aurorax.Location(lat=7.89, lon=101.23)

    # get the ephemeris source ID
    source = aurorax.sources.get(program, platform, instrument_type)

    # create Ephemeris object
    e = aurorax.ephemeris.Ephemeris(data_source=source,
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
    e2 = aurorax.ephemeris.Ephemeris(data_source=source,
                                    epoch=epoch2,
                                    location_geo=location_geo,
                                    location_gsm=location_gsm,
                                    nbtrace=nbtrace,
                                    sbtrace=sbtrace,
                                    metadata=metadata2)

    # set records array
    records = [e, e2]

    # upload record
    result = aurorax.ephemeris.upload(source.identifier, records, True)

    # retrieve uploaded record
    s = aurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                 datetime.datetime(2020, 1, 1, 23, 59, 59),
                                 programs=["test-program"],
                                 platforms=["test-platform"],
                                 instrument_types=["pytest"])

    s.execute()
    s.wait()
    s.check_for_data()
    s.get_data()
    
    assert result == 1 and len(s.data) > 0

def test_delete_ephemeris():
    program = "test-program"
    platform = "test-platform"
    instrument_type = "pytest"
    start = datetime.datetime(2020, 1, 1, 0, 0)
    end = datetime.datetime(2020, 1, 1, 0, 2)
    source = aurorax.sources.get(program, platform, instrument_type)

    if not source:
        assert False

    # do synchronous search for existing records
    s = aurorax.ephemeris.search(start,
                                 end,
                                 programs=[program],
                                 platforms=[platform],
                                 instrument_types=[instrument_type])

    if len(s.data) == 0:
        print("No ephemeris records exist to delete")
        assert False
    else:
        print(f"{len(s.data)} records found to be deleted")

    aurorax.ephemeris.delete(source, start, end)

    time.sleep(5)

    # search ephemeris again to see if they were deleted
    s = aurorax.ephemeris.search(start,
                                 end,
                                 programs=[program],
                                 platforms=[platform],
                                 instrument_types=[instrument_type])

    assert len(s.data) == 0

def test_cancel_ephemeris_search():
    start_dt = datetime.datetime(2018, 1, 1)
    end_dt = datetime.datetime(2021, 12, 31, 23, 59, 59)
    programs = ["themis"]

    s = aurorax.ephemeris.Search(start=start_dt, end=end_dt, programs=programs)
    s.execute()
    
    result = s.cancel(wait=True)
    
    assert result == 1
