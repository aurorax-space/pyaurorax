"""
The availability module provides the means to quickly determine the availability of
desired ephemeris or data product records in AuroraX.
"""
import pyaurorax
import datetime
import pprint
from pydantic import BaseModel
from typing import Dict, List


class AvailabilityResult(BaseModel):
    """
    Availability result data type.

    Attributes:
        data_source: pyaurorax.sources.DataSource object that the ephemeris record is associated with.
        available_data_products: data product availability dictionary of shape {"YYYY-MM-DD": <# of records>}.
        available_ephemeris: ephemeris availability dictionary of shape {"YYYY-MM-DD": <# of records>}.

    """
    data_source: pyaurorax.sources.DataSource
    available_data_products: Dict[str, int] = None
    available_ephemeris: Dict[str, int] = None

    def __str__(self) -> str:
        """
        String method.

        Returns:
            String format of AvailabilityResult.

        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation.

        Returns:
            Object representation of AvailabilityResult.

        """
        return pprint.pformat(self.__dict__)


def ephemeris(start: datetime.date,
              end: datetime.date,
              program: str = None,
              platform: str = None,
              instrument_type: str = None,
              source_type: str = None,
              owner: str = None,
              format: str = "basic_info",
              slow: bool = False) -> List[AvailabilityResult]:
    """
    Retrieve information about the number of existing ephemeris records.

    Attributes:
        start: start datetime.date.
        end: end datetime.date.
        program: program string name to filter sources by, defaults to None.
        platform: platform string name to filter sources by, defaults to None.
        instrument_type: instrument type string to filter sources by, defaults to None.
        source_type: source type string to filter sources by (heo, leo, lunar, or ground), defaults to None.
        owner: owner email address string to filter sources by, defaults to None.
        format: the format of the data sources returned (identifier_only, basic_info,
            full_record), defaults to "basic_info".
        slow: query the data directly (slower) for more accurate results, defaults to false.

    Returns:
        A list of pyaurorax.availability.AvailabilityResult objects.

    """
    # set parameters
    params = {
        "start": start.strftime("%Y-%m-%d"),
        "end": end.strftime("%Y-%m-%d"),
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "source_type": source_type,
        "owner": owner,
        "format": format,
        "slow": slow,
    }

    # do request
    req = pyaurorax.AuroraXRequest(
        method="get", url=pyaurorax.api.urls.ephemeris_availability_url, params=params)
    res = req.execute()

    # return
    return [AvailabilityResult(**av) for av in res.data]


def data_products(start: datetime,
                  end: datetime,
                  program: str = None,
                  platform: str = None,
                  instrument_type: str = None,
                  source_type: str = None,
                  owner: str = None,
                  format: str = "basic_info",
                  slow: bool = False) -> List[AvailabilityResult]:
    """
    Retrieve information about the number of existing data product records.

    Attributes:
        start: start datetime.date.
        end: end datetime.date.
        program: program string name to filter sources by, defaults to None.
        platform: platform string name to filter sources by, defaults to None.
        instrument_type: instrument type string to filter sources by, defaults to None.
        source_type: source type string to filter sources by (heo, leo, lunar, or ground), defaults to None.
        owner: owner email address string to filter sources by, defaults to None.
        format: the format of the data sources returned (identifier_only, basic_info,
            full_record), defaults to "basic_info".
        slow: query the data directly (slower) for more accurate results, defaults to false.

    Returns:
        A list of pyaurorax.availability.AvailabilityResult objects.

    """
    # set parameters
    params = {
        "start": start.strftime("%Y-%m-%d"),
        "end": end.strftime("%Y-%m-%d"),
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "source_type": source_type,
        "owner": owner,
        "format": format,
        "slow": slow,
    }

    # do request
    req = pyaurorax.AuroraXRequest(
        method="get", url=pyaurorax.api.urls.data_products_availability_url, params=params)
    res = req.execute()

    # return
    return [AvailabilityResult(**av) for av in res.data]
