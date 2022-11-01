"""
Functions for interacting with data sources
"""

import warnings
from typing import List, Dict, Optional, Any
from .classes.data_source import DataSource
from .classes.data_source_stats import DataSourceStatistics
from ..sources import FORMAT_FULL_RECORD, SOURCE_TYPE_NOT_APPLICABLE
from ..api import AuroraXRequest, urls
from ..exceptions import (AuroraXNotFoundException,
                          AuroraXDuplicateException,
                          AuroraXBadParametersException,
                          AuroraXConflictException,
                          AuroraXException)

# pdoc init
__pdoc__: Dict = {}


def list(program: Optional[str] = None,
         platform: Optional[str] = None,
         instrument_type: Optional[str] = None,
         source_type: Optional[str] = None,
         owner: Optional[str] = None,
         format: Optional[str] = FORMAT_FULL_RECORD,
         order: Optional[str] = "identifier",
         include_stats: Optional[bool] = False,
         include_na: Optional[bool] = False) -> List[DataSource]:
    """
    Retrieve all data source records (using params to filter as desired)

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
        include_stats: include additional stats information about the data source (note:
            slower response time since an additional request must be done for each
            data source), defaults to False
        include_na: include "not_applicable" special data sources (ie. adhoc sources)

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
    req = AuroraXRequest(method="get",
                         url=urls.data_sources_url,
                         params=params)
    res = req.execute()

    # order results
    res.data = sorted(res.data, key=lambda x: x[order])

    # cast
    if len(res.data):
        sources = [DataSource(**ds, format=format) for ds in res.data]
    else:
        return []

    # remove not_applicable sources
    sources_pruned = []
    if (include_na is False):
        for source in sources:
            if (source.source_type != SOURCE_TYPE_NOT_APPLICABLE):
                sources_pruned.append(source)
    else:
        sources_pruned = sources

    # get stats if requested
    if (include_stats is True):
        for i in range(0, len(sources_pruned)):
            source_with_stats = get_stats(sources_pruned[i].identifier)
            sources_pruned[i].stats = source_with_stats.stats

    # return
    return sources_pruned


def search(programs: Optional[List[str]] = [],
           platforms: Optional[List[str]] = [],
           instrument_types: Optional[List[str]] = [],
           format: Optional[str] = FORMAT_FULL_RECORD,
           order: Optional[str] = "identifier",
           include_stats: Optional[bool] = False) -> List[DataSource]:
    """
    Search for data source records (using params to filter as desired)

    This is very similar to the 'list' function, however multiple programs,
    platforms, and/or instrument types can be supplied to this function. The
    'list' function only supports single values for those parameters.

    Args:
        programs: the programs to filter for, defaults to []
        platforms: the platforms to filter for, defaults to []
        instrument_type: the instrument types to filter for, defaults to []
        format: the format of the data sources returned, defaults to "full_record".
            Other options are in the pyaurorax.sources module, or at the top level
            using the pyaurorax.FORMAT_* variables.
        order: the value to order results by (identifier, program, platform,
            instrument_type, display_name), defaults to "identifier"
        include_stats: include additional stats information about the data source (note:
            slower response time since an additional request must be done for each
            data source), defaults to False

    Returns:
        any data sources matching the requested parameters

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
    """
    # make request
    request_data = {
        "programs": programs,
        "platforms": platforms,
        "instrument_types": instrument_types,
    }
    params = {
        "format": format,
    }
    req = AuroraXRequest(method="post",
                         url=urls.data_sources_search_url,
                         params=params,
                         body=request_data)
    res = req.execute()

    # order results
    res.data = sorted(res.data, key=lambda x: x[order])

    # cast
    if len(res.data):
        data_sources = [DataSource(**ds, format=format) for ds in res.data]
    else:
        return []

    # get stats if requested
    if (include_stats is True):
        for i in range(0, len(data_sources)):
            data_source_with_stats = get_stats(data_sources[i].identifier)
            data_sources[i].stats = data_source_with_stats.stats

    # return
    return data_sources


def get(program: str,
        platform: str,
        instrument_type: str,
        format: Optional[str] = FORMAT_FULL_RECORD,
        include_stats: Optional[bool] = False) -> DataSource:
    """
    Retrieve a specific data source record

    Args:
        program: the program name
        platform: the platform name
        instrument_type: the instrument type name
        format: the format of the data sources returned, defaults to "full_record".
            Other options are in the pyaurorax.sources module, or at the top level
            using the pyaurorax.FORMAT_* variables.
        include_stats: include additional stats information about the data source (note:
            slower response time since an additional request must be done for each
            data source), defaults to False

    Returns:
        the data source matching the requested parameters

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
        pyaurorax.exceptions.AuroraXNotFoundException: source not found
    """
    # get the data source
    data_sources = list(program=program,
                        platform=platform,
                        instrument_type=instrument_type,
                        format=format,
                        include_stats=include_stats)

    # set results to the first thing found
    if (len(data_sources) == 1):
        return data_sources[0]
    elif (len(data_sources) > 1):
        warnings.warn("Found more than one data source matching this criteria, "
                      "returning the first (found %d)" % (len(data_sources)))
        return data_sources[0]
    else:
        raise AuroraXNotFoundException("No matching data source found")


def get_using_filters(program: Optional[str] = None,
                      platform: Optional[str] = None,
                      instrument_type: Optional[str] = None,
                      source_type: Optional[str] = None,
                      owner: Optional[str] = None,
                      format: Optional[str] = FORMAT_FULL_RECORD,
                      order: Optional[str] = "identifier",
                      include_stats: Optional[bool] = False,
                      include_na: Optional[bool] = False) -> List[DataSource]:
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
        include_stats: include additional stats information about the data source (note:
            slower response time since an additional request must be done for each
            data source), defaults to False
        include_na: include "not_applicable" special data sources (ie. adhoc sources)

    Returns:
        any data sources matching the requested parameters

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
    """
    # get data sources
    data_sources = list(program=program,
                        platform=platform,
                        instrument_type=instrument_type,
                        source_type=source_type,
                        owner=owner,
                        format=format,
                        order=order,
                        include_stats=include_stats,
                        include_na=include_na)

    # return
    return data_sources


def get_using_identifier(identifier: int,
                         format: Optional[str] = FORMAT_FULL_RECORD,
                         include_stats: Optional[bool] = False) -> DataSource:
    """
    Retrieve data source record matching an identifier

    Args:
        identifier: the AuroraX unique ID for the data source
        format: the format of the data sources returned, defaults to "full_record".
            Other options are in the pyaurorax.sources module, or at the top level
            using the pyaurorax.FORMAT_* variables.
        include_stats: include additional stats information about the data source (note:
            slower response time since an additional request must be done for each
            data source), defaults to False

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
    url = "%s/%d" % (urls.data_sources_url, identifier)
    req = AuroraXRequest(method="get", url=url, params=params)
    res = req.execute()

    # cast
    data_source = DataSource(**res.data, format=format)

    # get stats if requested
    if (include_stats is True):
        data_source = get_stats(data_source.identifier)

    # return
    return data_source


def get_stats(identifier: int,
              format: Optional[str] = FORMAT_FULL_RECORD,
              slow: Optional[bool] = False) -> DataSource:
    """
    Retrieve statistics for a data source

    Args:
        identifier: the AuroraX unique ID for the data source
        format: the format of the data sources returned, defaults to "full_record".
            Other options are in the pyaurorax.sources module, or at the top level
            using the pyaurorax.FORMAT_* variables.
        slow: retrieve the stats using a slower, but more accurate method, defaults to False

    Returns:
        the data source including additional stats information about it

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
    url = "%s/%d/stats" % (urls.data_sources_url, identifier)
    req = AuroraXRequest(method="get", url=url, params=params)
    res = req.execute()

    # cast data source record
    stats = DataSourceStatistics(**res.data)
    ds = DataSource(**res.data["data_source"], format=format)
    ds.stats = stats

    # return
    return ds


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
    }  # type: Dict[str, Any]
    if (data_source.identifier is not None):
        request_data["identifier"] = data_source.identifier

    # make request
    req = AuroraXRequest(method="post",
                         url=urls.data_sources_url,
                         body=request_data)
    res = req.execute()

    # evaluate response
    if (res.status_code == 409):
        raise AuroraXDuplicateException("%s - %s" % (res.data["error_code"],
                                                     res.data["error_message"]))

    # return
    try:
        return DataSource(**res.data)
    except Exception:
        raise AuroraXException("Could not create data source")


def delete(identifier: int) -> int:
    """
    Delete a data source from AuroraX

    Args:
        identifier: the AuroraX unique ID for the data source

    Returns:
        0 on success, raises error if an issue was encountered

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
        pyaurorax.exceptions.AuroraXNotFoundException: data source not found
        pyaurorax.exceptions.AuroraXConflictException: conflict of some type
    """
    # do request
    url = "%s/%d" % (urls.data_sources_url, identifier)
    req = AuroraXRequest(method="delete",
                         url=url,
                         null_response=True)
    res = req.execute()

    # evaluate response
    if (res.status_code == 400):
        raise AuroraXBadParametersException("%s - %s" % (res.data["error_code"],
                                                         res.data["error_message"]))
    elif (res.status_code == 409):
        raise AuroraXConflictException("%s - %s" % (res.data["error_code"],
                                                    res.data["error_message"]))

    # return
    return 0


def update(data_source: DataSource) -> DataSource:
    """
    Update a data source in AuroraX

    This operation will fully replace the data source with the
    data_source argument passed in. Be sure that the data_source
    object is complete. If the data source is missing the value
    for identifier, program, platform, instrument type, source
    type, or display name, the update will fail and raise a
    AuroraXBadParametersException exception.

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
    # check to make sure the identifier, program, platform, instrument type,
    # source type, and display name are all set in the data source
    if not all([data_source.identifier, data_source.program, data_source.platform,
                data_source.instrument_type, data_source.source_type, data_source.display_name]):
        raise AuroraXBadParametersException("One or more required data source fields "
                                            "are missing, update operation aborted")

    # set URL
    url = f"{urls.data_sources_url}/{data_source.identifier}"

    # make request to update the data source passed in
    req_data = data_source.__dict__
    del req_data["stats"]
    del req_data["format"]
    req = AuroraXRequest(method="put", url=url, body=req_data)
    req.execute()

    # return
    try:
        return get(data_source.program,
                   data_source.platform,
                   data_source.instrument_type,
                   format=FORMAT_FULL_RECORD)
    except Exception:
        raise AuroraXException("Could not update data source")


def update_partial(identifier: int,
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

    # set URL and request data
    url = f"{urls.data_sources_url}/{ds.identifier}"
    req_data = ds.__dict__
    del req_data["stats"]
    del req_data["format"]

    # make request
    req = AuroraXRequest(method="patch", url=url, body=req_data)
    req.execute()

    # return
    try:
        return get_using_identifier(ds.identifier, format=FORMAT_FULL_RECORD)
    except Exception:
        raise AuroraXException("Could not update data source")
