"""
Class definition for an ephemeris record
"""

import datetime
from pydantic import BaseModel
from typing import Dict, Optional
from ...location import Location
from ...sources import DataSource

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
        metadata: metadata for this record (arbitrary keys and values)
    """
    data_source: DataSource
    epoch: datetime.datetime
    location_geo: Location
    location_gsm: Optional[Location] = Location(lat=None, lon=None)
    nbtrace: Location
    sbtrace: Location
    metadata: Optional[Dict] = None

    def to_json_serializable(self) -> Dict:
        """
        Convert object to a JSON-serializable object (ie. translate
        datetime objects to strings)

        Returns:
            a dictionary object that is JSON-serializable
        """
        # init
        d = self.__dict__

        # format epoch as str
        if (type(d["epoch"]) is datetime.datetime):
            d["epoch"] = d["epoch"].strftime("%Y-%m-%dT%H:%M:00.000Z")

        # format location
        if (type(d["location_geo"]) is Location):
            d["location_geo"] = d["location_geo"].__dict__
        if (type(d["location_gsm"]) is Location):
            d["location_gsm"] = d["location_gsm"].__dict__
        if (type(d["nbtrace"]) is Location):
            d["nbtrace"] = d["nbtrace"].__dict__
        if (type(d["sbtrace"]) is Location):
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
        # shorten the metadata
        max_len = 20
        attr_metadata = f"{self.metadata}"
        if (len(attr_metadata) > max_len):
            attr_metadata = attr_metadata[0:max_len] + "...}"

        # return formatted representation
        return f"Ephemeris(data_source={repr(self.data_source)}, epoch={repr(self.epoch)}, " \
            f"location_geo={repr(self.location_geo)}, location_gsm={repr(self.location_gsm)}, " \
            f"nbtrace={repr(self.nbtrace)}, nbtrace={repr(self.nbtrace)}, " \
            f"metadata={attr_metadata})"
