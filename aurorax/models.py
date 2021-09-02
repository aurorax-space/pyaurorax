"""
This module contains the Location class.
"""
from pydantic import BaseModel, validator
from typing import Union


class Location(BaseModel):
    """
    Class representing an AuroraX location (ie. geographic coordinates, GSM coordinates,
    northern/southern magnetic footprints).

    Attributes:
        lat: latitude (degrees East).
        lon: longitude (degrees North).

    """
    lat: Union[float, None]
    lon: Union[float, None]

    @validator("lon")
    def both_must_be_none_or_number(cls, v, values):
        if (v and not values["lat"]) or (values["lat"] and not v):
            raise ValueError(
                "lat and lon must both be numbers or both be None")
        return v

    def __str__(self) -> str:
        """
        String method.

        Returns:
            String format of Location object.

        """
        return str(self.__dict__)

    def __repr__(self) -> str:
        """
        Object representation.

        Returns:
            Object representation of Location object.

        """
        return "%s(lat=%s, lon=%s)" % (self.__class__.__name__, str(self.lat), str(self.lon))
