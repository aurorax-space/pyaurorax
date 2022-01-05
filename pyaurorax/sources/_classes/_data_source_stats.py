import datetime
import pprint
from pydantic import BaseModel
from typing import Dict
from ._data_source import DataSource

# pdoc init
__pdoc__: Dict = {}


class DataSourceStatistics(BaseModel):
    """
    Data type for data source statistics

    Attributes:
        data_source: the data source the statistics are associated with
        earliest_ephemeris_loaded: datetime.datetime of the earliest ephemeris record
        latest_ephemeris_loaded: datetime.datetime of the latest ephemeris record
        ephemeris_count: total number of ephemeris records for this data source
        earliest_data_product_loaded: datetime.datetime of the earliest data_product record
        latest_data_product_loaded: datetime.datetime of the latest data product record
        data_product_count: total number of ephemeris records for this data source
    """
    data_source: DataSource
    earliest_ephemeris_loaded: datetime.datetime = None
    latest_ephemeris_loaded: datetime.datetime = None
    ephemeris_count: int
    earliest_data_product_loaded: datetime.datetime = None
    latest_data_product_loaded: datetime.datetime = None
    data_product_count: int

    def __str__(self) -> str:
        """
        String method

        Returns:
            String format of DataSource object
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation

        Returns:
            Object representation of DataSource object
        """
        return pprint.pformat(self.__dict__)
