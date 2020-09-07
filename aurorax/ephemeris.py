import requests

__URL_EPHEMERIS_SOURCES = "http://api.staging.aurorax.space/api/v1/ephemeris-sources"


def list_sources(program=None, platform=None, instrument_type=None, source_type=None, owner=None, format="basic_info"):
    """
    Returns a list of dictionaries representing all ephemeris sources.

    :param program: program name to filter sources by, optional
    :param platform: platform name to filter sources by, optional
    :param instrument_type: instrument type to filter sources by, optional
    :param source_type: source type to filter sources by (e.g. "heo"), optional
    :param owner: owner ID to filter sources by, optional
    :param format: the format of the ephemeris source returned Available values: "identifier_only", "basic_info",
                   "full_record". Default is "basic_info"

    :return: a dictionary of all ephemeris sources
    """
    filters = {
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "source_type": source_type,
        "owner": owner,
        "format": format
    }
    r = requests.get(__URL_EPHEMERIS_SOURCES, params=filters)
    if (r.status_code == 200):
        return r.json()
    else:
        return {}


def add_source(api_key, program, platform, instrument_type, source_type, metadata_schema={}, maintainers=[]):
    pass
