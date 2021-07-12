import pprint
from aurorax.sources import DataSource
import datetime
from pydantic import BaseModel
from typing import Dict, List


class Conjunction(BaseModel):
    """
    Conjunction data type
    
    :param conjunction_type: conjunction type "nbtrace" or "sbtrace"
    :type conjunction_type: str

    :param start: start time of conjunction event(s)
    :type start: datetime.datetime

    :param end: end time of conjunction event(s)
    :type end: datetime.datetime

    :param data_sources: data sources in conjunction
    :type data_sources: List[aurorax.sources.DataSource]

    :param min_distance: minimum distance of conjunction event(s)
    :type min_distance: float

    :param max_distance: maximum distance of conjunction event(s)
    :type max_distance: float

    :param events: details of individual conjunction events
    :type events: List[DIct]
    """
    conjunction_type: str
    start: datetime.datetime 
    end: datetime.datetime
    data_sources: List[DataSource]
    min_distance: float
    max_distance: float
    events: List[Dict]

    def __str__(self) -> str:
        """
        String method

        :return: string format
        :rtype: str
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation

        :return: object representation
        :rtype: str
        """
        return pprint.pformat(self.__dict__)


