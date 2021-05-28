import aurorax
import pprint
from pydantic import BaseModel
from typing import List, Dict

class DataSource(BaseModel):
    """
    Data source data type

    :param identifier: data source ID, defaults to None
    :type identifier: int
    :param program: data source program name, defaults to None
    :type program: str
    :param platform: data source platform name, defaults to None
    :type platform: str
    :param instrument_type: data source instrument type, defaults to None
    :type instrument_type: str
    :param source_type: data source type, defaults to None
    :type source_type: str
    :param display_name: data source display name, defaults to None
    :type display_name: str
    :param metadata: data source metadata, defaults to None
    :type metadata: str
    :param owner: data source owner's email address, defaults to None
    :type owner: str
    :param maintainers: list of maintainer email addresses, defaults to []
    :type maintainers: List[str]
    :param ephemeris_metadata_schema: data source ephemeris metadata schema, defaults to []
    :type ephemeris_metadata_schema: List[Dict]
    :param data_product_metadata_schema: data source data product metadata schema, defaults to []
    :type data_product_metadata_schema: List[Dict]
    """
    identifier: int = None
    program: str = None
    platform: str = None
    instrument_type: str = None
    source_type: str = None
    display_name: str = None
    metadata: str = None
    owner: str = None
    maintainers: List[str] = []
    ephemeris_metadata_schema: List[Dict] = []
    data_product_metadata_schema: List[Dict] = []


    def __str__(self) -> str:
        """
        String method

        :return: string format
        :rtype: str
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation

        :return: object representation
        :rtype: str
        """
        return pprint.pformat(self.__dict__)

def list(order: str = "identifier", format: str = "basic_info") -> List[DataSource]:
    """
    Retrieve all data source records

    :param order: value to order results by (identifier, program, platform,
                  instrument_type, display_name, owner), defaults to "identifier"
    :type order: str, optional
    :param format: record format, defaults to "basic_info"
    :type format: str, optional

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected error

    :return: all data sources
    :rtype: List[aurorax.sources.DataSource]
    """
    params = {
        format: format
    }
    # make request
    req = aurorax.AuroraXRequest(method="get", url=aurorax.api.urls.data_sources_url, params=params if format else None)
    res = req.execute()

    # order results
    res.data = sorted(res.data, key=lambda x: x[order])

    # return
    return [DataSource(**source) for source in res.data]

def get(program: str,
        platform: str,
        instrument_type: str,
        format: str = "basic_info") -> DataSource:
    """
    Retrieve a specific data source record

    :param program: program
    :type program: str
    :param platform: program
    :type platform: str
    :param instrument_type: program
    :type instrument_type: str
    :param format: record format, defaults to "basic_info"
    :type format: str, optional

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected error
    :raises aurorax.AuroraXNotFoundException: source not found

    :return: data source
    :rtype: aurorax.sources.DataSource
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

        # if format == "identifier_only":
        #     return res.data["identifier"]

        return DataSource(**res.data)
    else:
        raise aurorax.AuroraXNotFoundException("data source not found")


def get_using_filters(program: str = None,
                      platform: str = None,
                      instrument_type: str = None,
                      source_type: str = None,
                      owner: str = None,
                      format: str = "basic_info",
                      order: str = "identifier",) -> List[DataSource]:
    """
    Retrieve all data source records matching a filter

    :param program: program, defaults to None
    :type program: str, optional
    :param platform: program, defaults to None
    :type platform: str, optional
    :param instrument_type: program, defaults to None
    :type instrument_type: str, optional
    :param source_type: program, defaults to None
    :type source_type: str, optional
    :param owner: program, defaults to None
    :type owner: str, optional
    :param format: record format, defaults to "basic_info"
    :type format: str, optional
    :param order: value to order results by (identifier, program, platform,
                  instrument_type, display_name, owner), defaults to "identifier"
    :type order: str, optional

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected error

    :return: matching data sources
    :rtype: List[aurorax.sources.DataSource]
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
    try:
        return [DataSource(**ds) for ds in res.data]
    except:
        return []


def get_using_identifier(identifier: int, format: str = "basic_info") -> DataSource:
    """
    Retrieve data source records matching an identifier

    :param identifier: data source identifier
    :type identifier: int
    :param format: record format, defaults to "basic_info"
    :type format: str, optional

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected error

    :return: matching data source
    :rtype: aurorax.sources.DataSource
    """
    # make request
    params = {
        "format": format,
    }
    url = "%s/%d" % (aurorax.api.urls.data_sources_url, identifier)
    req = aurorax.AuroraXRequest(method="get", url=url, params=params)
    res = req.execute()

    # return
    try:
        return DataSource(**res.data)
    except:
        raise aurorax.AuroraXNotFoundException("Data source not found. Check that the identifier is correct.")


def get_stats(identifier: int,
              format: str = "basic_info",
              slow: bool = False) -> Dict:
    """
    Retrieve statistics for a data source

    :param identifier: data source identifier
    :type identifier: int
    :param format: record format, defaults to "basic_info"
    :type format: str, optional
    :param slow: use slow method which gets most up-to-date stats info, defaults to "False"
    :type slow: bool, optional

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


def add(data_source: DataSource) -> DataSource:
    """
    Add new data source to AuroraX

    :param data_source: DataSource object to add
    :type data_source: aurorax.sources.DataSource

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected error
    :raises aurorax.AuroraXDuplicateException: duplicate data source, already exists

    :return: created data source
    :rtype: aurorax.sources.DataSource
    """

    # do request
    # TODO: Check again after fix for null schema values
    request_data = {
        "program": data_source.program,
        "platform": data_source.platform,
        "instrument_type": data_source.instrument_type,
        "source_type": data_source.source_type,
        "display_name": data_source.display_name,
        "ephemeris_metadata_schema": data_source.ephemeris_metadata_schema,
        "data_product_metadata_schema": data_source.data_product_metadata_schema,
        "maintainers": data_source.maintainers,
    }

    if (data_source.identifier is not None):
        request_data["identifier"] = data_source.identifier

    req = aurorax.AuroraXRequest(method="post", url=aurorax.api.urls.data_sources_url, body=request_data)
    res = req.execute()

    # evaluate response
    if (res.status_code == 409):
        raise aurorax.AuroraXDuplicateException("%s - %s" % (res.data["error_code"], res.data["error_message"]))

    # return
    try:
        return DataSource(**res.data)
    except:
        raise aurorax.AuroraXException("Could not create data source.")


def delete(identifier: int) -> int:
    """
    Delete a data source

    :param identifier: data source identifier
    :type identifier: int

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected error
    :raises aurorax.AuroraXNotFoundException: data source not found
    :raises aurorax.AuroraXConflictException: conflict of some type

    :return: 1 on success
    :rtype: int
    """
    # do request
    url = "%s/%d" % (aurorax.api.urls.data_sources_url, identifier)
    req = aurorax.AuroraXRequest(method="delete", url=url, null_response=True)
    res = req.execute()

    # evaluate response
    if (res.status_code == 400):
        raise aurorax.AuroraXBadParametersException("%s - %s" % (res.data["error_code"], res.data["error_message"]))
    elif (res.status_code == 404):
        raise aurorax.AuroraXNotFoundException("%s - %s" % (res.data["error_code"], res.data["error_message"]))
    elif (res.status_code == 409):
        raise aurorax.AuroraXConflictException("%s - %s" % (res.data["error_code"], res.data["error_message"]))

    # return
    return 1


def update(data_source: DataSource) -> DataSource:
    """
    Update a data source in AuroraX. This operation will fully replace the data source with the data_source argument passed in.
    Please make sure data_source is complete. Refer to examples for usage.

    :param data_source: full record of data source to be updated
    :type data_source: aurorax.sources.DataSource

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected error
    :raises aurorax.AuroraXNotFoundException: data source not found
    :raises aurorax. AuroraXBadParametersException: missing parameters

    :return: updated data source
    :rtype: aurorax.sources.DataSource
    """
    # TODO: Check for not-None schema fields too?
    if not all([data_source.identifier, data_source.program, data_source.platform, data_source.instrument_type, data_source.source_type, data_source.display_name]):
        raise aurorax.AuroraXBadParametersException("One or more required data source fields are missing. Update operation aborted.")

    # set URL
    url = f"{aurorax.api.urls.data_sources_url}/{data_source.identifier}"

    # make request to update the data source passed in
    req = aurorax.AuroraXRequest(method="put", url=url, body=data_source)
    req.execute()

    # return
    try:
        return aurorax.sources.get(data_source.program, data_source.platform, data_source.instrument_type, "full_record")
    except:
        raise aurorax.AuroraXException("Could not update data source.")
