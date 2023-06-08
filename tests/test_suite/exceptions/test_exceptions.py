import pytest
import datetime
import pyaurorax
from pyaurorax.exceptions import (AuroraXConflictException, AuroraXDuplicateException,
                                  AuroraXNotFoundException, AuroraXUnauthorizedException,
                                  AuroraXValidationException)

# globals
ACCOUNTS_URL = "/api/v1/accounts"


@pytest.mark.exceptions
def test_AuroraXNotFoundException():
    # test finding a source that doesn't exist
    with pytest.raises(AuroraXNotFoundException):
        pyaurorax.sources.get("does-not-exist",
                              "does-not-exist",
                              "does-not-exist")


@pytest.mark.exceptions
def test_AuroraXDuplicateException():
    # test making duplicate data source
    with pytest.raises(AuroraXDuplicateException):
        existing_source = pyaurorax.sources.get("test-program",
                                                "test-platform",
                                                "pytest",
                                                "full_record")

        if not existing_source:
            assert False

        existing_source.identifier = None

        # make request
        pyaurorax.sources.add(existing_source)


@pytest.mark.exceptions
def test_AuroraXValidationException_ephemeris():
    with pytest.raises(AuroraXValidationException):
        # set values
        program = "test-program"
        platform = "test-platform"
        instrument_type = "pytest"
        metadata = {
            "test_meta1": "testing1",
            "test_meta2": "testing2",
        }
        epoch = datetime.datetime(2020, 1, 1, 0, 1)
        location_geo = pyaurorax.Location(lat=51.049999, lon=-114.066666)
        location_gsm = pyaurorax.Location(lat=150.25, lon=-10.75)
        nbtrace = pyaurorax.Location(lat=1.23, lon=45.6)
        sbtrace = pyaurorax.Location(lat=7.89, lon=101.23)

        # get the data source ID
        source = pyaurorax.sources.get(program, platform, instrument_type,
                                       format=pyaurorax.FORMAT_BASIC_INFO)
        source.instrument_type = "wrong-type"

        # create Ephemeris object
        e = pyaurorax.ephemeris.Ephemeris(data_source=source,
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
        pyaurorax.ephemeris.upload(source.identifier, records, True)


@pytest.mark.exceptions
def test_AuroraXValidationException_data_product():
    with pytest.raises(AuroraXValidationException):
        # set values
        program = "test-program"
        platform = "test-platform"
        instrument_type = "pytest"
        url = "test.jpg"
        metadata = {
            "test_meta1": "testing1",
            "test_meta2": "testing2",
        }
        data_product_type = "keogram"
        start_dt = datetime.datetime(2020, 1, 2, 0, 0, 0)
        end_dt = start_dt.replace(hour=23, minute=59, second=59)

        # get the data source ID
        source = pyaurorax.sources.get(program, platform, instrument_type)
        source.instrument_type = "wrong-instrument"

        # create DataProducts object
        e = pyaurorax.data_products.DataProduct(data_source=source,
                                                data_product_type=data_product_type,
                                                url=url,
                                                start=start_dt,
                                                end=end_dt,
                                                metadata=metadata)

        # set records array
        records = []
        records.append(e)

        # upload record
        pyaurorax.data_products.upload(source.identifier, records, True)


@pytest.mark.exceptions
@pytest.fixture(scope="function")
def set_bad_api_key():
    api_key = pyaurorax.api.get_api_key()
    pyaurorax.authenticate(api_key[:-1])
    yield

    pyaurorax.authenticate(api_key)


@pytest.mark.exceptions
def test_AuroraXUnauthorizedException(set_bad_api_key):
    with pytest.raises(AuroraXUnauthorizedException):
        req = pyaurorax.AuroraXRequest(method="get",
                                       url=pyaurorax.api.urls.base_url + ACCOUNTS_URL)

        req.execute()


@pytest.mark.exceptions
def test_AuroraXConflictException():
    with pytest.raises(AuroraXConflictException):
        # add a record for the test instrument, then try deleting the instrument
        # set values
        program = "test-program"
        platform = "test-platform"
        instrument_type = "pytest"
        metadata = {
            "test_meta1": "testing1",
            "test_meta2": "testing2",
        }
        epoch = datetime.datetime(2020, 1, 1, 0, 6)
        location_geo = pyaurorax.Location(lat=51.049999, lon=-114.066666)
        location_gsm = pyaurorax.Location(lat=150.25, lon=-10.75)
        nbtrace = pyaurorax.Location(lat=1.23, lon=45.6)
        sbtrace = pyaurorax.Location(lat=7.89, lon=101.23)

        # get the data source ID
        source = pyaurorax.sources.get(program, platform, instrument_type)

        # create ephemeris record
        record = pyaurorax.ephemeris.Ephemeris(data_source=source,
                                               epoch=epoch,
                                               location_geo=location_geo,
                                               location_gsm=location_gsm,
                                               nbtrace=nbtrace,
                                               sbtrace=sbtrace,
                                               metadata=metadata)

        # set records array
        records = [record]

        # upload record
        pyaurorax.ephemeris.upload(source.identifier, records=records)

        # try deleting the test instrument
        pyaurorax.sources.delete(source.identifier)
