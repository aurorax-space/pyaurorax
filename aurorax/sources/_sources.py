import aurorax
from typing import List, Dict, Optional


def list(order: Optional[str] = "identifier") -> List:
    """
    Retrieve all data source records

    :param order: value to order results by (identifier, program, platform,
                  instrument_type, display_name, owner), defaults to "identifier"
    :type format: Optional[str], optional

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected error

    :return: all data sources
    :rtype: List
    """
    # make request
    req = aurorax.AuroraXRequest(method="get", url=aurorax.api.URL_DATA_SOURCES)
    res = req.execute()

    # order results
    res.data = sorted(res.data, key=lambda x: x[order])

    # return
    return res.data


def get_using_filters(program: Optional[str] = None, platform: Optional[str] = None,
                      instrument_type: Optional[str] = None, source_type: Optional[str] = None,
                      owner: Optional[str] = None, format: Optional[str] = "basic_info",
                      order: Optional[str] = "identifier",) -> List:
    """
    Retrieve all data source records matching a filter

    :param program: program, defaults to None
    :type program: Optional[str], optional
    :param platform: program, defaults to None
    :type platform: Optional[str], optional
    :param instrument_type: program, defaults to None
    :type instrument_type: Optional[str], optional
    :param source_type: program, defaults to None
    :type source_type: Optional[str], optional
    :param owner: program, defaults to None
    :type owner: Optional[str], optional
    :param format: record format, defaults to "basic_info"
    :type format: Optional[str], optional
    :param order: value to order results by (identifier, program, platform,
                  instrument_type, display_name, owner), defaults to "identifier"
    :type order: Optional[str], optional

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected error

    :return: matching data sources
    :rtype: List
    """
    # make request
    params = {
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "source_type": source_type,
        "owner": owner,
        "format": format,
    }
    req = aurorax.AuroraXRequest(method="get", url=aurorax.api.URL_DATA_SOURCES, params=params)
    res = req.execute()

    # order results
    res.data = sorted(res.data, key=lambda x: x[order])

    # return
    return res.data


def get_using_identifier(identifier: int, format: Optional[str] = "basic_info") -> Dict:
    """
    Retrieve all data source records matching a filter

    :param identifier: data source identifier
    :type identifier: int
    :param format: record format, defaults to "basic_info"
    :type format: Optional[str], optional

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected error

    :return: matching data sources
    :rtype: List
    """
    # make request
    params = {
        "format": format,
    }
    url = "%s/%d" % (aurorax.api.URL_DATA_SOURCES, identifier)
    req = aurorax.AuroraXRequest(method="get", url=url, params=params)
    res = req.execute()

    # return
    return res.data


def get_stats(identifier: int, format: Optional[str] = "basic_info") -> Dict:
    """
    Retrieve statistics for a data source

    :param identifier: data source identifier
    :type identifier: int
    :param format: record format, defaults to "basic_info"
    :type format: Optional[str], optional

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected error

    :return: stats info
    :rtype: Dict
    """
    # make request
    params = {
        "format": format,
    }
    url = "%s/%d/stats" % (aurorax.api.URL_DATA_SOURCES, identifier)
    req = aurorax.AuroraXRequest(method="get", url=url, params=params)
    res = req.execute()

    # return
    return res.data


def add(program: str, platform: str, instrument_type: str, source_type: str,
        display_name: str, ephemeris_metadata_schema: List[Dict] = [],
        data_products_metadata_schema: List[Dict] = [], maintainers: List = [],
        identifier: int = None) -> Dict:
    """
    Add new data source to AuroraX

    :param program: program name
    :type program: str
    :param platform: platform name
    :type platform: str
    :param instrument_type: instrument type
    :type instrument_type: str
    :param source_type: source type (heo, leo, lunar, ground)
    :type source_type: str
    :param display_name: a more user-friendly display name
    :type display_name: str
    :param ephemeris_metadata_schema: metadata schema, defaults to []
    :type ephemeris_metadata_schema: List[Dict], optional
    :param data_products_metadata_schema: metadata schema, defaults to []
    :type data_products_metadata_schema: List[Dict], optional
    :param maintainers: list of users to give maintainer permissions to, defaults to []
    :type maintainers: List, optional
    :param identifier: data source ID, defaults to None
    :type identifier: int, optional
    :return: the created data source record details
    :rtype: Dict

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected error
    :raises aurorax.AuroraXDuplicateException: duplicate data source, already exists

    :return: created data source
    :rtype: Dict
    """
    # do request
    request_data = {
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "source_type": source_type,
        "display_name": display_name,
        "ephemeris_metadata_schema": ephemeris_metadata_schema,
        "data_product_metadata_schema": data_products_metadata_schema,
        "maintainers": maintainers,
    }
    if (identifier is not None):
        request_data["identifier"] = identifier
    req = aurorax.AuroraXRequest(method="post", url=aurorax.api.URL_DATA_SOURCES, body=request_data)
    res = req.execute()

    # evaluate response
    if (res.status_code == 409):
        raise aurorax.AuroraXDuplicateException("%s - %s" % (res.data["error_code"], res.data["error_message"]))

    # return
    return res.data


def delete(identifier: int) -> int:
    """
    Delete a data source

    :param identifier: data source identifier
    :type identifier: int

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected error
    :raises aurorax.AuroraXNotFoundException: data source not found
    :raises aurorax.AuroraXConflictException: conflict of some type

    :return: 0 on success
    :rtype: int
    """
    # do request
    url = "%s/%d" % (aurorax.api.URL_DATA_SOURCES, identifier)
    req = aurorax.AuroraXRequest(method="delete", url=url, null_response=True)
    res = req.execute()

    # evaluate response
    if (res.status_code == 404):
        raise aurorax.AuroraXNotFoundException("%s - %s" % (res.data["error_code"], res.data["error_message"]))
    elif (res.status_code == 409):
        raise aurorax.AuroraXConflictException("%s - %s" % (res.data["error_code"], res.data["error_message"]))

    # return
    return res.data
