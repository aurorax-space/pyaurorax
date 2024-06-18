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
"""
Helper functions for calculating the north and south B-trace geographic
locations for ground-based instruments.
"""

import datetime
import aacgmv2
from ..location import Location


def __calculate_btrace(geo_location: Location, dt: datetime.datetime) -> Location:
    # convert to magnetic coordinates
    mag_location = aacgmv2.convert_latlon(geo_location.lat, geo_location.lon, 0.0, dt, method_code="G2A")

    # change magnetic latitude to other hemisphere
    mag_location = (mag_location[0] * -1.0, mag_location[1], mag_location[2])

    # convert magnetic coordinates back to geographic
    btrace_aacgm = aacgmv2.convert_latlon(mag_location[0], mag_location[1], mag_location[2], dt, method_code="A2G")

    # return as Location object
    return Location(lat=btrace_aacgm[0], lon=btrace_aacgm[1])


def ground_geo_to_nbtrace(geo_location: Location, timestamp: datetime.datetime) -> Location:
    """
    Convert geographic location to North B-Trace geographic
    location

    The timestamp is required because when calculating the B-trace
    values, the location is converted into geomagnetic coordinates.
    This conversion is different based on the timestamp since the
    magnetic coordinates change over time.

    Args:
        geo_location: a Location object representing the
            geographic location
        dt: timestamp for this set of lat and lons

    Returns:
        the north B-trace location as a Location object
    """
    # check if location is in northern hemisphere
    if (geo_location.lat is not None and geo_location.lat >= 0.0):
        # northern hemisphere, north b-trace is the same as geographic location
        return geo_location

    # calculate South B-trace and return
    sbtrace = __calculate_btrace(geo_location, timestamp)
    return sbtrace


def ground_geo_to_sbtrace(geo_location: Location, timestamp: datetime.datetime) -> Location:
    """
    Convert geographic location to South B-Trace geographic
    location

    The timestamp is required because when calculating the B-trace
    values, the location is converted into geomagnetic coordinates.
    This conversion is different based on the timestamp since the
    magnetic coordinates change over time.

    Args:
        geo_location: a Location object representing the
            geographic location
        dt: timestamp for this set of lat and lons

    Returns:
        the south B-trace location as a Location object
    """
    # check if location is in southern hemisphere
    if (geo_location.lat is not None and geo_location.lat < 0.0):
        # southern hemisphere, south b-trace is the same as geographic location
        return geo_location

    # calculate North B-trace and return
    nbtrace = __calculate_btrace(geo_location, timestamp)
    return nbtrace
