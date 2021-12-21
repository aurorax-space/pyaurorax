"""
AuroraX holds ephemeris records for ground and space instruments in operation.
"""
import pyaurorax
import datetime
import humanize
import pprint
from pydantic import BaseModel
from typing import Dict, List, Optional, Union


class Ephemeris(BaseModel):
    """
    Ephemeris data type.

    Attributes:
        data_source: pyaurorax.sources.DataSource source that the ephemeris record is associated with.
        epoch: datetime.datetime timestamp for the record in UTC.
        location_geo: pyaurorax.Location object with latitude and longitude in geographic coordinates.
        location_gsm: pyaurorax.Location object with latitude and longitude in GSM coordinates (leave empty for
            data sources with a type of 'ground').
        nbtrace: pyaurorax.Location object with north B-trace geomagnetic latitude and longitude.
        sbtrace: pyaurorax.Location object with south B-trace geomagnetic latitude and longitude.
        metadata: dictionary containing metadata values for this record.

    """
    data_source: pyaurorax.sources.DataSource
    epoch: datetime.datetime
    location_geo: pyaurorax.Location
    location_gsm: pyaurorax.Location = pyaurorax.Location(lat=None, lon=None)
    nbtrace: pyaurorax.Location
    sbtrace: pyaurorax.Location
    metadata: Dict = None

    def to_json_serializable(self) -> Dict:
        """
        Convert object to a JSON-serializable object (ie. translate datetime objects to strings).

        Returns:
            Dictionary JSON-serializable object.

        """
        d = self.__dict__

        # format epoch as str
        if (type(d["epoch"]) is datetime.datetime):
            d["epoch"] = d["epoch"].strftime("%Y-%m-%dT%H:%M:00.000Z")

        # format location
        if (type(d["location_geo"]) is pyaurorax.Location):
            d["location_geo"] = d["location_geo"].__dict__
        if (type(d["location_gsm"]) is pyaurorax.Location):
            d["location_gsm"] = d["location_gsm"].__dict__
        if (type(d["nbtrace"]) is pyaurorax.Location):
            d["nbtrace"] = d["nbtrace"].__dict__
        if (type(d["sbtrace"]) is pyaurorax.Location):
            d["sbtrace"] = d["sbtrace"].__dict__

        # format metadata
        if (type(self.metadata) is dict):
            for key, value in self.metadata.items():
                if (type(value) is datetime.datetime or type(value) is datetime.date):
                    self.metadata[key] = self.metadata[key].strftime(
                        "%Y-%m-%dT%H:%M:%S.%f")
        if (type(self.metadata) is list):
            self.metadata = {}

        # format data source fields for query
        d["program"] = self.data_source.program
        d["platform"] = self.data_source.platform
        d["instrument_type"] = self.data_source.instrument_type
        del d["data_source"]

        # return
        return d

    def __str__(self) -> str:
        """
        String method.

        Returns:
            String format of Ephemeris.

        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation.

        Returns:
            Object representation of Ephemeris.

        """
        return pprint.pformat(self.__dict__)


class Search():
    """
    Class representing an AuroraX ephemeris search.

    At least one search criteria from programs, platforms, instrument_types, or metadata_filters
    must be specified.

    start: start datetime.datetime timestamp of the search.
    end: end datetime.datetime timestamp of the search.
    programs: list of program names to search.
    platforms: list of platform names to search.
    instrument_types: list of instrument types to search.
    metadata_filters: list of dictionaries describing metadata keys and values to filter on, defaults to None.
        e.g. {
            "key": "string",
            "operator": "=",
            "values": [
                "string"
            ]
        }
    response_format: JSON representation of desired data response format.
    request: pyaurorax.AuroraXResponse object returned when the search is executed.
    request_id: unique AuroraX string ID assigned to the request.
    request_url: unique AuroraX URL string assigned to the request.
    executed: boolean, gets set to True when the search is executed.
    completed: boolean, gets set to True when the search is checked to be finished.
    data_url: URL string where data is accessed.
    query: dictionary of values sent for the search query.
    status: dictionary of status updates.
    data: list of pyaurorax.ephemeris.Ephemeris objects returned, or a list of raw JSON results
        if response_format is specified.
    logs: list of logging messages from the API.
    """

    def __init__(self,
                 start: datetime.datetime,
                 end: datetime.datetime,
                 programs: List[str] = None,
                 platforms: List[str] = None,
                 instrument_types: List[str] = None,
                 metadata_filters: List[Dict] = None,
                 response_format: Dict = None,
                 metadata_filters_logical_operator: str = "AND"
                 ) -> None:
        """
        Create a new Search object.

        """
        self.request = None
        self.request_id = ""
        self.request_url = ""
        self.executed = False
        self.completed = False
        self.data_url = ""
        self.query = {}
        self.status = {}
        self.data: List[Union[Ephemeris, Dict]] = []
        self.logs = []

        self.start = start
        self.end = end
        self.programs = programs
        self.platforms = platforms
        self.instrument_types = instrument_types
        self.metadata_filters = metadata_filters
        self.metadata_filters_logical_operator = metadata_filters_logical_operator
        self.response_format = response_format

    def __str__(self) -> str:
        """
        String method.

        Returns:
            String format of Ephemeris Search object.

        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation.

        Returns:
            Object representation of Ephemeris Search object.

        """
        return pprint.pformat(self.__dict__)

    def execute(self) -> None:
        """
        Initiate ephemeris search request.

        Raises:
            pyaurorax.exceptions.AuroraXBadParametersException: missing parameters.

        """
        # check for at least one filter criteria
        if not (self.programs or self.platforms or self.instrument_types or self.metadata_filters):
            raise pyaurorax.AuroraXBadParametersException(
                "At least one filter criteria parameter besides Start and End must be specified.")

        # set up request
        url = pyaurorax.api.urls.ephemeris_search_url
        post_data = {
            "data_sources": {
                "programs": [] if not self.programs else self.programs,
                "platforms": [] if not self.platforms else self.platforms,
                "instrument_types": [] if not self.instrument_types else self.instrument_types,
                "ephemeris_metadata_filters": {} if not self.metadata_filters
                else {
                    "logical_operator": self.metadata_filters_logical_operator,
                    "expressions": self.metadata_filters
                },
            },
            "start": self.start.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": self.end.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        self.query = post_data

        # do request
        req = pyaurorax.AuroraXRequest(
            method="post", url=url, body=post_data, null_response=True)
        res = req.execute()

        # set request ID, request_url, executed
        self.executed = True
        if (res.status_code == 202):
            # request successfully dispatched
            self.executed = True
            self.request_url = res.request.headers["location"]
            self.request_id = self.request_url.rsplit("/", 1)[-1]
        self.request = res

    def update_status(self, status: Dict = None) -> None:
        """
        Update the status of this ephemeris search request.

        Attributes:
            status: retrieved status dictionary (include to avoid requesting it from the API again), defaults to None.
        """
        # get the status if it isn't passed in
        if (status is None):
            status = pyaurorax.requests.get_status(self.request_url)

        # update request status by checking if data URI is set
        if (status["search_result"]["data_uri"] is not None):
            self.completed = True
            self.data_url = "%s%s" % (
                pyaurorax.api.urls.base_url, status["search_result"]["data_uri"])

        # set class variable "status" and "logs"
        self.status = status
        self.logs = status["logs"]

    def check_for_data(self) -> bool:
        """
        Check to see if data is available for this ephemeris search request.

        Returns:
            True if data is available, else False.
        """
        self.update_status()

        return self.completed

    def get_data(self) -> None:
        """
        Retrieve the data available for this ephemeris search request.
        """
        if (self.completed is False):
            print("No data available, update status or check for data first")
            return
        url = self.data_url
        raw_data = pyaurorax.requests.get_data(
            url, post_body=self.response_format)

        if self.response_format is not None:
            self.data = raw_data
        else:
            self.data = [Ephemeris(**e) for e in raw_data]

    def wait(self, poll_interval: float = pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME, verbose: bool = False) -> None:
        """
        Block and wait for the request to complete and data is available for retrieval.

        Attributes:
            poll_interval: time in seconds to wait between polling attempts,
                defaults to pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME.
            verbose: output poll times, defaults to False.

        """
        url = pyaurorax.api.urls.ephemeris_request_url.format(self.request_id)
        self.update_status(pyaurorax.requests.wait_for_data(
            url, poll_interval=poll_interval, verbose=verbose))

    def cancel(self, wait: bool = False, verbose: bool = False,
               poll_interval: float = pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME) -> int:
        """
        Cancel the ephemeris search request at the API. This method returns asynchronously by default.

        Attributes:
            wait: set to True to block until the cancellation request has been completed. This may take several minutes.
            verbose: when wait=True, output poll times, defaults to False.
            poll_interval: when wait=True, seconds to wait between polling calls, defaults to STANDARD_POLLING_SLEEP_TIME.

        Returns:
            1 on success.

        Raises:
            pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error.
            pyaurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation.

        """
        url = pyaurorax.api.urls.ephemeris_request_url.format(self.request_id)
        return pyaurorax.requests.cancel(url, wait=wait, poll_interval=poll_interval, verbose=verbose)


def search_async(start: datetime.datetime,
                 end: datetime.datetime,
                 programs: List[str] = None,
                 platforms: List[str] = None,
                 instrument_types: List[str] = None,
                 metadata_filters: List[Dict] = None,
                 response_format: Dict = None,
                 metadata_filters_logical_operator: str = None) -> Search:
    """
    Submit a request for an ephemeris search, return asynchronously.

    At least one search criteria from programs, platforms, instrument_types, or metadata_filters
    must be specified.

    Attributes:
        start: start datetime.datetime timestamp of the search.
        end: end datetime.datetime timestamp of the search.
        programs: list of programs to search through, defaults to None.
        platforms: list of platforms to search through, defaults to None.
        instrument_types: list of instrument types to search through, defaults to None.
        metadata_filters: list of dictionaries describing metadata keys and values to filter on, defaults to None.
            e.g. {
                "key": "string",
                "operator": "=",
                "values": [
                    "string"
                ]
            }
        response_format: JSON representation of desired data response format.

    Returns:
        A pyaurorax.ephemeris.Search object.

    Raises:
        pyaurorax.exceptions.AuroraXBadParametersException: missing parameters.

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
           programs: List[str] = None,
           platforms: List[str] = None,
           instrument_types: List[str] = None,
           metadata_filters: List[Dict] = None,
           verbose: bool = False,
           poll_interval: float = pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME,
           response_format: Dict = None,
           metadata_filters_logical_operator: str = None) -> Search:
    """
    Search for ephemeris records.

    At least one search criteria from programs, platforms, instrument_types, or metadata_filters
    must be specified.

    Attributes:
        start: start datetime.datetime timestamp of the search.
        end: end datetime.datetime timestamp of the search.
        programs: list of programs to search through, defaults to None.
        platforms: list of platforms to search through, defaults to None.
        instrument_types: list of instrument types to search through, defaults to None.
        metadata_filters: list of dictionaries describing metadata keys and values to filter on, defaults to None.
            e.g. {
                "key": "string",
                "operator": "=",
                "values": [
                    "string"
                ]
            }
        verbose: output poll times, defaults to False.
        poll_interval: time in seconds to wait between polling attempts,
            defaults to pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME.
        response_format: JSON representation of desired data response format.

    Returns:
        A pyaurorax.ephemeris.Search object.

    Raises:
        pyaurorax.exceptions.AuroraXBadParametersException: missing parameters

    """
    # create a Search() object
    s = Search(start=start, end=end, programs=programs, platforms=platforms,
               instrument_types=instrument_types, metadata_filters=metadata_filters, response_format=response_format,
               metadata_filters_logical_operator=metadata_filters_logical_operator)
    if (verbose is True):
        print("[%s] Search object created" % (datetime.datetime.now()))

    # execute the search
    s.execute()
    if (verbose is True):
        print("[%s] Request submitted" % (datetime.datetime.now()))
        print("[%s] Request ID: %s" % (datetime.datetime.now(), s.request_id))
        print("[%s] Request details available at: %s" %
              (datetime.datetime.now(), s.request_url))

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


def __validate_data_source(identifier: int, records: List[Ephemeris]) -> Optional[Ephemeris]:
    # get all current sources
    sources = {source.identifier: source for source in pyaurorax.sources.list()}
    if identifier not in sources.keys():
        raise pyaurorax.AuroraXValidationException(
            f"Data source with unique identifier {identifier} could not be found.")

    for record in records:
        # check the identifier, program name, platform name, and instrument type
        try:
            reference = sources[record.data_source.identifier]
        except KeyError:
            raise pyaurorax.AuroraXValidationException(
                f"Data source with unique identifier {record.data_source.identifier} could not be found.")

        if not (record.data_source.program == reference.program
                and record.data_source.platform == reference.platform
                and record.data_source.instrument_type == reference.instrument_type):
            return record

    return None


def upload(identifier: int, records: List[Ephemeris], validate_source: bool = False) -> int:
    """
    Upload ephemeris records to AuroraX.

    Attributes:
        identifier: AuroraX data source ID int.
        records: list of pyaurorax.ephemeris.Ephemeris records to upload.
        validate_source: boolean, set to True to validate all records before uploading.

    Returns:
        1 for success, raises exception on error.

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error.
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected content error.
        pyaurorax.exceptions.AuroraXUploadException: upload error.
        pyaurorax.exceptions.AuroraXValidationException: data source validation error.

    """
    # validate record sources if the flag is set
    if validate_source:
        validation_error = __validate_data_source(identifier, records)
        if validation_error:
            raise pyaurorax.AuroraXValidationException(
                "Unable to validate data source found in record: {}".format(validation_error))

    # translate each ephemeris record to a request-friendly dict (ie. convert datetimes to strings, etc.)
    for i, _ in enumerate(records):
        if (type(records[i]) is Ephemeris):
            records[i] = records[i].to_json_serializable()

    # make request
    url = pyaurorax.api.urls.ephemeris_upload_url.format(identifier)
    req = pyaurorax.AuroraXRequest(
        method="post", url=url, body=records, null_response=True)
    res = req.execute()

    # evaluate response
    if (res.status_code == 400):
        raise pyaurorax.AuroraXUploadException(
            "%s - %s" % (res.data["error_code"], res.data["error_message"]))

    # return
    return 1


def delete(data_source: pyaurorax.sources.DataSource, start: datetime.datetime, end: datetime.datetime) -> int:
    """
    Delete a range of ephemeris records. This method is asynchronous.

    Attributes:
        data_source: pyaurorax.sources.DataSource source associated with the data product records.
            Identifier, program, platform, and instrument_type are required.
        start: datetime.datetime beginning of range to delete records for, inclusive.
        end: datetime.datetime end of datetime range to delete records for, inclusive.

    Returns:
        1 on success.

    Raises:
        pyaurorax.exceptions.AuroraXMaxRetriesException: max retry error.
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error.
        pyaurorax.exceptions.AuroraXNotFoundException: source not found.
        pyaurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation.
        pyaurorax.exceptions.AuroraXBadParametersException: missing parameters.

    """
    if not all([data_source.identifier, data_source.program, data_source.platform, data_source.instrument_type]):
        raise pyaurorax.AuroraXBadParametersException(
            "One or more required data source parameters are missing. Delete operation aborted.")

    # do request
    url = pyaurorax.api.urls.ephemeris_upload_url.format(
        data_source.identifier)
    params = {
        "program": data_source.program,
        "platform": data_source.platform,
        "instrument_type": data_source.instrument_type,
        "start": start.strftime("%Y-%m-%dT%H:%M:%S"),
        "end": end.strftime("%Y-%m-%dT%H:%M:%S")
    }
    delete_req = pyaurorax.AuroraXRequest(
        method="delete", url=url, body=params, null_response=True)
    res = delete_req.execute()

    # evaluate response
    if (res.status_code == 400):
        if type(res.data) is list:
            raise pyaurorax.AuroraXBadParametersException(
                "%s - %s" % (res.status_code, res.data[0]["message"]))
        raise pyaurorax.AuroraXBadParametersException(
            "%s - %s" % (res.data["error_code"], res.data["error_message"]))

    # return
    return 1
