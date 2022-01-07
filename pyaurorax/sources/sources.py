"""
Functions for interacting with data sources
"""

import pyaurorax
from typing import List, Dict, Optional
from .classes.data_source import DataSource
from .classes.data_source_stats import DataSourceStatistics
from ..sources import FORMAT_FULL_RECORD

# pdoc init
__pdoc__: Dict = {}


def list(order: Optional[str] = "identifier",
         format: Optional[str] = FORMAT_FULL_RECORD) -> List[DataSource]:
    """
    Retrieve all data sources

    Args:
        order: value to order results by (identifier, program, platform,
            instrument_type, display_name, owner), defaults to "identifier"
        format: the format of the data sources returned, defaults to "full_record".
            Other options are in the pyaurorax.sources module, or at the top level
            using the pyaurorax.FORMAT_* variables.

    Returns:
        all found data sources

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
    """
    params = {
        format: format
    }
    # make request
    req = pyaurorax.AuroraXRequest(method="get",
                                   url=pyaurorax.api.urls.data_sources_url,
                                   params=params if format else None)
    res = req.execute()

    # order results
    res.data = sorted(res.data, key=lambda x: x[order])

    # return
    return [DataSource(**source) for source in res.data]


def get(program: str,
        platform: str,
        instrument_type: str,
        format: Optional[str] = FORMAT_FULL_RECORD) -> DataSource:
    """
    Retrieve a specific data source record

    Args:
        program: the program name
        platform: the platform name
        instrument_type: the instrument type name
        format: the format of the data sources returned, defaults to "full_record".
            Other options are in the pyaurorax.sources module, or at the top level
            using the pyaurorax.FORMAT_* variables.

    Returns:
        the data source matching the requested parameters

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
        pyaurorax.exceptions.AuroraXNotFoundException: source not found
    """
    # make request
    params = {
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "format": format,
    }
    req = pyaurorax.AuroraXRequest(method="get",
                                   url=pyaurorax.api.urls.data_sources_url,
                                   params=params)
    res = req.execute()

    # set results to the first thing
    if (len(res.data) == 1):
        res.data = res.data[0]
        return DataSource(**res.data)
    else:
        raise pyaurorax.AuroraXNotFoundException("Data source not found")


def get_using_filters(program: Optional[str] = None,
                      platform: Optional[str] = None,
                      instrument_type: Optional[str] = None,
                      source_type: Optional[str] = None,
                      owner: Optional[str] = None,
                      format: Optional[str] = FORMAT_FULL_RECORD,
                      order: Optional[str] = "identifier") -> List[DataSource]:
    """
    Retrieve all data source records matching a filter

    Args:
        program: the program to filter for, defaults to None
        platform: the platform to filter for, defaults to None
        instrument_type: the instrument type to filter for, defaults to None
        source_type: the data source type to filter for, defaults to None.
            Options are in the pyaurorax.sources module, or at the top level
            using the pyaurorax.SOURCE_TYPE_* variables.
        owner: the owner's email address to filter for, defaults to None
        format: the format of the data sources returned, defaults to "full_record".
            Other options are in the pyaurorax.sources module, or at the top level
            using the pyaurorax.FORMAT_* variables.
        order: the value to order results by (identifier, program, platform,
            instrument_type, display_name, owner), defaults to "identifier"

    Returns:
        any data sources matching the requested parameters

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
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
    req = pyaurorax.AuroraXRequest(method="get",
                                   url=pyaurorax.api.urls.data_sources_url,
                                   params=params)
    res = req.execute()

    # order results
    res.data = sorted(res.data, key=lambda x: x[order])

    # return
    if len(res.data):
        return [DataSource(**ds) for ds in res.data]
    else:
        return []


def get_using_identifier(identifier: int,
                         format: Optional[str] = FORMAT_FULL_RECORD) -> DataSource:
    """
    Retrieve data source record matching an identifier

    Args:
        identifier: the AuroraX unique ID for the data source
        format: the format of the data sources returned, defaults to "full_record".
            Other options are in the pyaurorax.sources module, or at the top level
            using the pyaurorax.FORMAT_* variables.

    Returns:
        the data source matching the identifier

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
    """
    # make request
    params = {
        "format": format,
    }
    url = "%s/%d" % (pyaurorax.api.urls.data_sources_url, identifier)
    req = pyaurorax.AuroraXRequest(method="get", url=url, params=params)
    res = req.execute()

    # return
    return DataSource(**res.data)


def get_stats(identifier: int,
              format: Optional[str] = FORMAT_FULL_RECORD,
              slow: Optional[bool] = False) -> DataSourceStatistics:
    """
    Retrieve statistics for a data source

    Args:
        identifier: the AuroraX unique ID for the data source
        format: the format of the data sources returned, defaults to "full_record".
            Other options are in the pyaurorax.sources module, or at the top level
            using the pyaurorax.FORMAT_* variables.
        slow: retrieve the stats using a slower, but more accurate method, defaults to False

    Returns:
        information about the data source

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error
        pyaurorax.exceptions.AuroraXNotFoundException: data source not found
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
    """
    # make request
    params = {
        "format": format,
        "slow": slow,
    }
    url = "%s/%d/stats" % (pyaurorax.api.urls.data_sources_url, identifier)
    req = pyaurorax.AuroraXRequest(method="get", url=url, params=params)
    res = req.execute()

    # return
    return DataSourceStatistics(**res.data)


def add(data_source: DataSource) -> DataSource:
    """
    Add a new data source to AuroraX

    Args:
        data_source: the data source to add (note: it must be a fully-defined
            DataSource object)

    Returns:
        the newly created data source

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
        pyaurorax.exceptions.AuroraXDuplicateException: duplicate data source, already exists
    """
    # set up request
    request_data = {
        "program": data_source.program,
        "platform": data_source.platform,
        "instrument_type": data_source.instrument_type,
        "source_type": data_source.source_type,
        "display_name": data_source.display_name,
        "ephemeris_metadata_schema": data_source.ephemeris_metadata_schema,
        "data_product_metadata_schema": data_source.data_product_metadata_schema,
        "metadata": data_source.metadata
    }
    if (data_source.identifier is not None):
        request_data["identifier"] = data_source.identifier

    # make request
    req = pyaurorax.AuroraXRequest(method="post",
                                   url=pyaurorax.api.urls.data_sources_url,
                                   body=request_data)
    res = req.execute()

    # evaluate response
    if (res.status_code == 409):
        raise pyaurorax.AuroraXDuplicateException("%s - %s" % (res.data["error_code"],
                                                               res.data["error_message"]))

    # return
    try:
        return DataSource(**res.data)
    except Exception:
        raise pyaurorax.AuroraXException("Could not create data source")


def delete(identifier: int) -> int:
    """
    Delete a data source from AuroraX

    Args:
        identifier: the AuroraX unique ID for the data source

    Returns:
        1 on success

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
        pyaurorax.exceptions.AuroraXNotFoundException: data source not found
        pyaurorax.exceptions.AuroraXConflictException: conflict of some type
    """
    # do request
    url = "%s/%d" % (pyaurorax.api.urls.data_sources_url, identifier)
    req = pyaurorax.AuroraXRequest(method="delete",
                                   url=url,
                                   null_response=True)
    res = req.execute()

    # evaluate response
    if (res.status_code == 400):
        raise pyaurorax.AuroraXBadParametersException("%s - %s" % (res.data["error_code"],
                                                                   res.data["error_message"]))
    elif (res.status_code == 409):
        raise pyaurorax.AuroraXConflictException("%s - %s" % (res.data["error_code"],
                                                              res.data["error_message"]))

    # return
    return 1


def update(data_source: DataSource) -> DataSource:
    """
    Update a data source in AuroraX

    This operation will fully replace the data source with the
    data_source argument passed in. Be sure that the data_source
    object is complete.

    Args:
        data_source: the data source to update (note: it must be a fully-defined
            DataSource object with the values set to what you want AuroraX to
            update it to)

    Returns:
        the updated data source

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
        pyaurorax.exceptions.AuroraXNotFoundException: data source not found
        pyaurorax.exceptions.AuroraXBadParametersException: missing parameters
    """
    if not all([data_source.identifier, data_source.program, data_source.platform,
                data_source.instrument_type, data_source.source_type, data_source.display_name]):
        raise pyaurorax.AuroraXBadParametersException("One or more required data source fields "
                                                      "are missing, update operation aborted")

    # set URL
    url = f"{pyaurorax.api.urls.data_sources_url}/{data_source.identifier}"

    # make request to update the data source passed in
    req = pyaurorax.AuroraXRequest(method="put", url=url, body=data_source)
    req.execute()

    # return
    try:
        return pyaurorax.sources.get(data_source.program,
                                     data_source.platform,
                                     data_source.instrument_type,
                                     format=pyaurorax.FORMAT_FULL_RECORD)
    except Exception:
        raise pyaurorax.AuroraXException("Could not update data source")


def partial_update(identifier: int,
                   program: Optional[str] = None,
                   platform: Optional[str] = None,
                   instrument_type: Optional[str] = None,
                   source_type: Optional[str] = None,
                   display_name: Optional[str] = None,
                   metadata: Optional[Dict] = None,
                   owner: Optional[str] = None,
                   maintainers: Optional[List[str]] = None,
                   ephemeris_metadata_schema: Optional[List[Dict]] = None,
                   data_product_metadata_schema: Optional[List[Dict]] = None) -> DataSource:
    """
    Partially update a data source in AuroraX (omitted fields are ignored)

    Args:
        identifier: the AuroraX unique ID for the data source, defaults to None
        program: the new program for the data source, defaults to None
        platform: the new platform for the data source, defaults to None
        instrument_type: the new instrument type for the data source, defaults to None
        source_type: the new source type for the data source, defaults to None. Options
            are in the pyaurorax.sources module, or at the top level using the
            pyaurorax.SOURCE_TYPE_* variables.
        display_name: the new display name for the data source, defaults to None
        metadata: the new metadata for the data source, defaults to None
        maintainers: the new maintainer AuroraX account email addresses, defaults to None
        ephemeris_metadata_schema: a list of dictionaries capturing the metadata
            keys and values that can appear in ephemeris records associated with
            the data source, defaults to None
        data_product_metadata_schema: a list of dictionaries capturing the metadata
            keys and values that can appear in data product records associated with
            the data source, defaults to None

    Returns:
        the updated data source

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
        pyaurorax.exceptions.AuroraXNotFoundException: data source not found
        pyaurorax.exceptions.AuroraXBadParametersException: missing parameters
    """
    if not identifier:
        raise pyaurorax.AuroraXBadParametersException("Required identifier field is "
                                                      "missing, update operation aborted")

    # create a DataSource
    ds = DataSource(identifier=identifier,
                    program=program,
                    platform=platform,
                    instrument_type=instrument_type,
                    source_type=source_type,
                    display_name=display_name,
                    metadata=metadata,
                    owner=owner,
                    maintainers=maintainers,
                    ephemeris_metadata_schema=ephemeris_metadata_schema,
                    data_product_metadata_schema=data_product_metadata_schema)

    # set URL
    url = f"{pyaurorax.api.urls.data_sources_url}/{ds.identifier}"

    # make request to update the data source passed in
    req = pyaurorax.AuroraXRequest(method="patch", url=url, body=ds)
    req.execute()

    # return
    try:
        return pyaurorax.sources.get_using_identifier(ds.identifier, format=pyaurorax.FORMAT_FULL_RECORD)
    except Exception:
        raise pyaurorax.AuroraXException("Could not update data source")
