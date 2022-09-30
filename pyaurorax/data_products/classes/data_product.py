"""
Class definition for a data product
"""

import datetime
from pydantic import BaseModel
from typing import Dict
from ...sources import DataSource

# pdoc init
__pdoc__: Dict = {}


class DataProduct(BaseModel):
    """
    Data product object

    Attributes:
        data_source: data source that the ephemeris record is associated with
        data_product_type: data product type ("keogram", "movie", "summary_plot")
        start: starting timestamp for the record (assumed it is in UTC), inclusive
        end: ending timestamp for the record (assumed it is in UTC), inclusive
        url: the URL of data product
        metdata: metadata for this record (arbitrary keys and values)
    """
    data_source: DataSource
    data_product_type: str
    start: datetime.datetime
    end: datetime.datetime
    url: str
    metadata: Dict

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
        if (type(d["start"]) is datetime.datetime):
            d["start"] = d["start"].strftime("%Y-%m-%dT%H:%M:00.000")
        if (type(d["end"]) is datetime.datetime):
            d["end"] = d["end"].strftime("%Y-%m-%dT%H:%M:00.000")

        # format metadata
        if (type(self.metadata) is dict):
            for key, value in self.metadata.items():
                if (type(value) is datetime.datetime or type(value) is datetime.date):
                    self.metadata[key] = self.metadata[key].strftime(
                        "%Y-%m-%dT%H:%M:%S.%f")
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
            string format of DataProduct object
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation

        Returns:
            object representation of DataProduct object
        """
        # shorten the metadata and url
        max_len = 20
        attr_metadata = f"{self.metadata}"
        if (len(attr_metadata) > max_len):
            attr_metadata = attr_metadata[0:max_len] + "...}"
        attr_url = f"{self.url}"
        if (len(attr_url) > max_len):
            attr_url = attr_url[0:max_len] + "..."

        # return formatted representation
        return f"DataProduct(data_source={repr(self.data_source)}, start={repr(self.start)}, " \
            f"end={repr(self.end)}, data_product_type='{self.data_product_type}', url='{attr_url}', " \
            f"metadata={attr_metadata})"
