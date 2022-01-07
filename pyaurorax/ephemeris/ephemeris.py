"""
Main functions for performing ephemeris searches
"""

import pyaurorax
import datetime
import humanize
from typing import Dict, List, Optional
from .classes.ephemeris import Ephemeris
from .classes.search import Search

# pdoc init
__pdoc__: Dict = {}


def __validate_data_source(identifier: int,
                           records: List[Ephemeris]) -> Optional[Ephemeris]:
    # get all current sources
    sources = {source.identifier: source for source in pyaurorax.sources.list()}
    if identifier not in sources.keys():
        raise pyaurorax.AuroraXValidationException(f"Data source with unique identifier "
                                                   "{identifier} could not be found.")

    # process each record to make sure the program/platform/instrument_type matches
    # the identifier found for the data source
    for record in records:
        # check the identifier, program name, platform name, and instrument type
        try:
            reference = sources[record.data_source.identifier]
        except KeyError:
            raise pyaurorax.AuroraXValidationException(f"Data source with unique identifier "
                                                       "{record.data_source.identifier} could "
                                                       "not be found.")

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
                 response_format: Optional[Dict] = None,
                 metadata_filters_logical_operator: Optional[str] = None) -> Search:
    """
    Submit a request for an ephemeris search, returns asynchronously

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

            e.g. {
                "key": "string",
                "operator": "=",
                "values": [
                    "string"
                ]
            }
        response_format: JSON representation of desired data response format

    Returns:
        A pyaurorax.ephemeris.Search object

    Raises:
        pyaurorax.exceptions.AuroraXBadParametersException: missing parameters
    """
    s = pyaurorax.ephemeris.Search(start=start,
                                   end=end,
                                   programs=programs,
                                   platforms=platforms,
                                   instrument_types=instrument_types,
                                   metadata_filters=metadata_filters,
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
           verbose: Optional[bool] = False,
           poll_interval: Optional[float] = pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME,
           response_format: Optional[Dict] = None,
           metadata_filters_logical_operator: Optional[str] = None) -> Search:
    """
    Search for ephemeris records

    Note: At least one search criteria from programs, platforms, or instrument_types
    must be specified.

    Args:
        start: start timestamp of the search (inclusive)
        end: end timestamp of the search (inclusive)
        programs: list of programs to search through, defaults to None
        platforms: list of platforms to search through, defaults to None
        instrument_types: list of instrument types to search through, defaults to None
        metadata_filters: list of dictionaries describing metadata keys and
            values to filter on, defaults to None

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
        A pyaurorax.ephemeris.Search object

    Raises:
        pyaurorax.exceptions.AuroraXBadParametersException: missing parameters
    """
    # create a Search() object
    s = Search(start=start,
               end=end,
               programs=programs,
               platforms=platforms,
               instrument_types=instrument_types,
               metadata_filters=metadata_filters,
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
           records: List[Ephemeris],
           validate_source: Optional[bool] = False) -> int:
    """
    Upload ephemeris records to AuroraX

    Args:
        identifier: AuroraX data source ID
        records: list of pyaurorax.ephemeris.Ephemeris records to upload
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
            raise pyaurorax.AuroraXValidationException("Unable to validate data source found "
                                                       "in record: {}".format(validation_error))

    # translate each ephemeris record to a request-friendly
    # dict (ie. convert datetimes to strings, etc.)
    for i, _ in enumerate(records):
        if (type(records[i]) is Ephemeris):
            records[i] = records[i].to_json_serializable()  # type: ignore

    # make request
    url = pyaurorax.api.urls.ephemeris_upload_url.format(identifier)
    req = pyaurorax.AuroraXRequest(method="post",
                                   url=url,
                                   body=records,
                                   null_response=True)
    res = req.execute()

    # evaluate response
    if (res.status_code == 400):
        raise pyaurorax.AuroraXUploadException("%s - %s" % (res.data["error_code"],
                                                            res.data["error_message"]))

    # return
    return 1


def delete(data_source: pyaurorax.sources.DataSource,
           start: datetime.datetime,
           end: datetime.datetime) -> int:
    """
    Delete a range of ephemeris records. This method is asynchronous.

    Args:
        data_source: pyaurorax.sources.DataSource source associated with
            the data product records. Identifier, program, platform, and
            instrument_type are required.
        start: timestamp marking beginning of range to delete records for, inclusive
        end: timestamp marking end of range to delete records for, inclusive

    Returns:
        1 on success

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
        pyaurorax.exceptions.AuroraXNotFoundException: source not found
        pyaurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation
        pyaurorax.exceptions.AuroraXBadParametersException: missing parameters
    """
    if not all([data_source.identifier, data_source.program, data_source.platform, data_source.instrument_type]):
        raise pyaurorax.AuroraXBadParametersException("One or more required data source parameters "
                                                      "are missing, delete operation aborted")

    # do request
    url = pyaurorax.api.urls.ephemeris_upload_url.format(data_source.identifier)
    params = {
        "program": data_source.program,
        "platform": data_source.platform,
        "instrument_type": data_source.instrument_type,
        "start": start.strftime("%Y-%m-%dT%H:%M:%S"),
        "end": end.strftime("%Y-%m-%dT%H:%M:%S")
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
        raise pyaurorax.AuroraXBadParametersException("%s - %s" % (res.data["error_code"],
                                                                   res.data["error_message"]))

    # return
    return 1
