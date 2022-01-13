"""
Class definition used for containing Availability information
"""

from pydantic import BaseModel
from typing import Dict, Optional
from ...sources import DataSource

# pdoc init
__pdoc__: Dict = {}


class AvailabilityResult(BaseModel):
    """
    Availability information object

    Attributes:
        data_source: the data source that the records are associated with
        available_data_products: the data product availability information
        available_ephemeris: the ephemeris availability information
    """
    data_source: DataSource
    available_data_products: Optional[Dict[str, int]] = None
    available_ephemeris: Optional[Dict[str, int]] = None

    def __str__(self) -> str:
        """
        String method

        Returns:
            string format of AvailabilityResult
        """
        return self.__repr__()
