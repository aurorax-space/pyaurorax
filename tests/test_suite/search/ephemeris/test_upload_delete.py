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
from pyaurorax.search import Location, EphemerisData


@pytest.mark.search_rw
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
    result = aurorax.search.ephemeris.upload(ds.identifier, records, validate_source=True, chunk_size=1)
    assert result == 0

    # briefly sleep, arbitrary amount > a few seconds
    time.sleep(5)

    # cleanup by deleting the ephemeris data that was uploaded
    delete_result = aurorax.search.ephemeris.delete(
        ds,
        datetime.datetime(2020, 1, 1, 0, 0),
        datetime.datetime(2020, 1, 1, 23, 59),
    )
    assert delete_result == 0
