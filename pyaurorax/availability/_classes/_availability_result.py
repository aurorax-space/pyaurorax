import pyaurorax
import pprint
from pydantic import BaseModel
from typing import Dict

# pdoc init
__pdoc__: Dict = {}


class AvailabilityResult(BaseModel):
    """
    Availability result data type

    Attributes:
        data_source: DataSource object that the records are associated with
        available_data_products: data product availability dictionary
        available_ephemeris: ephemeris availability dictionary
    """
    data_source: pyaurorax.sources.DataSource
    available_data_products: Dict[str, int] = None
    available_ephemeris: Dict[str, int] = None

    def __str__(self) -> str:
        """
        String method

        Returns:
            String format of AvailabilityResult
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation

        Returns:
            Object representation of AvailabilityResult
        """
        return pprint.pformat(self.__dict__)
