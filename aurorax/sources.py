import aurorax
import pprint
from pydantic import BaseModel
from typing import List, Dict

class DataSource(BaseModel):
    """
    Data source data type

    Attributes:
        identifier: an integer unique to the data source
        program: a string representing the data source program
        platform: a string representing the data source platform
        instrument_type: a string representing the data source instrument type
        source_type: a string representing the data source type
        display_name: a string representing the data source's proper display name
        metadata: a dictionary of metadata properties
        owner: a string representing the data source's owner in AuroraX
        maintainers: a list of strings representing the email addresses of AuroraX accounts
            that can alter this data source and its associated records
        ephemeris_metadata_schema: a list of dictionaries capturing the metadata keys and values 
            that can appear in ephemeris records associated with the data source
        data_product_metadata_schema: a list of dictionaries capturing the metadata keys and values 
            that can appear in data product records associated with the data source

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
    Retrieve all data source records.

    Attributes:
        order: string value to order results by (identifier, program, platform,
            instrument_type, display_name, owner), defaults to "identifier"
        format: string record format, defaults to "basic_info"

    Returns:
        A list of AuroraX DataSource objects

    Raises:
        aurorax.exceptions.AuroraXMaxRetriesException: max retry error
        aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
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
    Retrieve a specific data source record.

    Attributes:
        program: the string name of the program
        platform: the string name of the platform
        instrument_type: the string name of the instrument type
        format: record format, defaults to "basic_info"

    Returns:
        An AuroraX DataSource object matching the input parameters

    Raises:
        aurorax.exceptions.AuroraXMaxRetriesException: max retry error
        aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
        aurorax.exceptions.AuroraXNotFoundException: source not found

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
    Retrieve all data source records matching a filter.

    Attributes:
        program: the string name of the program
        platform: the string name of the platform
        instrument_type: the string name of the instrument type
        source_type: the string name of the data source type
        owner: the AuroraX data source owner's email address
        format: record format, defaults to "basic_info"
        order: string value to order results by (identifier, program, platform,
            instrument_type, display_name, owner), defaults to "identifier"

    Returns:
        A list of AuroraX DataSource objects matching the filter parameters

    Raises:
        aurorax.exceptions.AuroraXMaxRetriesException: max retry error
        aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error

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
    Retrieve data source record matching an identifier.

    Attributes:
        identifier: an integer unique to the data source
        format: record format, defaults to "basic_info"

    Returns:
        An AuroraX DataSource object matching the input identifier.

    Raises:
        aurorax.exceptions.AuroraXMaxRetriesException: max retry error
        aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error

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
    Retrieve statistics for a data source.

    Attributes:
        identifier: an integer unique to the data source
        format: record format, defaults to "basic_info"
        slow: a boolean indicating whether to use slow method which gets most up-to-date stats info

    Returns:
        A dictionary of statistics information about the data source.

    Raises:
        aurorax.exceptions.AuroraXMaxRetriesException: max retry error
        aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error

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
    Add a new data source to AuroraX.

    Attributes:
        data_source: the fully defined AuroraX DataSource object to add

    Returns:
        The newly created AuroraX DataSource object.

    Raises:
        aurorax.exceptions.AuroraXMaxRetriesException: max retry error
        aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
        aurorax.exceptions.AuroraXDuplicateException: duplicate data source, already exists

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
    Delete a data source from AuroraX.

    Attributes:
        identifier: an integer unique to the data source

    Returns:
        1 on success.

    Raises:
        aurorax.exceptions.AuroraXMaxRetriesException: max retry error
        aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
        aurorax.exceptions.AuroraXNotFoundException: data source not found
        aurorax.exceptions.AuroraXConflictException: conflict of some type

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
    Update a data source in AuroraX.
    
    This operation will fully replace the data source with the data_source argument passed in.
    Please make sure data_source is complete. Refer to examples for usage.

    Attributes:
        data_source: the fully defined AuroraX DataSource object to update

    Returns:
        The updated AuroraX DataSource object.

    Raises:
        aurorax.exceptions.AuroraXMaxRetriesException: max retry error
        aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
        aurorax.exceptions.AuroraXNotFoundException: data source not found
        aurorax.exceptions.AuroraXBadParametersException: missing parameters

    """
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
        identifier: an integer unique to the data source
        program: a string representing the data source program
        platform: a string representing the data source platform
        instrument_type: a string representing the data source instrument type
        source_type: a string representing the data source type
        display_name: a string representing the data source's proper display name
        metadata: a dictionary of metadata properties
        owner: a string representing the data source's owner in AuroraX
        maintainers: a list of strings representing the email addresses of AuroraX accounts
            that can alter this data source and its associated records
        ephemeris_metadata_schema: a list of dictionaries capturing the metadata keys and values 
            that can appear in ephemeris records associated with the data source
        data_product_metadata_schema: a list of dictionaries capturing the metadata keys and values 
            that can appear in data product records associated with the data source

    Returns:
        The updated AuroraX DataSource object.

    Raises:
        aurorax.exceptions.AuroraXMaxRetriesException: max retry error
        aurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
        aurorax.exceptions.AuroraXNotFoundException: data source not found
        aurorax.exceptions.AuroraXBadParametersException: missing parameters

    """
    if not identifier:
        raise aurorax.AuroraXBadParametersException("Required identifier field is missing. Update operation aborted.")

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
    url = f"{aurorax.api.urls.data_sources_url}/{ds.identifier}"

    # make request to update the data source passed in
    req = aurorax.AuroraXRequest(method="patch", url=url, body=ds)
    req.execute()

    # return
    try:
        return aurorax.sources.get_using_identifier(ds.identifier, "full_record")
    except:
        raise aurorax.AuroraXException("Could not update data source.")
