"""
AuroraX data sources are unique instruments that produce ephemeris or data product records.
"""
import pyaurorax
import datetime
import pprint
from pydantic import BaseModel
from typing import List, Dict


class DataSource(BaseModel):
    """
    Data source data type.

    Attributes:
        identifier: an integer unique to the data source.
        program: a string representing the data source program.
        platform: a string representing the data source platform.
        instrument_type: a string representing the data source instrument type.
        source_type: a string representing the data source type.
        display_name: a string representing the data source's proper display name.
        metadata: a dictionary of metadata properties.
        owner: a string representing the data source's owner in AuroraX.
        maintainers: a list of strings representing the email addresses of AuroraX accounts
            that can alter this data source and its associated records.
        ephemeris_metadata_schema: a list of dictionaries capturing the metadata keys and values
            that can appear in ephemeris records associated with the data source.
        data_product_metadata_schema: a list of dictionaries capturing the metadata keys and values
            that can appear in data product records associated with the data source.

    """
    identifier: int = None
    program: str = None
    platform: str = None
    instrument_type: str = None
    source_type: str = None
    display_name: str = None
    metadata: Dict = None
    owner: str = None
    maintainers: List[str] = None
    ephemeris_metadata_schema: List[Dict] = None
    data_product_metadata_schema: List[Dict] = None

    def __str__(self) -> str:
        """
        String method.

        Returns:
            String format of DataSource object.

        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation.

        Returns:
            Object representation of DataSource object.

        """
        return pprint.pformat(self.__dict__)


class DataSourceStatistics(BaseModel):
    """
    Data type for data source statistics.

    Attributes:
        data_source: the data source the statistics are associated with
        earliest_ephemeris_loaded: datetime.datetime of the earliest ephemeris record
        latest_ephemeris_loaded: datetime.datetime of the latest ephemeris record
        ephemeris_count: total number of ephemeris records for this data source
        earliest_data_product_loaded: datetime.datetime of the earliest data_product record
        latest_data_product_loaded: datetime.datetime of the latest data product record
        data_product_count: total number of ephemeris records for this data source
    """
    data_source: DataSource
    earliest_ephemeris_loaded: datetime.datetime = None
    latest_ephemeris_loaded: datetime.datetime = None
    ephemeris_count: int
    earliest_data_product_loaded: datetime.datetime = None
    latest_data_product_loaded: datetime.datetime = None
    data_product_count: int

    def __str__(self) -> str:
        """
        String method.

        Returns:
            String format of DataSource object.

        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation.

        Returns:
            Object representation of DataSource object.

        """
        return pprint.pformat(self.__dict__)


def list(order: str = "identifier", format: str = "basic_info") -> List[DataSource]:
    """
    Retrieve all data source records.

    Attributes:
        order: string value to order results by (identifier, program, platform,
            instrument_type, display_name, owner), defaults to "identifier".
        format: string record format, defaults to "basic_info".

    Returns:
        A list of AuroraX DataSource objects.

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error.
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error.
    """
    params = {
        format: format
    }
    # make request
    req = pyaurorax.AuroraXRequest(
        method="get", url=pyaurorax.api.urls.data_sources_url, params=params if format else None)
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
    Retrieve a specific data source record.

    Attributes:
        program: the string name of the program.
        platform: the string name of the platform.
        instrument_type: the string name of the instrument type.
        format: record format, defaults to "basic_info".

    Returns:
        An AuroraX DataSource object matching the input parameters.

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error.
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error.
        pyaurorax.exceptions.AuroraXNotFoundException: source not found.

    """
    # make request
    params = {
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "format": format,
    }
    req = pyaurorax.AuroraXRequest(
        method="get", url=pyaurorax.api.urls.data_sources_url, params=params)
    res = req.execute()

    # set results to the first thing
    if (len(res.data) == 1):
        res.data = res.data[0]

        return DataSource(**res.data)
    else:
        raise pyaurorax.AuroraXNotFoundException("Data source not found")


def get_using_filters(program: str = None,
                      platform: str = None,
                      instrument_type: str = None,
                      source_type: str = None,
                      owner: str = None,
                      format: str = "basic_info",
                      order: str = "identifier",) -> List[DataSource]:
    """
    Retrieve all data source records matching a filter.

    Attributes:
        program: the string name of the program.
        platform: the string name of the platform.
        instrument_type: the string name of the instrument type.
        source_type: the string name of the data source type.
        owner: the AuroraX data source owner's email address.
        format: record format, defaults to "basic_info".
        order: string value to order results by (identifier, program, platform,
            instrument_type, display_name, owner), defaults to "identifier".

    Returns:
        A list of AuroraX DataSource objects matching the filter parameters.

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error.
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error.

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
    req = pyaurorax.AuroraXRequest(
        method="get", url=pyaurorax.api.urls.data_sources_url, params=params)
    res = req.execute()

    # order results
    res.data = sorted(res.data, key=lambda x: x[order])

    # return
    if len(res.data):
        return [DataSource(**ds) for ds in res.data]
    else:
        return []


def get_using_identifier(identifier: int, format: str = "basic_info") -> DataSource:
    """
    Retrieve data source record matching an identifier.

    Attributes:
        identifier: an integer unique to the data source.
        format: record format, defaults to "basic_info".

    Returns:
        An AuroraX DataSource object matching the input identifier.

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error.
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error.

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
              format: str = "basic_info",
              slow: bool = False) -> Dict:
    """
    Retrieve statistics for a data source.

    Attributes:
        identifier: an integer unique to the data source.
        format: record format, defaults to "basic_info".
        slow: a boolean indicating whether to use slow method which gets most up-to-date stats info.

    Returns:
        A dictionary of statistics information about the data source.

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error.
        pyaurorax.exceptions.AuroraXNotFoundException: data source not found.
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error.

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
    Add a new data source to AuroraX.

    Attributes:
        data_source: the fully defined AuroraX DataSource object to add.

    Returns:
        The newly created AuroraX DataSource object.

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error.
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error.
        pyaurorax.exceptions.AuroraXDuplicateException: duplicate data source, already exists.

    """

    # do request
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

    req = pyaurorax.AuroraXRequest(
        method="post", url=pyaurorax.api.urls.data_sources_url, body=request_data)
    res = req.execute()

    # evaluate response
    if (res.status_code == 409):
        raise pyaurorax.AuroraXDuplicateException(
            "%s - %s" % (res.data["error_code"], res.data["error_message"]))

    # return
    try:
        return DataSource(**res.data)
    except Exception:
        raise pyaurorax.AuroraXException("Could not create data source.")


def delete(identifier: int) -> int:
    """
    Delete a data source from AuroraX.

    Attributes:
        identifier: an integer unique to the data source.

    Returns:
        1 on success.

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error.
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error.
        pyaurorax.exceptions.AuroraXNotFoundException: data source not found.
        pyaurorax.exceptions.AuroraXConflictException: conflict of some type.

    """
    # do request
    url = "%s/%d" % (pyaurorax.api.urls.data_sources_url, identifier)
    req = pyaurorax.AuroraXRequest(
        method="delete", url=url, null_response=True)
    res = req.execute()

    # evaluate response
    if (res.status_code == 400):
        raise pyaurorax.AuroraXBadParametersException(
            "%s - %s" % (res.data["error_code"], res.data["error_message"]))
    elif (res.status_code == 409):
        raise pyaurorax.AuroraXConflictException(
            "%s - %s" % (res.data["error_code"], res.data["error_message"]))

    # return
    return 1


def update(data_source: DataSource) -> DataSource:
    """
    Update a data source in AuroraX.

    This operation will fully replace the data source with the data_source argument passed in.
    Please make sure data_source is complete. Refer to examples for usage.

    Attributes:
        data_source: the fully defined AuroraX DataSource object to update.

    Returns:
        The updated AuroraX DataSource object.

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error.
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error.
        pyaurorax.exceptions.AuroraXNotFoundException: data source not found.
        pyaurorax.exceptions.AuroraXBadParametersException: missing parameters.

    """
    if not all([data_source.identifier, data_source.program, data_source.platform,
                data_source.instrument_type, data_source.source_type, data_source.display_name]):
        raise pyaurorax.AuroraXBadParametersException(
            "One or more required data source fields are missing. Update operation aborted.")

    # set URL
    url = f"{pyaurorax.api.urls.data_sources_url}/{data_source.identifier}"

    # make request to update the data source passed in
    req = pyaurorax.AuroraXRequest(method="put", url=url, body=data_source)
    req.execute()

    # return
    try:
        return pyaurorax.sources.get(data_source.program, data_source.platform, data_source.instrument_type, "full_record")
    except Exception:
        raise pyaurorax.AuroraXException("Could not update data source.")


def partial_update(identifier: int,
                   program: str = None,
                   platform: str = None,
                   instrument_type: str = None,
                   source_type: str = None,
                   display_name: str = None,
                   metadata: Dict = None,
                   owner: str = None,
                   maintainers: List[str] = None,
                   ephemeris_metadata_schema: List[Dict] = None,
                   data_product_metadata_schema: List[Dict] = None) -> DataSource:
    """
    Partially update a data source in AuroraX.

    Omitted fields are ignored in the update. Refer to examples for usage.

    Attributes:
        identifier: an integer unique to the data source.
        program: a string representing the data source program.
        platform: a string representing the data source platform.
        instrument_type: a string representing the data source instrument type.
        source_type: a string representing the data source type.
        display_name: a string representing the data source's proper display name.
        metadata: a dictionary of metadata properties.
        owner: a string representing the data source's owner in AuroraX.
        maintainers: a list of strings representing the email addresses of AuroraX accounts
            that can alter this data source and its associated records.
        ephemeris_metadata_schema: a list of dictionaries capturing the metadata keys and values
            that can appear in ephemeris records associated with the data source.
        data_product_metadata_schema: a list of dictionaries capturing the metadata keys and values
            that can appear in data product records associated with the data source.

    Returns:
        The updated AuroraX DataSource object.

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error.
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error.
        pyaurorax.exceptions.AuroraXNotFoundException: data source not found.
        pyaurorax.exceptions.AuroraXBadParametersException: missing parameters.

    """
    if not identifier:
        raise pyaurorax.AuroraXBadParametersException(
            "Required identifier field is missing. Update operation aborted.")

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
        return pyaurorax.sources.get_using_identifier(ds.identifier, "full_record")
    except Exception:
        raise pyaurorax.AuroraXException("Could not update data source.")
