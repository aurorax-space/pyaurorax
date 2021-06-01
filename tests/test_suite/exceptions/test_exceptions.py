import aurorax
from aurorax.exceptions import *
import datetime
import os
import pytest
import time

ACCOUNTS_URL = "/api/v1/accounts"

def test_AuroraXNotFoundException():
    # test finding a source that doesn't exist
    with pytest.raises(AuroraXNotFoundException):
        aurorax.sources.get("does-not-exist", "does-not-exist", "does-not-exist")


def test_AuroraXDuplicateException():
    # test making duplicate data source
    with pytest.raises(AuroraXDuplicateException):
        existing_source = aurorax.sources.get("test-program", "test-platform", "test-instrument-type", "full_record")
        
        if not existing_source:
            assert False

        existing_source.identifier = None
        
        # make request
        aurorax.sources.add(existing_source)


def test_AuroraXValidationException_ephemeris():
    with pytest.raises(AuroraXValidationException):
        # set values
        program = "test-program"
        platform = "test-platform"
        instrument_type = "test-instrument-type"
        metadata = {
            "test_meta1": "testing1",
            "test_meta2": "testing2",
        }
        epoch = datetime.datetime(2020, 1, 1, 0, 1)
        location_geo = aurorax.Location(lat=51.049999, lon=-114.066666)
        location_gsm = aurorax.Location(lat=150.25, lon=-10.75)
        nbtrace = aurorax.Location(lat=1.23, lon=45.6)
        sbtrace = aurorax.Location(lat=7.89, lon=101.23)

        # get the ephemeris source ID
        source = aurorax.sources.get(program, platform, instrument_type, format="basic_info")
        source.instrument_type = "wrong-type"

        # create Ephemeris object
        e = aurorax.ephemeris.Ephemeris(data_source=source,
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
        aurorax.ephemeris.upload(source.identifier, records, True)


def test_AuroraXValidationException_data_product():
    with pytest.raises(AuroraXValidationException):
        # set values
        program = "test-program"
        platform = "test-platform"
        instrument_type = "test-instrument-type"
        url = "test.jpg"
        metadata = {
            "test_meta1": "testing1",
            "test_meta2": "testing2",
        }
        data_product_type = "keogram"
        start_dt = datetime.datetime(2020, 1, 2, 0, 0, 0)
        end_dt = start_dt.replace(hour=23, minute=59, second=59)

        # get the data source ID
        source = aurorax.sources.get(program, platform, instrument_type)
        source.instrument_type = "wrong-instrument"

        # create DataProducts object
        e = aurorax.data_products.DataProduct(data_source=source,
                                            data_product_type=data_product_type,
                                            url=url,
                                            start=start_dt,
                                            end=end_dt,
                                            metadata=metadata)

        # set records array
        records = []
        records.append(e)

        # upload record
        aurorax.data_products.upload(source.identifier, records, True)


@pytest.fixture(scope="function")
def set_bad_api_key():
    api_key = aurorax.api.get_api_key()
    aurorax.api.authenticate(api_key[:-1])
    yield

    aurorax.api.authenticate(api_key)


def test_AuroraXUnauthorizedException(set_bad_api_key):
    with pytest.raises(AuroraXUnauthorizedException):
        req = aurorax.AuroraXRequest(method="get", url=aurorax.api.urls.base_url + ACCOUNTS_URL)
        
        req.execute()


def test_AuroraXConflictException():
    with pytest.raises(AuroraXConflictException):
        # add a record for the test instrument, then try deleting the instrument
        # set values
        program = "test-program"
        platform = "test-platform"
        instrument_type = "test-instrument-type"
        metadata = {
            "test_meta1": "testing1",
            "test_meta2": "testing2",
        }
        epoch = datetime.datetime(2020, 1, 1, 0, 6)
        location_geo = aurorax.Location(lat=51.049999, lon=-114.066666)
        location_gsm = aurorax.Location(lat=150.25, lon=-10.75)
        nbtrace = aurorax.Location(lat=1.23, lon=45.6)
        sbtrace = aurorax.Location(lat=7.89, lon=101.23)

        # get the ephemeris source ID
        source = aurorax.sources.get(program, platform, instrument_type)

        e = aurorax.ephemeris.Ephemeris(data_source=source,
                                        epoch=epoch,
                                        location_geo=location_geo,
                                        location_gsm=location_gsm,
                                        nbtrace=nbtrace,
                                        sbtrace=sbtrace,
                                        metadata=metadata)

        # set records array
        records = [e]

        # upload record
        aurorax.ephemeris.upload(source.identifier, records=records)
        time.sleep(10)

        # try deleting the test instrument
        aurorax.sources.delete(source.identifier)
