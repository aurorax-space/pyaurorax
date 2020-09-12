from typing import List, Dict
from .api import URL_EPHEMERIS_SOURCES
from .api import AuroraXRequest, AuroraXResponse


def get_all_sources(format: str = "basic_info") -> List[Dict]:
    """
    Retrieves all ephemeris source records

    :param format: the format of the ephemeris source returned Available values: "identifier_only", \
                   "basic_info", "full_record". Default is "basic_info"

    :return: dictionary containing information about all ephemeris sources
    """
    url = URL_EPHEMERIS_SOURCES
    params = {
        "format": format,
    }
    req = AuroraXRequest(url, params=params)
    res = req.execute()
    if (res.status_code == 200):
        return res.data
    else:
        return []


def get_source_using_identifier(identifier: str, format: str = "basic_info") -> Dict:
    """
    Retrieves ephemeris source record matching identifier

    :param identifier: ephemeris source unique identifier
    :param format: the format of the ephemeris source returned (identifier_only, basic_info, \
                   full_record. Default is basic_info

    :return: dictionary containing information about all ephemeris sources
    """
    url = "%s/%s" % (URL_EPHEMERIS_SOURCES, str(identifier))
    params = {
        "format": format
    }
    req = AuroraXRequest(url, params=params)
    res = req.execute()
    if (res.status_code == 200):
        return res.data
    else:
        return {}


def get_source_using_filters(program: str = None, platform: str = None, instrument_type: str = None,
                             source_type: str = None, owner: str = None, format: str = "basic_info") -> List[Dict]:
    """
    Retrieves all ephemeris source records matching the specified filters

    :param program: program name
    :param platform: platform name
    :param instrument_type: instrument type
    :param source_type: source type (leo, heo, lunar, or ground)
    :param owner: owner account name
    :param format: the format of the ephemeris source returned (identifier_only, basic_info, \
                   full_record. Default is basic_info

    :return: dictionary containing information about all ephemeris sources
    """
    url = "%s" % (URL_EPHEMERIS_SOURCES)
    params = {
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "source_type": source_type,
        "owner": owner,
        "format": format,
    }
    req = AuroraXRequest(url, params=params)
    res = req.execute()
    if (res.status_code == 200):
        return res.data
    else:
        return []


def get_source_statistics(identifier: str) -> Dict:
    """
    Retrieves additional statistics about the specified ephemeris source such as
    the earliest/latest ephemeris record and the total number of ephemeris records
    available

    :param identifier: ephemeris source identifier

    :return: an AuroraXResponse object with the ephemeris source statistics
    """
    url = "%s/%s/stats" % (URL_EPHEMERIS_SOURCES, str(identifier))
    req = AuroraXRequest(url)
    res = req.execute()
    if (res.status_code == 200):
        return res.data
    else:
        return {}


def add_source(api_key: str, program: str, platform: str, instrument_type: str, source_type: str,
               metadata_schema: List = [], maintainers: List = []) -> AuroraXResponse:
    """
    Create a new ephemeris source record

    :param api_key: API key associated with your account
    :param program: program name
    :param platform: platform name
    :param instrument_type: instrument type
    :param source_type: source type (heo, leo, lunar, ground)
    :param metadata_schema: metadata schema
    :param maintainers: list of users to give maintainer permissions to

    :return: an AuroraXResponse object with the returned ephemeris source record details
    """
    url = URL_EPHEMERIS_SOURCES
    post_data = {
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "source_type": source_type,
        "metadata_schema": metadata_schema,
        "maintainers": maintainers,
    }
    req = AuroraXRequest(url, method="POST", api_key=api_key, json=post_data)
    res = req.execute()
    if (res.status_code != 200 and res.status_code != 409):
        res.data = []
    elif (res.status_code == 409):
        res.data = res.request.json()
    return res


def remove_source(api_key: str, identifier: str) -> AuroraXResponse:
    """
    Remove an ephemeris source record

    :param api_key: API key associated with your account
    :param identifier: unique ephemeris source identifier

    :return: an AuroraXResponse object
    """
    url = "%s/%s" % (URL_EPHEMERIS_SOURCES, str(identifier))
    req = AuroraXRequest(url, method="DELETE", api_key=api_key)
    res = req.execute()
    if (res.status_code != 200 and res.status_code != 409):
        res.data = ""
    elif (res.status_code == 409):
        res.data = res.request.json()
    return res


def update_source(api_key, program, platform, instrument_type, source_type, metadata_schema={}, maintainers=[]):
    pass


def search(start_dt, end_dt, programs=[], platforms=[], instrument_types=[], metadata_filters=[]):
    pass


def upload():
    pass
