"""
Class definition for a conjunction
"""

import pyaurorax
import pprint
import datetime
from pydantic import BaseModel
from typing import Dict, List

# pdoc init
__pdoc__: Dict = {}


class Conjunction(BaseModel):
    """
    Conjunction data type

    Attributes:
        conjunction_type: the type of location data used when the conjunction
            was found. It can either be "nbtrace" or "sbtrace"
        start: start timestamp of conjunction
        end: end timestamp of conjunction
        data_sources: data sources in the conjunction
        min_distance: minimum kilometer distance of conjunction
        max_distance: maximum kilometer distance of conjunction
        events: list of dictionaries containing details of sub-conjunctions
    """
    conjunction_type: str
    start: datetime.datetime
    end: datetime.datetime
    data_sources: List[pyaurorax.sources.DataSource]
    min_distance: float
    max_distance: float
    events: List[Dict]

    def __str__(self) -> str:
        """
        String method

        Returns:
            string format of Conjunction object
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation

        Returns:
            object representation of Conjunction object
        """
        return pprint.pformat(self.__dict__)
