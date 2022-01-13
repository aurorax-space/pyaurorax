"""
Functions for retrieving availablity information
"""

import datetime
from typing import Dict, List, Optional
from .classes.availability_result import AvailabilityResult
from ..sources import FORMAT_DEFAULT, DataSource
from ..api import urls, AuroraXRequest

# pdoc init
__pdoc__: Dict = {}


def ephemeris(start: datetime.date,
              end: datetime.date,
              program: Optional[str] = None,
              platform: Optional[str] = None,
              instrument_type: Optional[str] = None,
              source_type: Optional[str] = None,
              owner: Optional[str] = None,
              format: Optional[str] = FORMAT_DEFAULT,
              slow: Optional[bool] = False) -> List[AvailabilityResult]:
    """
    Retrieve information about the number of existing ephemeris records

    Args:
        start: start date to retrieve availability info from (inclusive)
        end: end date to retrieve availability info until (inclusive)
        program: program name to filter sources by, defaults to None
        platform: platform name to filter sources by, defaults to None
        instrument_type: instrument type to filter sources by, defaults to None
        source_type: source type to filter sources by, defaults to None. Other
            options are in the pyaurorax.sources module, or at the top level
            using the pyaurorax.SOURCE_TYPE_* variables.
        owner: owner email address to filter sources by, defaults to None
        format: the format of the data sources returned, defaults to "basic_info".
            Other options are in the pyaurorax.sources module, or at the top level
            using the pyaurorax.FORMAT_* variables.
        slow: query the data using a slower, but more accurate method, defaults to False

    Returns:
        ephemeris availability information matching the requested parameters
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
    req = AuroraXRequest(method="get",
                         url=urls.ephemeris_availability_url,
                         params=params)
    res = req.execute()

    # cast data source record
    for i in range(0, len(res.data)):
        ds = DataSource(**res.data[i]["data_source"], format=format)
        res.data[i]["data_source"] = ds

    # return
    return [AvailabilityResult(**av) for av in res.data]


def data_products(start: datetime.date,
                  end: datetime.date,
                  program: Optional[str] = None,
                  platform: Optional[str] = None,
                  instrument_type: Optional[str] = None,
                  source_type: Optional[str] = None,
                  owner: Optional[str] = None,
                  format: Optional[str] = FORMAT_DEFAULT,
                  slow: Optional[bool] = False) -> List[AvailabilityResult]:
    """
    Retrieve information about the number of existing data product records

    Args:
        start: start date to retrieve availability info from (inclusive)
        end: end date to retrieve availability info until (inclusive)
        program: program name to filter sources by, defaults to None
        platform: platform name to filter sources by, defaults to None
        instrument_type: instrument type to filter sources by, defaults to None
        source_type: source type to filter sources by, defaults to None. Other
            options are in the pyaurorax.sources module, or at the top level
            using the pyaurorax.SOURCE_TYPE_* variables.
        owner: owner email address to filter sources by, defaults to None
        format: the format of the data sources returned, defaults to "basic_info".
            Other options are in the pyaurorax.sources module, or at the top level
            using the pyaurorax.FORMAT_* variables.
        slow: query the data using a slower, but more accurate method, defaults to False

    Returns:
        data product availability information matching the requested parameters
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
    req = AuroraXRequest(method="get",
                         url=urls.data_products_availability_url,
                         params=params)
    res = req.execute()

    # cast data source record
    for i in range(0, len(res.data)):
        ds = DataSource(**res.data[i]["data_source"], format=format)
        res.data[i]["data_source"] = ds

    # return
    return [AvailabilityResult(**av) for av in res.data]
