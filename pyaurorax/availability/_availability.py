import pyaurorax
import datetime
from typing import Dict, List, Optional
from ._classes._availability_result import AvailabilityResult

# pdoc init
__pdoc__: Dict = {}


def ephemeris(start: datetime.date,
              end: datetime.date,
              program: Optional[str] = None,
              platform: Optional[str] = None,
              instrument_type: Optional[str] = None,
              source_type: Optional[str] = None,
              owner: Optional[str] = None,
              format: Optional[str] = "basic_info",
              slow: Optional[bool] = False) -> List[AvailabilityResult]:
    """
    Retrieve information about the number of existing ephemeris records

    Args:
        start: start date to retrieve availability info from (inclusive)
        end: end date to retrieve availability info to (inclusive)
        program: program string name to filter sources by, defaults to None
        platform: platform string name to filter sources by, defaults to None
        instrument_type: instrument type string to filter sources by, defaults to None
        source_type: source type string to filter sources by, defaults to None
        owner: owner email address string to filter sources by, defaults to None
        format: the format of the data sources returned (identifier_only, basic_info,
            full_record, with_metadata), defaults to "basic_info"
        slow: query the data directly (slower) for more accurate results, defaults to false

    Returns:
        a list of pyaurorax.availability.AvailabilityResult objects
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
    req = pyaurorax.AuroraXRequest(method="get",
                                   url=pyaurorax.api.urls.ephemeris_availability_url,
                                   params=params)
    res = req.execute()

    # return
    return [AvailabilityResult(**av) for av in res.data]


def data_products(start: datetime,
                  end: datetime,
                  program: Optional[str] = None,
                  platform: Optional[str] = None,
                  instrument_type: Optional[str] = None,
                  source_type: Optional[str] = None,
                  owner: Optional[str] = None,
                  format: Optional[str] = "basic_info",
                  slow: Optional[bool] = False) -> List[AvailabilityResult]:
    """
    Retrieve information about the number of existing data product records

    Args:
        start: start date to retrieve availability info from (inclusive)
        end: end date to retrieve availability info to (inclusive)
        program: program string name to filter sources by, defaults to None
        platform: platform string name to filter sources by, defaults to None
        instrument_type: instrument type string to filter sources by, defaults to None
        source_type: source type string to filter sources by, defaults to None
        owner: owner email address string to filter sources by, defaults to None
        format: the format of the data sources returned (identifier_only, basic_info,
            full_record, with_metadata), defaults to "basic_info"
        slow: query the data directly (slower) for more up-to-date results, defaults
            to false

    Returns:
        a list of pyaurorax.availability.AvailabilityResult objects
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
    req = pyaurorax.AuroraXRequest(method="get",
                                   url=pyaurorax.api.urls.data_products_availability_url,
                                   params=params)
    res = req.execute()

    # return
    return [AvailabilityResult(**av) for av in res.data]
