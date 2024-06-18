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
AuroraX `pyaurorax.search.location.Location` class definition
"""

from typing import Optional, Dict


class Location:
    """
    Representation for an AuroraX location, such as geographic coordinates, GSM coordinates,
    or northern/southern B-trace magnetic footprints.

    Latitude and longitude values are in decimal degrees format, ranging from -90 to 90
    for latitude and -180 to 180 for longitude.

    Note that latitude and longitude must both be numbers, or both be None.

    Attributes:
        lat (float): latitude value
        lon (float): longitude value
    
    Raises:
        ValueError: if both latitude and longitude are not real numbers, or not both None.
    """

    def __init__(self, lat: Optional[float] = None, lon: Optional[float] = None):
        if (lat is None and lon is not None) or (lat is not None and lon is None):
            # one of them is None, not allowed
            raise ValueError("Latitude and longitude must both be numbers, or both be None")
        self.__lat = lat
        self.__lon = lon

    @property
    def lat(self):
        return self.__lat

    @lat.setter
    def lat(self, value: float):
        if (self.__lon is None and value is not None) or (self.__lon is not None and value is None):
            # one of them is None, not allowed
            raise ValueError("Latitude and longitude must both be numbers, or both be None")
        self.__lat = value

    @property
    def lon(self):
        return self.__lon

    @lon.setter
    def lon(self, value: float):
        if (self.__lat is None and value is not None) or (self.__lat is not None and value is None):
            # one of them is None, not allowed
            raise ValueError("Latitude and longitude must both be numbers, or both be None")
        self.__lon = value

    def to_json_serializable(self) -> Dict:
        """
        Convert object to a JSON-serializable object (ie. translate
        datetime objects to strings)

        Returns:
            a dictionary object that is JSON-serializable
        """
        return {"lat": self.lat, "lon": self.lon}

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "%s(lat=%s, lon=%s)" % (self.__class__.__name__, str(self.lat), str(self.lon))
