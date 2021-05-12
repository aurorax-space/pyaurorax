import aurorax
from aurorax.exceptions import *
import datetime
import os
import pytest
import time

ACCOUNTS_URL = "/api/v1/accounts"
aurorax.api.set_base_url("https://api.staging.aurorax.space")

def test_AuroraXNotFoundException():
    # test finding a source that doesn't exist
    with pytest.raises(AuroraXNotFoundException):
        aurorax.sources.get("does-not-exist", "does-not-exist", "does-not-exist")


def test_AuroraXDuplicateException():
    # test making duplicate data source
    with pytest.raises(AuroraXDuplicateException):
        aurorax.api.authenticate(os.getenv("AURORAX_APIKEY_STAGING"))

        existing_source = aurorax.sources.get("test-program", "test-platform", "test-instrument-type", "full_record")
        
        if not existing_source:
            assert False
        
        # make request
        aurorax.sources.add(existing_source["program"],
                                existing_source["platform"],
                                existing_source["instrument_type"],
                                existing_source["source_type"],
                                existing_source["display_name"],
                                ephemeris_metadata_schema=existing_source["ephemeris_metadata_schema"],
                                data_product_metadata_schema=existing_source["data_product_metadata_schema"])


def test_AuroraXValidationException_ephemeris():
    with pytest.raises(AuroraXValidationException):
        aurorax.api.authenticate(os.getenv("AURORAX_APIKEY_STAGING"))

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
        source = aurorax.sources.get(program, platform, instrument_type, format="identifier_only")
        identifier = source["identifier"]

        # create Ephemeris object
        e = aurorax.ephemeris.Ephemeris(identifier=105,
                                        program=program, 
                                        platform="wrong-platform", 
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
        aurorax.ephemeris.upload(identifier, records=records, validate_source=True)


def test_AuroraXValidationException_data_product():
    with pytest.raises(AuroraXValidationException):
        aurorax.api.authenticate(os.getenv("AURORAX_APIKEY_STAGING"))

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
        ds = aurorax.sources.get(program, platform, instrument_type)
        identifier = ds["identifier"]

        # create DataProducts object
        e = aurorax.data_products.DataProduct(identifier=identifier,
                                            program=program,
                                            platform=platform,
                                            instrument_type="random-string",
                                            data_product_type=data_product_type,
                                            url=url,
                                            start=start_dt,
                                            end=end_dt,
                                            metadata=metadata)

        # set records array
        records = []
        records.append(e)

        # upload record
        aurorax.data_products.upload(identifier, records=records, validate_source=True)


# def test_AuroraXBadParametersException():
#     assert False


def test_AuroraXUnauthorizedException():
    with pytest.raises(AuroraXUnauthorizedException):
        aurorax.api.authenticate(os.getenv("AURORAX_APIKEY_STAGING")[:-1])

        req = aurorax.AuroraXRequest(method="get", url=aurorax.api.urls.base_url + ACCOUNTS_URL)
        
        req.execute()


def test_AuroraXConflictException():
    with pytest.raises(AuroraXConflictException):
        # add a record for the test instrument, then try deleting the instrument
        aurorax.api.authenticate(os.getenv("AURORAX_APIKEY_STAGING"))

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
        source = aurorax.sources.get(program, platform, instrument_type, format="identifier_only")
        identifier = source["identifier"]

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
        aurorax.ephemeris.upload(identifier, records=records)
        time.sleep(2)

        # try deleting the test instrument
        aurorax.sources.delete(identifier)


# not sure how to test this because the API only returns 202
# def test_AuroraXUploadException():
#     # this is raised for status code 400 which also includes duplicate records
#     with pytest.raises(AuroraXUploadException):
#         aurorax.api.authenticate(os.getenv("AURORAX_APIKEY_STAGING"))

#         # set values
#         program = "test-program"
#         platform = "test-platform"
#         instrument_type = "test-instrument-type"
#         metadata = {
#             "test_meta1": "testing1",
#             "test_meta2": "testing2",
#         }
#         epoch = datetime.datetime(2020, 1, 1, 0, 4)
#         location_geo = aurorax.Location(lat=51.049999, lon=-114.066666)
#         location_gsm = aurorax.Location(lat=150.25, lon=-10.75)
#         nbtrace = aurorax.Location(lat=1.23, lon=45.6)
#         sbtrace = aurorax.Location(lat=7.89, lon=101.23)

#         # get the ephemeris source ID
#         source = aurorax.sources.get(program, platform, instrument_type, format="identifier_only")
#         identifier = source["identifier"]
    
#         # create Ephemeris object
#         e = aurorax.ephemeris.Ephemeris(identifier=15000,
#                                         program="wrong-program", 
#                                         platform="wrong-platform", 
#                                         instrument_type=instrument_type, 
#                                         epoch=epoch,
#                                         location_geo=location_geo,
#                                         location_gsm=location_gsm,
#                                         nbtrace=nbtrace,
#                                         sbtrace=sbtrace,
#                                         metadata=metadata)

#         # set records array
#         records = []
#         records.append(e)

#         # upload record
#         aurorax.ephemeris.upload(identifier, records=records)
