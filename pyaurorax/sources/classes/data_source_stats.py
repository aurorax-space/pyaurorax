"""
Class definition for a statistics about a data source
"""

import datetime
from pydantic import BaseModel
from typing import Dict, Optional

# pdoc init
__pdoc__: Dict = {}


class DataSourceStatistics(BaseModel):
    """
    Data source statistics object

    Attributes:
        earliest_ephemeris_loaded: timestamp of the earliest ephemeris record
        latest_ephemeris_loaded: timestamp of the latest ephemeris record
        ephemeris_count: total number of ephemeris records for this data source
        earliest_data_product_loaded: timestamp of the earliest data_product record
        latest_data_product_loaded: timestamp of the latest data product record
        data_product_count: total number of ephemeris records for this data source
    """
    earliest_ephemeris_loaded: Optional[datetime.datetime] = None
    latest_ephemeris_loaded: Optional[datetime.datetime] = None
    ephemeris_count: int
    earliest_data_product_loaded: Optional[datetime.datetime] = None
    latest_data_product_loaded: Optional[datetime.datetime] = None
    data_product_count: int

    def __str__(self) -> str:
        """
        String method

        Returns:
            string format of DataSource object
        """
        return self.__repr__()
