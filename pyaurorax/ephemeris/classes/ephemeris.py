"""
Class definition for an ephemeris record
"""

import pyaurorax
import datetime
import pprint
from pydantic import BaseModel
from typing import Dict, Optional

# pdoc init
__pdoc__: Dict = {}


class Ephemeris(BaseModel):
    """
    Ephemeris object

    Attributes:
        data_source: data source that the ephemeris record is associated with
        epoch: timestamp for the record (assumed it is in UTC)
        location_geo: Location object containing geographic latitude and longitude
        location_gsm: Location object containing GSM latitude and longitude (leave
            empty for data sources with a type of 'ground')
        nbtrace: Location object with north B-trace geographic latitude and longitude
        sbtrace: Location object with south B-trace geographic latitude and longitude
        metadata: metadata for this record
    """
    data_source: pyaurorax.sources.DataSource
    epoch: datetime.datetime
    location_geo: pyaurorax.Location
    location_gsm: Optional[pyaurorax.Location] = pyaurorax.Location(lat=None, lon=None)
    nbtrace: pyaurorax.Location
    sbtrace: pyaurorax.Location
    metadata: Dict = None

    def to_json_serializable(self) -> Dict:
        """
        Convert object to a JSON-serializable object (ie. translate
        datetime objects to strings)

        Returns:
            a dictionary object that is JSON-serializable
        """
        d = self.__dict__

        # format epoch as str
        if (type(d["epoch"]) is datetime.datetime):
            d["epoch"] = d["epoch"].strftime("%Y-%m-%dT%H:%M:00.000Z")

        # format location
        if (type(d["location_geo"]) is pyaurorax.Location):
            d["location_geo"] = d["location_geo"].__dict__
        if (type(d["location_gsm"]) is pyaurorax.Location):
            d["location_gsm"] = d["location_gsm"].__dict__
        if (type(d["nbtrace"]) is pyaurorax.Location):
            d["nbtrace"] = d["nbtrace"].__dict__
        if (type(d["sbtrace"]) is pyaurorax.Location):
            d["sbtrace"] = d["sbtrace"].__dict__

        # format metadata
        if (type(self.metadata) is dict):
            for key, value in self.metadata.items():
                if (type(value) is datetime.datetime or type(value) is datetime.date):
                    self.metadata[key] = self.metadata[key].strftime("%Y-%m-%dT%H:%M:%S.%f")
        if (type(self.metadata) is list):
            self.metadata = {}

        # format data source fields for query
        d["program"] = self.data_source.program
        d["platform"] = self.data_source.platform
        d["instrument_type"] = self.data_source.instrument_type
        del d["data_source"]

        # return
        return d

    def __str__(self) -> str:
        """
        String method

        Returns:
            string format of Ephemeris
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation

        Returns:
            object representation of Ephemeris
        """
        return pprint.pformat(self.__dict__)
