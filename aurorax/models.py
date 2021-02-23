from pydantic import BaseModel
from typing import Union


class Location(BaseModel):
    """
    Class representing an AuroraX locations (ie. geographic coordinates,
    GSM coordinates, northern/southern magnetic footprints)

    :param lat: latitude
    :type lat: float
    :param lon: longitude
    :type lon: float
    """
    lat: Union[float, None]
    lon: Union[float, None]

    def __str__(self) -> str:
        """
        String method

        :return: string format
        :rtype: str
        """
        return str(self.__dict__)

    def __repr__(self) -> str:
        """
        Object representation

        :return: object representation
        :rtype: str
        """
        return "%s(lat=%s, lon=%s)" % (self.__class__.__name__, str(self.lat), str(self.lon))
