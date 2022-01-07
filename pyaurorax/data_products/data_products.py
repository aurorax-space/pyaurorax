"""
Main functions for performing data product searches
"""

import pyaurorax
import datetime
import humanize
from typing import Dict, List, Optional
from .classes.data_product import DataProduct
from .classes.search import Search

# pdoc init
__pdoc__: Dict = {}


def __validate_data_source(identifier: int,
                           records: List[DataProduct]) -> Optional[DataProduct]:
    # get all current sources
    sources = {source.identifier: source for source in pyaurorax.sources.list()}
    if identifier not in sources.keys():
        raise pyaurorax.AuroraXValidationException(f"Data source with unique identifier "
                                                   "{identifier} could not be found")

    # process each record to make sure the program/platform/instrument_type matches
    # the identifier found for the data source
    for record in records:
        # check the identifier, program name, platform name, and instrument type
        try:
            reference = sources[record.data_source.identifier]
        except KeyError:
            raise pyaurorax.AuroraXValidationException(f"Data source with unique identifier "
                                                       "{record.data_source.identifier} could "
                                                       "not be found")

        # check if it's a bad record
        if not (record.data_source.program == reference.program
                and record.data_source.platform == reference.platform
                and record.data_source.instrument_type == reference.instrument_type):
            return record

    # found no bad records
    return None


def search_async(start: datetime.datetime,
                 end: datetime.datetime,
                 programs: Optional[List[str]] = None,
                 platforms: Optional[List[str]] = None,
                 instrument_types: Optional[List[str]] = None,
                 metadata_filters: Optional[List[Dict]] = None,
                 data_product_type_filters: Optional[List[str]] = None,
                 response_format: Optional[Dict] = None,
                 metadata_filters_logical_operator: Optional[str] = None) -> Search:
    """
    Submit a request for a data products search, return asynchronously

    Args:
        start: start timestamp of the search (inclusive)
        end: end timestamp of the search (inclusive)
        programs: list of programs to search through, defaults to None
        platforms: list of platforms to search through, defaults to None
        instrument_types: list of instrument types to search through, defaults to None
        metadata_filters: list of dictionaries describing metadata keys and values
            to filter on, defaults to None

            e.g. {
                "key": "string",
                "operator": "=",
                "values": [
                    "string"
                ]
            }
        data_product_type_filters: list of dictionaries describing data product
            types to filter on e.g. "keogram", defaults to None

            e.g. {
                "key": "string",
                "operator": "=",
                "values": [
                    "string"
                ]
            }
        response_format: JSON representation of desired data response format

    Returns:
        a pyaurorax.data_products.Search object
    """
    s = pyaurorax.data_products.Search(start,
                                       end,
                                       programs=programs,
                                       platforms=platforms,
                                       instrument_types=instrument_types,
                                       metadata_filters=metadata_filters,
                                       data_product_type_filters=data_product_type_filters,
                                       response_format=response_format,
                                       metadata_filters_logical_operator=metadata_filters_logical_operator)
    s.execute()
    return s


def search(start: datetime.datetime,
           end: datetime.datetime,
           programs: Optional[List[str]] = None,
           platforms: Optional[List[str]] = None,
           instrument_types: Optional[List[str]] = None,
           metadata_filters: Optional[List[Dict]] = None,
           data_product_type_filters: Optional[List[str]] = None,
           verbose: Optional[bool] = False,
           poll_interval: Optional[float] = pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME,
           response_format: Optional[Dict] = None,
           metadata_filters_logical_operator: Optional[str] = None) -> Search:
    """
    Search for data product records and block until results are returned

    Args:
        start: start timestamp of the search (inclusive)
        end: end timestamp of the search (inclusive)
        programs: list of programs to search through, defaults to None
        platforms: list of platforms to search through, defaults to None
        instrument_types: list of instrument types to search through, defaults to None
        metadata_filters: list of dictionaries describing metadata keys and values
            to filter on, defaults to None

            e.g. {
                "key": "string",
                "operator": "=",
                "values": [
                    "string"
                ]
            }
        data_product_type_filters: list of dictionaries describing data product types to
            filter on e.g. "keogram", defaults to None

            e.g. {
                "key": "string",
                "operator": "=",
                "values": [
                    "string"
                ]
            }
        verbose: output poll times, defaults to False
        poll_interval: time in seconds to wait between polling attempts, defaults
            to pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME
        response_format: JSON representation of desired data response format

    Returns:
        a pyaurorax.data_products.Search object
    """
    # create a Search() object
    s = Search(start,
               end,
               programs,
               platforms,
               instrument_types,
               metadata_filters,
               data_product_type_filters,
               response_format=response_format,
               metadata_filters_logical_operator=metadata_filters_logical_operator)
    if (verbose is True):
        print("[%s] Search object created" % (datetime.datetime.now()))

    # execute the search
    s.execute()
    if (verbose is True):
        print("[%s] Request submitted" % (datetime.datetime.now()))
        print("[%s] Request ID: %s" % (datetime.datetime.now(), s.request_id))
        print("[%s] Request details available at: %s" % (datetime.datetime.now(),
                                                         s.request_url))

    # wait for data
    if (verbose is True):
        print("[%s] Waiting for data ..." % (datetime.datetime.now()))
    s.wait(poll_interval=poll_interval, verbose=verbose)

    # get the data
    if (verbose is True):
        print("[%s] Retrieving data ..." % (datetime.datetime.now()))
    s.get_data()

    # return response with the data
    if (verbose is True):
        print("[%s] Retrieved %s of data containing %d records" % (datetime.datetime.now(),
                                                                   humanize.filesize.naturalsize(
                                                                       s.status["search_result"]["file_size"]),
                                                                   s.status["search_result"]["result_count"]))
    return s


def upload(identifier: int,
           records: List[DataProduct],
           validate_source: Optional[bool] = False) -> int:
    """
    Upload data product records to AuroraX

    Args:
        identifier: the AuroraX data source ID
        records: list of pyaurorax.data_products.DataProduct records to upload
        validate_source: boolean, set to True to validate all records before uploading

    Returns:
        1 for success, raises exception on error

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected content error
        pyaurorax.exceptions.AuroraXUploadException: upload error
        pyaurorax.exceptions.AuroraXValidationException: data source validation error
    """
    # validate record sources if the flag is set
    if validate_source:
        validation_error = __validate_data_source(identifier, records)
        if validation_error:
            raise pyaurorax.AuroraXValidationException(f"Unable to validate data source "
                                                       "found in record: {validation_error}")

    # translate each data product record to a request-friendly
    # dict (ie. convert datetimes to strings, etc.)
    for i, _ in enumerate(records):
        if (type(records[i]) is DataProduct):
            records[i] = records[i].to_json_serializable()  # type: ignore

    # make request
    url = pyaurorax.api.urls.data_products_upload_url.format(identifier)
    req = pyaurorax.AuroraXRequest(method="post",
                                   url=url,
                                   body=records,
                                   null_response=True)
    res = req.execute()

    # evaluate response
    if (res.status_code == 400):
        if type(res.data) is list:
            raise pyaurorax.AuroraXUploadException("%s - %s" % (res.status_code,
                                                                res.data[0]["error_message"]))

        raise pyaurorax.AuroraXUploadException("%s - %s" % (res.status_code,
                                                            res.data["error_message"]))

    # return
    return 1


def delete_daterange(data_source: pyaurorax.sources.DataSource,
                     start: datetime.datetime,
                     end: datetime.datetime,
                     data_product_types: Optional[List[str]] = None) -> int:
    """
    Deletes data products associated with a data source in the date range
    provided. This method is asynchronous.

    Args:
        data_source: pyaurorax.sources.DataSource source associated
            with the data product records. Identifier, program, platform,
            and instrument_type are required.
        start: timestamp marking beginning of range to delete records for, inclusive
        end: timestamp marking end of range to delete records for, inclusive
        data_product_types: specific types of data product to delete, e.g.
            ["keogram", "movie"]. If omitted, all data product types will be deleted.

    Returns:
        1 on success

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
        pyaurorax.exceptions.AuroraXNotFoundException: source not found
        pyaurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation
    """
    if not all([data_source.identifier, data_source.program, data_source.platform, data_source.instrument_type]):
        raise pyaurorax.AuroraXBadParametersException("One or more required data source parameters "
                                                      "are missing, delete operation aborted")

    # do request to get all data products between start and end datetimes
    try:
        s = pyaurorax.data_products.search(start=start,
                                           end=end,
                                           programs=[data_source.program],
                                           platforms=[data_source.platform],
                                           instrument_types=[data_source.instrument_type],
                                           data_product_type_filters=[] if not data_product_types else data_product_types)
    except Exception as e:
        raise pyaurorax.AuroraXException(e)

    # collect URLs from search result
    urls = []
    for dp in s.data:
        urls.append(dp.url)  # type: ignore

    # do delete request
    return delete(data_source, urls)


def delete(data_source: pyaurorax.sources.DataSource,
           urls: List[str]) -> int:
    """
    Delete data products by URL. This method is asynchronous.

    Args:
        data_source: the pyaurorax.sources.DataSource source associated with the
            data product records. Identifier, program, platform, and instrument_type
            are required.
        urls: list of URL strings associated with the data products being deleted

    Returns:
        1 on success

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
        pyaurorax.exceptions.AuroraXBadParametersException: invalid parameters entered
        pyaurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation
    """
    if not all([data_source.identifier, data_source.program, data_source.platform, data_source.instrument_type]):
        raise pyaurorax.AuroraXBadParametersException("One or more required data source parameters "
                                                      "are missing, delete operation aborted")

    # do request
    url = pyaurorax.api.urls.data_products_upload_url.format(data_source.identifier)
    params = {
        "program": data_source.program,
        "platform": data_source.platform,
        "instrument_type": data_source.instrument_type,
        "urls": urls
    }
    delete_req = pyaurorax.AuroraXRequest(method="delete",
                                          url=url,
                                          body=params,
                                          null_response=True)
    res = delete_req.execute()

    # evaluate response
    if (res.status_code == 400):
        if type(res.data) is list:
            raise pyaurorax.AuroraXBadParametersException("%s - %s" % (res.status_code,
                                                                       res.data[0]["message"]))
        raise pyaurorax.AuroraXBadParametersException("%s - %s" % (res.status_code,
                                                                   res.data["message"]))

    # return
    return 1
