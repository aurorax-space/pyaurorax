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
        conjunction_type: conjunction type "nbtrace" or "sbtrace"
        start: start datetime.datetime of conjunction event(s)
        end: end datetime.datetime of conjunction event(s)
        data_sources: pyaurorax.sources.DataSource sources in the conjunction
        min_distance: minimum kilometre distance of conjunction event(s), float
        max_distance: maximum kilometre distance of conjunction event(s), float
        events: list of dictionaries containing details of individual conjunction events
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
            String format of Conjunction object
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation

        Returns:
            Object representation of Conjunction object
        """
        return pprint.pformat(self.__dict__)
