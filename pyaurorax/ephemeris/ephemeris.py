"""
Functions for performing ephemeris searches
"""

import datetime
import humanize
from typing import Dict, List, Optional
from .classes.ephemeris import Ephemeris
from .classes.search import Search
from ..sources import (DataSource,
                       list as sources_list)
from ..exceptions import (AuroraXSearchException,
                          AuroraXValidationException,
                          AuroraXUploadException,
                          AuroraXBadParametersException)
from ..requests import STANDARD_POLLING_SLEEP_TIME
from ..api import (AuroraXRequest, urls)

# pdoc init
__pdoc__: Dict = {}


def __validate_data_source(identifier: int,
                           records: List[Ephemeris]) -> Optional[Ephemeris]:
    # get all current sources
    sources = {source.identifier: source for source in sources_list()}
    if identifier not in sources.keys():
        raise AuroraXValidationException(f"Data source with unique identifier "
                                         "{identifier} could not be found")

    # process each record to make sure the program/platform/instrument_type matches
    # the identifier found for the data source
    for record in records:
        # check the identifier, program name, platform name, and instrument type
        try:
            reference = sources[record.data_source.identifier]
        except KeyError:
            raise AuroraXValidationException(f"Data source with unique identifier "
                                             "{record.data_source.identifier} could "
                                             "not be found")

        # check if it's a bad record
        if not (record.data_source.program == reference.program
                and record.data_source.platform == reference.platform
                and record.data_source.instrument_type == reference.instrument_type):
            return record

    # found no bad records
    return None


def search(start: datetime.datetime,
           end: datetime.datetime,
           programs: Optional[List[str]] = None,
           platforms: Optional[List[str]] = None,
           instrument_types: Optional[List[str]] = None,
           metadata_filters: Optional[List[Dict]] = None,
           metadata_filters_logical_operator: Optional[str] = None,
           response_format: Optional[Dict] = None,
           poll_interval: Optional[float] = STANDARD_POLLING_SLEEP_TIME,
           return_immediately: Optional[bool] = False,
           verbose: Optional[bool] = False) -> Search:
    """
    Search for ephemeris records

    By default, this function will block and wait until the request completes and
    all data is downloaded. If you don't want to wait, set the 'return_immediately`
    value to True. The Search object will be returned right after the search has been
    started, and you can use the helper functions as part of that object to get the
    data when it's done.

    Note: At least one search criteria from programs, platforms, or
    instrument_types, must be specified.

    Args:
        start: start timestamp of the search (inclusive)
        end: end timestamp of the search (inclusive)
        programs: list of programs to search through, defaults to None
        platforms: list of platforms to search through, defaults to None
        instrument_types: list of instrument types to search through, defaults to None
        metadata_filters: list of dictionaries describing metadata keys and
            values to filter on, defaults to None

            Example:

                [{
                    "key": "nbtrace_region",
                    "operator": "in",
                    "values": ["north polar cap"]
                }]
        metadata_filters_logical_operator: the logical operator to use when
            evaluating metadata filters (either 'AND' or 'OR'), defaults
            to "AND"
        response_format: JSON representation of desired data response format
        poll_interval: time in seconds to wait between polling attempts, defaults
            to pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME
        return_immediately: initiate the search and return without waiting for data to
            be received, defaults to False
        verbose: output poll times and other progress messages, defaults to False

    Returns:
        A pyaurorax.ephemeris.Search object

    Raises:
        pyaurorax.exceptions.AuroraXBadParametersException: missing parameters
    """
    # create a Search() object
    s = Search(start,
               end,
               programs=programs,
               platforms=platforms,
               instrument_types=instrument_types,
               metadata_filters=metadata_filters,
               metadata_filters_logical_operator=metadata_filters_logical_operator,
               response_format=response_format)
    if (verbose is True):
        print("[%s] Search object created" % (datetime.datetime.now()))

    # execute the search
    s.execute()
    if (verbose is True):
        print("[%s] Request submitted" % (datetime.datetime.now()))
        print("[%s] Request ID: %s" % (datetime.datetime.now(), s.request_id))
        print("[%s] Request details available at: %s" % (datetime.datetime.now(),
                                                         s.request_url))

    # return immediately if we wanted to
    if (return_immediately is True):
        return s

    # wait for data
    if (verbose is True):
        print("[%s] Waiting for data ..." % (datetime.datetime.now()))
    s.wait(poll_interval=poll_interval, verbose=verbose)

    # check if error condition encountered
    if (s.status["search_result"]["error_condition"] is True):
        # error encountered
        raise AuroraXSearchException(s.logs[-1]["summary"])

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
           records: List[Ephemeris],
           validate_source: Optional[bool] = False) -> int:
    """
    Upload ephemeris records to AuroraX

    Args:
        identifier: AuroraX data source ID
        records: ephemeris records to upload
        validate_source: validate all records before uploading, defaults to False

    Returns:
        0 for success, raises exception on error

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
            raise AuroraXValidationException("Unable to validate data source found "
                                             "in record: {}".format(validation_error))

    # translate each ephemeris record to a request-friendly
    # dict (ie. convert datetimes to strings, etc.)
    for i, _ in enumerate(records):
        if (type(records[i]) is Ephemeris):
            records[i] = records[i].to_json_serializable()  # type: ignore

    # make request
    url = urls.ephemeris_upload_url.format(identifier)
    req = AuroraXRequest(method="post",
                         url=url,
                         body=records,
                         null_response=True)
    res = req.execute()

    # evaluate response
    if (res.status_code == 400):
        raise AuroraXUploadException("%s - %s" % (res.data["error_code"],
                                                  res.data["error_message"]))

    # return
    return 0


def delete(data_source: DataSource,
           start: datetime.datetime,
           end: datetime.datetime) -> int:
    """
    Delete ephemeris records between a timeframe.

    The API processes this request asynchronously, so this method will return
    immediately whether or not the data has already been deleted.

    Args:
        data_source: data source associated with the data product records (note that
            identifier, program, platform, and instrument_type are required)
        start: timestamp marking beginning of range to delete records for, inclusive
        end: timestamp marking end of range to delete records for, inclusive

    Returns:
        0 on success

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
        pyaurorax.exceptions.AuroraXNotFoundException: source not found
        pyaurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation
        pyaurorax.exceptions.AuroraXBadParametersException: missing parameters
    """
    # check to make sure the identifier, program, platform, and instrument type are all set in the data source
    if not all([data_source.identifier, data_source.program, data_source.platform, data_source.instrument_type]):
        raise AuroraXBadParametersException("One or more required data source parameters "
                                            "are missing, delete operation aborted")

    # do request
    url = urls.ephemeris_upload_url.format(data_source.identifier)
    params = {
        "program": data_source.program,
        "platform": data_source.platform,
        "instrument_type": data_source.instrument_type,
        "start": start.strftime("%Y-%m-%dT%H:%M:%S"),
        "end": end.strftime("%Y-%m-%dT%H:%M:%S")
    }
    delete_req = AuroraXRequest(method="delete",
                                url=url,
                                body=params,
                                null_response=True)
    res = delete_req.execute()

    # evaluate response
    if (res.status_code == 400):
        if type(res.data) is list:
            raise AuroraXBadParametersException("%s - %s" % (res.status_code,
                                                             res.data[0]["message"]))
        raise AuroraXBadParametersException("%s - %s" % (res.data["error_code"],
                                                         res.data["error_message"]))

    # return
    return 0


def describe(search_obj: Search) -> str:
    """
    Describe an ephemeris search as a "SQL-like" string

    Args:
        search_obj: the ephemeris search object to describe

    Returns:
        the "SQL-like" string describing the ephemeris search object
    """
    # make request
    req = AuroraXRequest(method="post",
                         url=urls.describe_ephemeris_query_url,
                         body=search_obj.query)
    res = req.execute()

    # return
    return res.data


def get_request_url(request_id: str) -> str:
    """
    Get the ephemeris search request URL for a given
    request ID. This URL can be used for subsequent
    pyaurorax.requests function calls. Primarily this method
    facilitates delving into details about a set of already-submitted
    ephemeris searches.

    Args:
        request_id: the request identifier

    Returns:
        the request URL
    """
    url = urls.ephemeris_request_url.format(request_id)
    return url
