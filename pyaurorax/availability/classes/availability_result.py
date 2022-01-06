"""
Class definition used for containing Availability information
"""

import pyaurorax
import pprint
from pydantic import BaseModel
from typing import Dict, Optional

# pdoc init
__pdoc__: Dict = {}


class AvailabilityResult(BaseModel):
    """
    Availability result data type

    Attributes:
        data_source: a DataSource object that the records are associated with
        available_data_products: data product availability dictionary
        available_ephemeris: ephemeris availability dictionary
    """
    data_source: pyaurorax.sources.DataSource
    available_data_products: Optional[Dict[str, int]] = None
    available_ephemeris: Optional[Dict[str, int]] = None

    def __str__(self) -> str:
        """
        String method

        Returns:
            string format of AvailabilityResult
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation

        Returns:
            object representation of AvailabilityResult
        """
        return pprint.pformat(self.__dict__)
