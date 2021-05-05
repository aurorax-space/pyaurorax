import aurorax
from aurorax.ephemeris._ephemeris import Ephemeris
from aurorax.ephemeris._search import Search
import datetime


api_key = "ff179c25-962f-4cc8-b77d-bf16768c0991:c2c008f9-c50f-445c-a459-982606e0b1b1"
aurorax.api.set_base_url("https://api.staging.aurorax.space")
aurorax.authenticate(api_key)

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
    data_source = aurorax.sources.get_using_filters(program=program,
                                                    platform=platform,
                                                    instrument_type=instrument_type)
    identifier = data_source[0]["identifier"]

    # create Ephemeris object
    e = aurorax.ephemeris.Ephemeris(identifier=identifier,
                                    program=program,
                                    platform=platform,
                                    instrument_type=instrument_type,
                                    epoch=epoch,
                                    location_geo=location_geo,
                                    location_gsm=location_gsm,
                                    nbtrace=nbtrace,
                                    sbtrace=sbtrace,
                                    metadata=metadata)

    assert type(e) is Ephemeris and e.instrument_type == "test-instrument-type"


def test_create_ephemeris_search_object():
    s = aurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                 datetime.datetime(2020, 1, 10, 0, 0, 0),
                                 programs=["swarm"],
                                 platforms=["swarma"],
                                 instrument_types=["footprint"])

    assert type(s) is Search and s.end_dt ==  datetime.datetime(2020, 1, 10, 0, 0, 0)


def test_search_ephemeris_synchronous():
    s = aurorax.ephemeris.search(datetime.datetime(2019, 1, 1, 0, 0, 0),
                                 datetime.datetime(2019, 1, 1, 0, 59, 59),
                                 programs=["swarm"],
                                 platforms=["swarma"],
                                 instrument_types=["footprint"])

    assert len(s.data) > 0 and "data_source" in s.data[0]


def test_search_ephemeris_asynchronous():
    s = aurorax.ephemeris.search_async(datetime.datetime(2019, 1, 1, 0, 0, 0),
                                 datetime.datetime(2019, 1, 1, 0, 59, 59),
                                 programs=["swarm"],
                                 platforms=["swarma"],
                                 instrument_types=["footprint"])

    assert type(s) is Search


def test_upload_ephemeris():
    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    metadata = {
        "test_meta1": "testing1",
        "test_meta2": "testing2",
    }
    epoch = datetime.datetime(2020, 1, 1, 1, 2)
    location_geo = aurorax.Location(lat=51.049999, lon=-114.066666)
    location_gsm = aurorax.Location(lat=150.25, lon=-10.75)
    nbtrace = aurorax.Location(lat=1.23, lon=45.6)
    sbtrace = aurorax.Location(lat=7.89, lon=101.23)

    # get the ephemeris source ID
    source = aurorax.sources.get_using_filters(program=[program],
                                               platform=[platform],
                                               instrument_type=[instrument_type])
    identifier = source[0]["identifier"]

    # create Ephemeris object
    e = aurorax.ephemeris.Ephemeris(identifier=identifier,
                                    program=program,
                                    platform=platform,
                                    instrument_type=instrument_type,
                                    epoch=epoch,
                                    location_geo=location_geo,
                                    location_gsm=location_gsm,
                                    nbtrace=nbtrace,
                                    sbtrace=sbtrace,
                                    metadata=metadata)

    # set records array
    records = []
    records.append(e)

    # upload record
    result = aurorax.ephemeris.upload(identifier, records=records)

    # retrieve uploaded record
    s = aurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                 datetime.datetime(2020, 1, 5, 0, 0, 0),
                                 programs=["test-program"],
                                 platforms=["test-platform"],
                                 instrument_types=["test-instrument-type"])

    s.execute()
    s.wait()
    s.check_for_data()
    s.get_data()
    

    assert result == 0 and len(s.data) > 0


def test_delete_ephemeris():
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    start_dt = datetime.datetime(2020, 1, 1, 0, 0)
    end_dt = datetime.datetime(2020, 1, 10, 0, 0, 0)
    source = aurorax.sources.get_using_filters(program=program, platform=platform, instrument_type=instrument_type, format="identifier_only")

    if len(source) != 1:
        assert False

    # do synchronous search for existing records
    s = aurorax.ephemeris.search(start_dt,
                                 end_dt,
                                 programs=[program],
                                 platforms=[platform],
                                 instrument_types=[instrument_type])

    if len(s.data) == 0:
        print("No ephemeris records exist to delete")
        assert False
    else:
        print(f"{len(s.data)} records found to be deleted")

    params = {
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "start": start_dt.strftime("%Y-%m-%dT%H:%M:%S"),
        "end": end_dt.strftime("%Y-%m-%dT%H:%M:%S")
    }
    delete_req = aurorax.AuroraXRequest(method="delete", url=aurorax.api.urls.ephemeris_upload_url.format(source[0]["identifier"]), body=params)

    try:
        delete_req.execute()
    except KeyError as err:
        # this is here because the API does not return a "Content-Type" header
        pass

    # search ephemeris again to see if they were deleted
    s = aurorax.ephemeris.search(start_dt,
                                 end_dt,
                                 programs=[program],
                                 platforms=[platform],
                                 instrument_types=[instrument_type])

    assert len(s.data) == 0

