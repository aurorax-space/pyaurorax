import pyaurorax
from typing import List, Dict, Optional
from ._classes._data_source import DataSource
from ._classes._data_source_stats import DataSourceStatistics

# pdoc init
__pdoc__: Dict = {}


def list(order: Optional[str] = "identifier",
         format: Optional[str] = "full_record") -> List[DataSource]:
    """
    Retrieve all data source records

    Args:
        order: string value to order results by (identifier, program, platform,
               instrument_type, display_name, owner), defaults to "identifier"
        format: string record format, defaults to "full_record"

    Returns:
        a list of AuroraX DataSource objects

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
        format: Optional[str] = "full_record") -> DataSource:
    """
    Retrieve a specific data source record

    Args:
        program: the string name of the program
        platform: the string name of the platform
        instrument_type: the string name of the instrument type
        format: record format, defaults to "full_record"

    Returns:
        an AuroraX DataSource object matching the input parameters

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
                      format: Optional[str] = "full_record",
                      order: Optional[str] = "identifier") -> List[DataSource]:
    """
    Retrieve all data source records matching a filter

    Args:
        program: the name of the program
        platform: the name of the platform
        instrument_type: the name of the instrument type
        source_type: the name of the data source type
        owner: the AuroraX data source owner's email address
        format: record format, defaults to "full_record"
        order: the value to order results by (identifier, program, platform,
            instrument_type, display_name, owner), defaults to "identifier"

    Returns:
        A list of AuroraX DataSource objects matching the filter parameters

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
                         format: Optional[str] = "full_record") -> DataSource:
    """
    Retrieve data source record matching an identifier

    Args:
        identifier: an integer unique to the data source
        format: record format, defaults to "basic_info"

    Returns:
        An AuroraX DataSource object matching the input identifier

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
              format: Optional[str] = "full_record",
              slow: Optional[bool] = False) -> DataSourceStatistics:
    """
    Retrieve statistics for a data source

    Args:
        identifier: an integer unique to the data source
        format: record format, defaults to "full_record"
        slow: a boolean indicating whether to use slow method which gets
            most up-to-date stats info (this may take longer to return)

    Returns:
        a DataSourceStatistics object with information about the data source

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
        data_source: the fully defined AuroraX DataSource object to add

    Returns:
        the newly created AuroraX DataSource object

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
        identifier: an integer unique to the data source

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
        data_source: the fully defined AuroraX DataSource object to update

    Returns:
        the updated AuroraX DataSource object

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
                                     format="full_record")
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
    Partially update a data source in AuroraX

    Omitted fields are ignored in the update. Refer to examples for usage

    Args:
        identifier: an integer unique to the data source
        program: a string representing the data source program
        platform: a string representing the data source platform
        instrument_type: a string representing the data source instrument type
        source_type: a string representing the data source type
        display_name: a string representing the data source's proper display name
        metadata: a dictionary of metadata properties
        owner: a string representing the data source's owner in AuroraX
        maintainers: a list of strings representing the email addresses of AuroraX
            accounts that can alter this data source and its associated records
        ephemeris_metadata_schema: a list of dictionaries capturing the metadata
            keys and values that can appear in ephemeris records associated with
            the data source
        data_product_metadata_schema: a list of dictionaries capturing the metadata
            keys and values that can appear in data product records associated with
            the data source

    Returns:
        the updated AuroraX DataSource object

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
        return pyaurorax.sources.get_using_identifier(ds.identifier, format="full_record")
    except Exception:
        raise pyaurorax.AuroraXException("Could not update data source")
