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
import numpy as np
from pyaurorax.search import Location


@pytest.mark.search_util
def test_convert_nbtrace_northern(aurorax):
    # set timestamp
    timestamp = datetime.datetime(2020, 1, 1, 0, 0, 0)

    lat = 56
    lon = 20

    # set geographic lat/lon
    geo_location = Location(lat=lat, lon=lon)
    nbtrace = aurorax.search.util.ground_geo_to_nbtrace(geo_location, timestamp)

    assert np.floor(nbtrace.lat) == lat and np.floor(nbtrace.lon) == lon


@pytest.mark.search_util
def test_convert_nbtrace_southern(aurorax):
    # set timestamp
    timestamp = datetime.datetime(2020, 1, 1, 0, 0, 0)

    lat = 56
    lon = 20

    # set geographic lat/lon
    geo_location = Location(lat=-lat, lon=lon)
    nbtrace = aurorax.search.util.ground_geo_to_nbtrace(geo_location, timestamp)

    assert np.floor(nbtrace.lat) == 58 and np.floor(nbtrace.lon) == -9


@pytest.mark.search_util
def test_convert_sbtrace_northern(aurorax):
    # set timestamp
    timestamp = datetime.datetime(2020, 1, 1, 0, 0, 0)

    lat = -56
    lon = 20

    # set geographic lat/lon
    geo_location = Location(lat=lat, lon=lon)
    sbtrace = aurorax.search.util.ground_geo_to_sbtrace(geo_location, timestamp)

    assert np.floor(sbtrace.lat) == lat and np.floor(sbtrace.lon) == lon


@pytest.mark.search_util
def test_convert_sbtrace_southern(aurorax):
    # set timestamp
    timestamp = datetime.datetime(2020, 1, 1, 0, 0, 0)

    lat = -56
    lon = 20

    # set geographic lat/lon
    geo_location = Location(lat=-lat, lon=lon)
    sbtrace = aurorax.search.util.ground_geo_to_sbtrace(geo_location, timestamp)

    assert np.floor(sbtrace.lat) == -48 and np.floor(sbtrace.lon) == 39
