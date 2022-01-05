import pyaurorax
import datetime
import pprint
from pydantic import BaseModel
from typing import Dict

# pdoc init
__pdoc__: Dict = {}


class DataProduct(BaseModel):
    """
    DataProduct data type

    Attributes:
        data_source: data source that the ephemeris record is associated with
        data_product_type: data product type ("keogram", "movie", "summary_plot")
        start: starting timestamp for the record in UTC
        end: ending timestamp for the record in UTC
        url: the URL location string of data product
        metdata: metadata dictionary for this record
    """
    data_source: pyaurorax.sources.DataSource
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
        d = self.__dict__

        # format epoch as str
        if (type(d["start"]) is datetime.datetime):
            d["start"] = d["start"].strftime("%Y-%m-%dT%H:%M:00.000Z")
        if (type(d["end"]) is datetime.datetime):
            d["end"] = d["end"].strftime("%Y-%m-%dT%H:%M:00.000Z")

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
        return pprint.pformat(self.__dict__)
