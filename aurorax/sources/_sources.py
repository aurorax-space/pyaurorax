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
    req = aurorax.AuroraXRequest(method="get", url=aurorax.api.urls.data_sources_url)
    res = req.execute()

    # order results
    res.data = sorted(res.data, key=lambda x: x[order])

    # return
    return res.data


def get(program: str,
        platform: str,
        instrument_type: str,
        format: Optional[str] = "basic_info") -> Dict:
    """
    Retrieve a specific data source record

    :param program: program
    :type program: str
    :param platform: program
    :type platform: str
    :param instrument_type: program
    :type instrument_type: str
    :param format: record format, defaults to "basic_info"
    :type format: Optional[str], optional

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected error

    :return: data source
    :rtype: Dict
    """
    # make request
    params = {
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "format": format,
    }
    req = aurorax.AuroraXRequest(method="get", url=aurorax.api.urls.data_sources_url, params=params)
    res = req.execute()

    # set results to the first thing
    if (len(res.data) == 1):
        res.data = res.data[0]
    else:
        res.data = {}

    # return
    return res.data


def get_using_filters(program: Optional[str] = None,
                      platform: Optional[str] = None,
                      instrument_type: Optional[str] = None,
                      source_type: Optional[str] = None,
                      owner: Optional[str] = None,
                      format: Optional[str] = "basic_info",
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
    req = aurorax.AuroraXRequest(method="get", url=aurorax.api.urls.data_sources_url, params=params)
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
    url = "%s/%d" % (aurorax.api.urls.data_sources_url, identifier)
    req = aurorax.AuroraXRequest(method="get", url=url, params=params)
    res = req.execute()

    # return
    return res.data


def get_stats(identifier: int,
              format: Optional[str] = "basic_info",
              slow: Optional[bool] = False) -> Dict:
    """
    Retrieve statistics for a data source

    :param identifier: data source identifier
    :type identifier: int
    :param format: record format, defaults to "basic_info"
    :type format: Optional[str], optional
    :param slow: use slow method which gets most up-to-date stats info, defaults to "False"
    :type slow: Optional[bool], optional

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected error

    :return: stats info
    :rtype: Dict
    """
    # make request
    params = {
        "format": format,
        "slow": slow,
    }
    url = "%s/%d/stats" % (aurorax.api.urls.data_sources_url, identifier)
    req = aurorax.AuroraXRequest(method="get", url=url, params=params)
    res = req.execute()

    # return
    return res.data


def add(program: str,
        platform: str,
        instrument_type: str,
        source_type: str,
        display_name: str,
        ephemeris_metadata_schema: List[Dict] = [],
        data_product_metadata_schema: List[Dict] = [],
        maintainers: List = [],
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
    :param data_product_metadata_schema: metadata schema, defaults to []
    :type data_product_metadata_schema: List[Dict], optional
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
        "data_product_metadata_schema": data_product_metadata_schema,
        "maintainers": maintainers,
    }
    if (identifier is not None):
        request_data["identifier"] = identifier
    req = aurorax.AuroraXRequest(method="post", url=aurorax.api.urls.data_sources_url, body=request_data)
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
    url = "%s/%d" % (aurorax.api.urls.data_sources_url, identifier)
    req = aurorax.AuroraXRequest(method="delete", url=url, null_response=True)
    res = req.execute()

    # evaluate response
    if (res.status_code == 404):
        raise aurorax.AuroraXNotFoundException("%s - %s" % (res.data["error_code"], res.data["error_message"]))
    elif (res.status_code == 409):
        raise aurorax.AuroraXConflictException("%s - %s" % (res.data["error_code"], res.data["error_message"]))

    # return
    return res.data


def update(identifier: int,
           program: Optional[str] = None,
           platform: Optional[str] = None,
           instrument_type: Optional[str] = None,
           source_type: Optional[str] = None,
           display_name: Optional[str] = None,
           ephemeris_metadata_schema: Optional[List[Dict]] = None,
           data_product_metadata_schema: Optional[List[Dict]] = None,
           metadata: Optional[Dict] = None) -> Dict:
    """
    Update a data source in AuroraX

    :param identifier: data source identifier
    :type identifier: int
    :param program: new program name, defaults to None
    :type program: Optional[str], optional
    :param platform: new platform name, defaults to None
    :type platform: Optional[str], optional
    :param instrument_type: new instrument type, defaults to None
    :type instrument_type: Optional[str], optional
    :param source_type: new source type (heo, leo, lunar, ground), defaults to None
    :type source_type: Optional[str], optional
    :param display_name: new user-friendly display name, defaults to None
    :type display_name: Optional[str], optional
    :param ephemeris_metadata_schema: new metadata schema, defaults to []
    :type ephemeris_metadata_schema: List[Dict], optional
    :param data_product_metadata_schema: new metadata schema, defaults to []
    :type data_product_metadata_schema: List[Dict], optional
    :param metadata: new metadata, defaults to None
    :type metadata: Optional[Dict], optional

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected error
    :raises aurorax.AuroraXNotFoundException: data source not found

    :return: updated data source
    :rtype: Dict
    """
    # get the data source first
    ds = get_using_identifier(identifier)
    if (ds == {}):
        raise aurorax.AuroraXNotFoundException("data source not found")

    # set URL
    url = "%s/%d" % (aurorax.api.urls.data_sources_url, identifier)

    # replace data source values with ones passed into this function
    if (program is not None):
        ds["program"] = program
    if (platform is not None):
        ds["platform"] = platform
    if (instrument_type is not None):
        ds["instrument_type"] = instrument_type
    if (source_type is not None):
        ds["source_type"] = source_type
    if (display_name is not None):
        ds["display_name"] = display_name
    if (ephemeris_metadata_schema is not None):
        ds["ephemeris_metadata_schema"] = ephemeris_metadata_schema
    if (data_product_metadata_schema is not None):
        ds["data_product_metadata_schema"] = data_product_metadata_schema
    if (metadata is not None):
        ds["metadata"] = metadata

    # make request
    req = aurorax.AuroraXRequest(method="put", url=url, body=ds)
    res = req.execute()

    # return
    return res.data
