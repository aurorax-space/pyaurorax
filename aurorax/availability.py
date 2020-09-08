from .api import URL_EPHEMERIS_AVAILABILITY, URL_DATA_PRODUCTS_AVAILABILITY
from .api import AuroraXRequest
import datetime


def get_ephemeris(start_dt: datetime, end_dt: datetime, program: str = None, platform: str = None,
                  instrument_type: str = None, source_type: str = None, owner: str = None,
                  format: str = "basic_info") -> AuroraXRequest:
    """
    Returns a list of dictionaries representing information about the number of existing
    ephemeris records

    :param start_dt: start date
    :param end_dt: end date
    :param program: program name to filter sources by, optional
    :param platform: platform name to filter sources by, optional
    :param instrument_type: instrument type to filter sources by, optional
    :param source_type: source type to filter sources by (e.g. "heo"), optional
    :param owner: owner ID to filter sources by, optional
    :param format: the format of the ephemeris source returned Available values: "identifier_only",
                   "basic_info", "full_record". Default is "basic_info"

    :return: a dictionary of ephemeris availability information
    """
    params = {
        "start": start_dt.strftime("%Y-%m-%d"),
        "end": end_dt.strftime("%Y-%m-%d"),
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "source_type": source_type,
        "owner": owner,
        "format": format,
    }
    req = AuroraXRequest(URL_EPHEMERIS_AVAILABILITY, params=params)
    res = req.execute()
    return res


def get_data_products(start_dt: datetime, end_dt: datetime, program: str = None, platform: str = None,
                      instrument_type: str = None, source_type: str = None, owner: str = None,
                      format: str = "basic_info") -> AuroraXRequest:
    """
    Returns a list of dictionaries representing information about the number of existing
    data products records

    :param start_dt: start date
    :param end_dt: end date
    :param program: program name to filter sources by, optional
    :param platform: platform name to filter sources by, optional
    :param instrument_type: instrument type to filter sources by, optional
    :param source_type: source type to filter sources by (e.g. "heo"), optional
    :param owner: owner ID to filter sources by, optional
    :param format: the format of the ephemeris source returned available values: "identifier_only",
                   "basic_info", "full_record". Default is "basic_info"

    :return: a dictionary of ephemeris availability information
    """
    params = {
        "start": start_dt.strftime("%Y-%m-%d"),
        "end": end_dt.strftime("%Y-%m-%d"),
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "source_type": source_type,
        "owner": owner,
        "format": format,
    }
    req = AuroraXRequest(URL_DATA_PRODUCTS_AVAILABILITY, params=params)
    res = req.execute()
    return res
