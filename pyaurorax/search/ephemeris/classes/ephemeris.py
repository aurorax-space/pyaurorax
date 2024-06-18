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
Class definition for an ephemeris record
"""

import datetime
from typing import Dict, Optional
from ...location import Location
from ...sources.classes.data_source import DataSource


class EphemerisData:
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

    def __init__(self,
                 data_source: DataSource,
                 epoch: datetime.datetime,
                 location_geo: Optional[Location] = None,
                 nbtrace: Optional[Location] = None,
                 sbtrace: Optional[Location] = None,
                 location_gsm: Optional[Location] = None,
                 metadata: Optional[Dict] = None):
        self.data_source = data_source
        self.epoch = epoch
        self.location_geo = Location(lat=None, lon=None) if location_geo is None else location_geo
        self.nbtrace = Location(lat=None, lon=None) if nbtrace is None else nbtrace
        self.sbtrace = Location(lat=None, lon=None) if sbtrace is None else sbtrace
        self.location_gsm = Location(lat=None, lon=None) if location_gsm is None else location_gsm
        self.metadata = metadata

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
        if (isinstance(d["epoch"], datetime.datetime) is True):
            d["epoch"] = d["epoch"].strftime("%Y-%m-%dT%H:%M:00.000Z")

        # format location
        if (isinstance(d["location_geo"], Location) is True):
            d["location_geo"] = d["location_geo"].to_json_serializable()
        if (isinstance(d["location_gsm"], Location) is True):
            d["location_gsm"] = d["location_gsm"].to_json_serializable()
        if (isinstance(d["nbtrace"], Location) is True):
            d["nbtrace"] = d["nbtrace"].to_json_serializable()
        if (isinstance(d["sbtrace"], Location) is True):
            d["sbtrace"] = d["sbtrace"].to_json_serializable()

        # format metadata
        if (self.metadata is not None):
            for key, value in self.metadata.items():
                if (isinstance(value, datetime.datetime) is True or isinstance(value, datetime.date) is True):
                    self.metadata[key] = self.metadata[key].strftime("%Y-%m-%dT%H:%M:%S.%f")
        # if (isinstance(self.metadata, list) is True):
        #     self.metadata = {}

        # format data source fields for query
        d["program"] = self.data_source.program
        d["platform"] = self.data_source.platform
        d["instrument_type"] = self.data_source.instrument_type
        del d["data_source"]

        # return
        return d

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        # shorten the metadata
        max_len = 20
        attr_metadata = f"{self.metadata}"
        if (len(attr_metadata) > max_len):
            attr_metadata = attr_metadata[0:max_len] + "...}"

        # return formatted representation
        return f"EphemerisData(epoch={repr(self.epoch)}, location_geo={repr(self.location_geo)}, " \
            f"location_gsm={repr(self.location_gsm)}, nbtrace={repr(self.nbtrace)}, sbtrace={repr(self.sbtrace)}, " \
            f"metadata={attr_metadata}, data_source=DataSource(...))"
