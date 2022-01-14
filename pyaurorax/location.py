"""
The Location module provides a class used throughout the PyAuroraX
library to manage lat/lon positions of different things.
"""

from pydantic import BaseModel, validator
from typing import Union, Optional


class Location(BaseModel):
    """
    Class representing an AuroraX location (ie. geographic coordinates,
    GSM coordinates, northern/southern B-trace magnetic footprints)

    The numbers are in decimal degrees format and range from -90 to 90
    for latitude and -180 to 180 for longitude.

    Attributes:
        lat: latitude value
        lon: longitude value
    """
    lat: Optional[Union[float, None]] = None
    lon: Optional[Union[float, None]] = None

    @validator("lon")
    def __both_must_be_none_or_number(cls, v, values):  # pylint: disable=unused-private-member
        # check to make sure the values are both numbers or None types. We don't
        # allow a Location object to have the latitude set and not the
        # longitude (or vice-versa)
        if (v and not values["lat"]) or (values["lat"] and not v):
            raise ValueError("Latitude and longitude must both be numbers, or both be None")
        return v

    def __str__(self) -> str:
        """
        String method

        Returns:
            string format of Location object
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation

        Returns:
            object representation of Location object
        """
        return "%s(lat=%s, lon=%s)" % (self.__class__.__name__, str(self.lat), str(self.lon))
