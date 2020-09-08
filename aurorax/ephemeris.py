from .api import URL_EPHEMERIS_SOURCES
from .api import AuroraXRequest
from typing import List, Dict


def get_all_sources(program: str = None, platform: str = None, instrument_type: str = None, source_type: str = None,
                    owner: str = None, format: str = "basic_info") -> List[Dict]:
    """
    Retrieves all ephemeris source records

    :param program: program name to filter sources by, optional
    :param platform: platform name to filter sources by, optional
    :param instrument_type: instrument type to filter sources by, optional
    :param source_type: source type to filter sources by (e.g. "heo"), optional
    :param owner: owner ID to filter sources by, optional
    :param format: the format of the ephemeris source returned Available values: "identifier_only", \
                   "basic_info", "full_record". Default is "basic_info"

    :return: a list of dictionaries with information about all ephemeris sources
    """
    url = URL_EPHEMERIS_SOURCES
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
    if (res.status_code != 200):
        return []
    else:
        return res.data


def get_source(identifier: int, format: str = "basic_info") -> Dict:
    """
    Retrieves a single specific ephemeris source record

    :param identifier: ephemeris source identifier
    :param format: the format of the ephemeris source returned Available values: "identifier_only",
                   "basic_info", "full_record". Default is "basic_info"

    :return: a dictionary with the ephemeris source information
    """
    url = "%s/%d" % (URL_EPHEMERIS_SOURCES, identifier)
    params = {"format": format}
    req = AuroraXRequest(url, params=params)
    res = req.execute()
    if (res.status_code != 200):
        return {}
    else:
        return res.data


def get_source_statistics(identifier: int) -> Dict:
    """
    Retrieves additional statistics about the specified ephemeris source such as
    the earliest/latest ephemeris record and the total number of ephemeris records
    available

    :param identifier: ephemeris source identifier

    :return: a dictionary with the ephemeris source statistics
    """
    url = "%s/%d/stats" % (URL_EPHEMERIS_SOURCES, identifier)
    req = AuroraXRequest(url)
    res = req.execute()
    if (res.status_code != 200):
        return {}
    else:
        return res.data


def add_source(api_key, program, platform, instrument_type, source_type, metadata_schema={}, maintainers=[]):
    pass


def remove_source(api_key, program, platform, instrument_type, source_type, metadata_schema={}, maintainers=[]):
    pass


def update_source(api_key, program, platform, instrument_type, source_type, metadata_schema={}, maintainers=[]):
    pass


def search(start_dt, end_dt, programs=[], platforms=[], instrument_types=[], metadata_filters=[]):
    pass


def upload():
    pass
