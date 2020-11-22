import aurorax as _aurorax
from typing import List as _List
from typing import Dict as _Dict


def list(format: str = "basic_info") -> _Dict:
    """
    Retrieves all data source records

    :param format: the format of the data source returned (identifier_only, basic_info,
                   full_record), defaults to "basic_info"
    :type format: str, optional

    :return: information about all data sources
    :rtype: Dict
    """
    # make request
    url = _aurorax.api.URL_DATA_SOURCES
    params = {
        "format": format,
    }
    req = _aurorax.AuroraXRequest(url, params=params)
    res = req.execute()

    # set dict to return
    return_dict = {
        "status_code": res.status_code,
        "data": [],
    }
    if (res.status_code == 200):
        return_dict["data"] = res.data

    # return
    return return_dict


def get_using_identifier(identifier: int, format: str = "basic_info") -> _Dict:
    """
    Retrieves data source record matching identifier

    :param identifier: data source unique identifier
    :type identifier: int
    :param format: the format of the data source returned (identifier_only, basic_info,
                   full_record), defaults to "basic_info"
    :type format: str, optional


    :return: information the specific data source
    :rtype: Dict
    """
    # make request
    url = "%s/%d" % (_aurorax.api.URL_DATA_SOURCES, identifier)
    params = {
        "format": format
    }
    req = _aurorax.AuroraXRequest(url, params=params)
    res = req.execute()

    # set dict to return
    return_dict = {
        "status_code": res.status_code,
        "data": {},
    }
    if (res.status_code == 200):
        return_dict["data"] = res.data

    # return
    return return_dict


def get_using_filters(program: str = None, platform: str = None, instrument_type: str = None, source_type: str = None,
                      owner: str = None, format: str = "basic_info") -> _Dict:
    """
    Retrieves all data source records matching the specified filters

    :param program: program name, defaults to None
    :type program: str, optional
    :param platform: platform name, defaults to None
    :type platform: str, optional
    :param instrument_type: instrument type, defaults to None
    :type instrument_type: str, optional
    :param source_type: source type (leo, heo, lunar, ground), defaults to None
    :type source_type: str, optional
    :param owner: owner account name, defaults to None
    :type owner: str, optional
    :param format: the format of the data source returned (identifier_only, basic_info,
                   full_record), defaults to "basic_info"
    :type format: str, optional

    :return: information about the specific data sources matching the filter criteria
    :rtype: Dict
    """
    # make request
    url = "%s" % (_aurorax.api.URL_DATA_SOURCES)
    params = {
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "source_type": source_type,
        "owner": owner,
        "format": format,
    }
    req = _aurorax.AuroraXRequest(url, params=params)
    res = req.execute()

    # set dict to return
    return_dict = {
        "status_code": res.status_code,
        "data": [],
    }
    if (res.status_code == 200):
        return_dict["data"] = res.data

    # return
    return return_dict


def get_stats(identifier: int) -> _Dict:
    """
    Retrieves additional statistics about the specified data source such as
    the earliest/latest data record and the total number of data records
    available

    :param identifier: data source identifier
    :type identifier: int

    :return: the data source statistics
    :rtype: Dict
    """
    # make request
    url = "%s/%d/stats" % (_aurorax.api.URL_DATA_SOURCES, identifier)
    req = _aurorax.AuroraXRequest(url)
    res = req.execute()

    # set dict to return
    return_dict = {
        "status_code": res.status_code,
        "data": {},
    }
    if (res.status_code == 200):
        return_dict["data"] = res.data

    # return
    return return_dict


def add(api_key: str, program: str, platform: str, instrument_type: str, source_type: str,
        display_name: str, ephemeris_metadata_schema: _List[_Dict] = [],
        data_products_metadata_schema: _List[_Dict] = [], maintainers: _List = [],
        identifier: int = None) -> _Dict:
    """
    Create a new data source record

    :param api_key: API key associated with your account
    :type api_key: str
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
    """
    # make request
    url = _aurorax.api.URL_DATA_SOURCES
    post_data = {
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
        post_data["identifier"] = identifier
    req = _aurorax.AuroraXRequest(url, method="POST", api_key=api_key, json=post_data)
    res = req.execute()

    # set dict to return
    return_dict = {
        "status_code": res.status_code,
        "data": {},
    }
    if (res.status_code == 200 or res.status_code == 409):
        return_dict["data"] = res.request.json()

    # return
    return return_dict


def delete(api_key: str, identifier: int) -> _Dict:
    """
    Remove a data source record

    :param api_key: API key associated with your account
    :type api_key: str
    :param identifier: unique data source identifier
    :type identifier: int

    :return: status summary
    :rtype: Dict
    """
    # make request
    url = "%s/%s" % (_aurorax.api.URL_DATA_SOURCES, str(identifier))
    req = _aurorax.AuroraXRequest(url, method="DELETE", api_key=api_key)
    res = req.execute()

    # set dict to return
    return_dict = {
        "status_code": res.status_code,
        "data": {},
    }
    if (res.status_code == 409):
        return_dict["data"] = res.request.json()

    # return
    return return_dict


def update(api_key: str, identifier: int, program: str = None, platform: str = None,
           instrument_type: str = None, source_type: str = None, ephemeris_metadata_schema: _List[_Dict] = [],
           data_products_metadata_schema: _List[_Dict] = [], owner: str = None,
           maintainers: _List = None) -> _Dict:
    """
    Update a data source record

    :param api_key: API key associated with your account
    :type api_key: str
    :param program: program name
    :type program: str
    :param platform: platform name
    :type platform: str
    :param instrument_type: instrument type
    :type instrument_type: str
    :param source_type: source type (heo, leo, lunar, ground)
    :type source_type: str
    :param ephemeris_metadata_schema: metadata schema, defaults to []
    :type ephemeris_metadata_schema: List[Dict], optional
    :param data_products_metadata_schema: metadata schema, defaults to []
    :type data_products_metadata_schema: List[Dict], optional
    :param maintainers: list of users to give maintainer permissions to, defaults to None
    :type maintainers: List, optional

    :return: the new data source record details
    :rtype: Dict
    """
    # set new information based on current values and function parameters
    # post_data = {}
    # if (program is not None):
    #     post_data["program"] = program
    # if (platform is not None):
    #     post_data["platform"] = platform
    # if (instrument_type is not None):
    #     post_data["instrument_type"] = instrument_type
    # if (source_type is not None):
    #     post_data["source_type"] = source_type
    # if (ephemeris_metadata_schema is not None):
    #     post_data["ephemeris_metadata_schema"] = ephemeris_metadata_schema
    # if (data_products_metadata_schema is not None):
    #     post_data["data_products_metadata_schema"] = data_products_metadata_schema
    # if (owner is not None):
    #     post_data["owner"] = owner
    # if (maintainers is not None):
    #     post_data["maintainers"] = maintainers

    # # make request
    # url = "%s/%s" % (URL_DATA_SOURCES, str(identifier))
    # print(url)
    # req = AuroraXRequest(url, method="PUT", api_key=api_key, json=post_data)
    # res = req.execute()
    # if (res.status_code != 200 and res.status_code != 409):
    #     res.data = ""
    # elif (res.status_code == 409):
    #     res.data = res.request.json()
    # return res
    pass
