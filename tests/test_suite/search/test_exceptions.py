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
from pyaurorax import (
    AuroraXConflictError,
    AuroraXDuplicateError,
    AuroraXNotFoundError,
    AuroraXError,
)
from pyaurorax.search import FORMAT_FULL_RECORD, FORMAT_BASIC_INFO, Location, EphemerisData, DataProductData

# globals
ACCOUNTS_URL = "/api/v1/accounts"


@pytest.mark.search_exceptions
def test_auroraxnotfound_error(aurorax):
    # test finding a source that doesn't exist
    with pytest.raises(AuroraXNotFoundError):
        aurorax.search.sources.get("does-not-exist", "does-not-exist", "does-not-exist")


@pytest.mark.search_exceptions
def test_auroraxduplicate_error(aurorax):
    # test making duplicate data source
    with pytest.raises(AuroraXDuplicateError):
        ds = aurorax.search.sources.get(
            "test-program",
            "test-platform",
            "test-instrument-type",
            format=FORMAT_FULL_RECORD,
        )
        ds.identifier = None
        aurorax.search.sources.add(ds)


@pytest.mark.search_exceptions
def test_ephemeris_aurorax_error(aurorax):
    with pytest.raises(AuroraXError):
        # set values
        program = "test-program"
        platform = "test-platform"
        instrument_type = "test-instrument-type"
        metadata = {
            "test_meta1": "testing1",
            "test_meta2": "testing2",
        }
        epoch = datetime.datetime(2020, 1, 1, 0, 1)
        location_geo = Location(lat=51.049999, lon=-114.066666)
        location_gsm = Location(lat=150.25, lon=-10.75)
        nbtrace = Location(lat=1.23, lon=45.6)
        sbtrace = Location(lat=7.89, lon=101.23)

        # get the data source ID
        source = aurorax.search.sources.get(program, platform, instrument_type, format=FORMAT_BASIC_INFO)
        source.instrument_type = "wrong-type"

        # create Ephemeris object
        e = EphemerisData(data_source=source,
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
        aurorax.search.ephemeris.upload(source.identifier, records, True)


@pytest.mark.search_exceptions
def test_data_product_aurorax_error(aurorax):
    with pytest.raises(AuroraXError):
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
        source = aurorax.search.sources.get(program, platform, instrument_type)
        source.instrument_type = "wrong-instrument"

        # create DataProducts object
        e = DataProductData(data_source=source, data_product_type=data_product_type, url=url, start=start_dt, end=end_dt, metadata=metadata)

        # set records array
        records = []
        records.append(e)

        # upload record
        aurorax.search.data_products.upload(source.identifier, records, True)


@pytest.mark.search_exceptions
def test_auroraxconflict_error(aurorax):
    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    metadata = {
        "test_meta1": "testing1",
        "test_meta2": "testing2",
    }

    # get the data source ID
    ds = aurorax.search.sources.get(program, platform, instrument_type)

    # add a record for the test instrument, then try deleting the instrument
    epoch = datetime.datetime(2020, 3, 1, 0, 6)
    location_geo = Location(lat=51.049999, lon=-114.066666)
    location_gsm = Location(lat=150.25, lon=-10.75)
    nbtrace = Location(lat=1.23, lon=45.6)
    sbtrace = Location(lat=7.89, lon=101.23)

    # create ephemeris record
    record = EphemerisData(data_source=ds,
                           epoch=epoch,
                           location_geo=location_geo,
                           location_gsm=location_gsm,
                           nbtrace=nbtrace,
                           sbtrace=sbtrace,
                           metadata=metadata)

    # set records array
    records = [record]

    # upload record
    result = aurorax.search.ephemeris.upload(ds.identifier, records=records)
    assert result == 0

    with pytest.raises(AuroraXConflictError):
        # try deleting the test instrument
        aurorax.search.sources.delete(ds.identifier)

    # delete the ephemeris data
    result = aurorax.search.ephemeris.delete(
        ds,
        datetime.datetime(2020, 3, 1, 0, 0),
        datetime.datetime(2020, 3, 1, 0, 59),
    )
    assert result == 0
