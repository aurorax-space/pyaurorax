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
from pyaurorax.search import Location, EphemerisData, DataSource


@pytest.mark.search_ro
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
    e = EphemerisData(
        data_source=data_source,
        epoch=epoch,
        location_geo=location_geo,
        nbtrace=nbtrace,
        sbtrace=sbtrace,
        metadata=metadata,
    )

    # check
    assert isinstance(e, EphemerisData) is True
    assert isinstance(e.data_source, DataSource) is True
    assert e.data_source.program == program
    assert e.data_source.platform == platform
    assert e.data_source.instrument_type == instrument_type
