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
Utility methods. For example, converting arbitrary geographic locations to North/South 
B-trace geographic locations.
"""

import datetime
from ..location import Location
from ._calculate_btrace import ground_geo_to_nbtrace as func_ground_geo_to_nbtrace
from ._calculate_btrace import ground_geo_to_sbtrace as func_ground_geo_to_sbtrace


class UtilManager:
    """
    The UtilManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    def __init__(self):
        pass

    def ground_geo_to_nbtrace(self, geo_location: Location, timestamp: datetime.datetime) -> Location:
        """
        Convert geographic location to North B-Trace geographic location

        The timestamp is required because when calculating the B-trace values, the 
        location is converted into geomagnetic coordinates using AACGM. This conversion 
        is different  based on the timestamp since the magnetic coordinates change over time.

        Args:
            geo_location (Location): a Location object representing the geographic location
            dt (datetime.datetime): timestamp for this set of latitudes and longitudes

        Returns:
            the north B-trace location as a `Location` object
        """
        return func_ground_geo_to_nbtrace(geo_location, timestamp)

    def ground_geo_to_sbtrace(self, geo_location: Location, timestamp: datetime.datetime) -> Location:
        """
        Convert geographic location to South B-Trace geographic location

        The timestamp is required because when calculating the B-trace values, the 
        location is converted into geomagnetic coordinates using AACGM. This conversion 
        is different  based on the timestamp since the magnetic coordinates change over time.

        Args:
            geo_location (Location): a Location object representing the geographic location
            dt (datetime.datetime): timestamp for this set of latitudes and longitudes

        Returns:
            the south B-trace location as a `Location` object
        """
        return func_ground_geo_to_sbtrace(geo_location, timestamp)
