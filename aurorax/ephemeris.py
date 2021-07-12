import datetime
import pprint
import aurorax
from aurorax.sources import DataSource
from pydantic import BaseModel
from typing import Dict, List, Optional
from aurorax import Location
import humanize
from aurorax.requests import STANDARD_POLLING_SLEEP_TIME

class Ephemeris(BaseModel):
    """
    Ephemeris data type

    :param data_source: data source that the ephemeris record is associated with
    :type data_source: aurorax.sources.DataSource
    :param epoch: timestamp for the record in UTC
    :type epoch: datetime.datetime
    :param location_geo: latitude and longitude in geographic coordinates
    :type location_geo: Location
    :param location_gsm: latitude and longitude in GSM coordinates (leave empty for
                         data sources with a type of 'ground')
    :type location_gsm: Location
    :param nbtrace: north B-trace geomagnetic latitude and longitude
    :type nbtrace: Location
    :param sbtrace: south B-trace geomagnetic latitude and longitude
    :type sbtrace: Location
    :param metadata: metadata values for this record
    :type metadata: Dict
    """
    data_source: DataSource
    epoch: datetime.datetime
    location_geo: Location
    location_gsm: Location
    nbtrace: Location
    sbtrace: Location
    metadata: Dict

    def to_json_serializable(self) -> Dict:
        """
        Convert object to a JSON-serializable object (ie. translate datetime
        objects to strings)

        :return: dictionary JSON-serializable object
        :rtype: Dict
        """
        d = self.__dict__

        # format epoch as str
        if (type(d["epoch"]) is datetime.datetime):
            d["epoch"] = d["epoch"].strftime("%Y-%m-%dT%H:%M:00.000Z")

        # format location
        if (type(d["location_geo"]) is Location):
            d["location_geo"] = d["location_geo"].__dict__
        if (type(d["location_gsm"]) is Location):
            d["location_gsm"] = d["location_gsm"].__dict__
        if (type(d["nbtrace"]) is Location):
            d["nbtrace"] = d["nbtrace"].__dict__
        if (type(d["sbtrace"]) is Location):
            d["sbtrace"] = d["sbtrace"].__dict__

        # format metadata
        if (type(self.metadata) is dict):
            for key, value in self.metadata.items():
                if (type(value) is datetime.datetime or type(value) is datetime.date):
                    self.metadata[key] = self.metadata[key].strftime("%Y-%m-%dT%H:%M:%S.%f")
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

class Search():
    """
    Class representing an AuroraX ephemeris search
    """

    def __init__(self,
                 start: datetime.datetime,
                 end: datetime.datetime,
                 programs: List[str] = None,
                 platforms: List[str] = None,
                 instrument_types: List[str] = None,
                 metadata_filters: List[Dict] = None) -> None:
        """
        Create a new Search object

        :param start: start timestamp
        :type start: datetime
        :param end: end timestamp
        :type end: datetime
        :param programs: programs to search through, defaults to None
        :type programs: List[str], optional
        :param platforms: platforms to search through, defaults to None
        :type platforms: List[str], optional
        :param instrument_types: instrument types to search through, defaults to None
        :type instrument_types: List[str], optional
        :param metadata_filters: metadata keys and values to filter on, defaults to None
        :type metadata_filters: List[Dict], optional
        """
        self.request = None
        self.request_id = ""
        self.request_url = ""
        self.executed = False
        self.completed = False
        self.data_url = ""
        self.query = {}
        self.status = {}
        self.data: List[Ephemeris] = []
        self.logs = []

        self.start = start
        self.end = end
        self.programs = programs #[] if not programs else programs
        self.platforms = platforms #[] if not platforms else platforms
        self.instrument_types = instrument_types #[] if not instrument_types else instrument_types
        self.metadata_filters = metadata_filters #[] if not metadata_filters else metadata_filters

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

    def execute(self) -> None:
        """
        Initiate ephemeris search request
        """
        # set up request
        url = aurorax.api.urls.ephemeris_search_url
        post_data = {
            "data_sources": {
                "programs": [] if not self.programs else self.programs,
                "platforms": [] if not self.platforms else self.platforms,
                "instrument_types": [] if not self.instrument_types else self.instrument_types,
                "ephemeris_metadata_filters": [] if not self.metadata_filters else self.metadata_filters,
            },
            "start": self.start.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": self.end.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        self.query = post_data

        # do request
        req = aurorax.AuroraXRequest(method="post", url=url, body=post_data, null_response=True)
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
        Update the status of this ephemeris search request

        :param status: retrieved status (include to avoid requesting it from the API again), defaults to None
        :type status: Dict, optional
        """
        # get the status if it isn't passed in
        if (status is None):
            status = aurorax.requests.get_status(self.request_url)

        # update request status by checking if data URI is set
        if (status["search_result"]["data_uri"] is not None):
            self.completed = True
            self.data_url = "%s%s" % (aurorax.api.urls.base_url, status["search_result"]["data_uri"])

        # set class variable "status" and "logs"
        self.status = status
        self.logs = status["logs"]

    def check_for_data(self) -> None:
        """
        Check to see if data is available for this ephemeris search request
        """
        self.update_status()

    def get_data(self) -> None:
        """
        Retrieve the data available for this ephemeris search request
        """
        if (self.completed is False):
            print("No data available, update status first")
            return
        url = self.data_url
        raw_data = aurorax.requests.get_data(url)

        self.data = [Ephemeris(**e) for e in raw_data]

    def wait(self, poll_interval: float = STANDARD_POLLING_SLEEP_TIME, verbose: bool = False) -> None:
        """
        Block and wait for the request to complete and data is available for retrieval

        :param poll_interval: time in seconds to wait between polling
                              attempts, defaults to STANDARD_POLLING_SLEEP_TIME
        :type poll_interval: float, optional
        :param verbose: output poll times, defaults to False
        :type verbose: bool, optional
        """
        url = aurorax.api.urls.ephemeris_request_url.format(self.request_id)
        self.update_status(aurorax.requests.wait_for_data(url, poll_interval=poll_interval, verbose=verbose))


def search_async(start: datetime,
                 end: datetime,
                 programs: List[str] = None,
                 platforms: List[str] = None,
                 instrument_types: List[str] = None,
                 metadata_filters: List[Dict] = None) -> Search:
    """
    Submit a request for an ephemeris search, return asynchronously

    :param start: start timestamp
    :type start: datetime
    :param end: end timestamp
    :type end: datetime
    :param programs: programs to search through, defaults to []
    :type programs: List[str], optional
    :param platforms: platforms to search through, defaults to []
    :type platforms: List[str], optional
    :param instrument_types: instrument types to search through, defaults to []
    :type instrument_types: List[str], optional
    :param metadata_filters: metadata keys and values to filter on, defaults to []
    :type metadata_filters: List[Dict], optional

    :return: Search object
    :rtype: Search
    """
    s = aurorax.ephemeris.Search(start=start,
                                 end=end,
                                 programs=programs,
                                 platforms=platforms,
                                 instrument_types=instrument_types,
                                 metadata_filters=metadata_filters)
    s.execute()
    return s


def search(start: datetime,
           end: datetime,
           programs: List[str] = None,
           platforms: List[str] = None,
           instrument_types: List[str] = None,
           metadata_filters: List[Dict] = None,
           verbose: bool = False,
           poll_interval: float = STANDARD_POLLING_SLEEP_TIME) -> Search:
    """
    Search for ephemeris records

    :param start: start timestamp
    :type start: datetime
    :param end: end timestamp
    :type end: datetime
    :param programs: programs to search through, defaults to []
    :type programs: List[str], optional
    :param platforms: platforms to search through, defaults to []
    :type platforms: List[str], optional
    :param instrument_types: instrument types to search through, defaults to []
    :type instrument_types: List[str], optional
    :param metadata_filters: metadata keys and values to filter on, defaults to []
    :type metadata_filters: List[Dict], optional
    :param verbose: show the progress of the request using the request log, defaults to False
    :type verbose: bool, optional
    :param poll_interval: seconds to wait between polling calls, defaults to STANDARD_POLLING_SLEEP_TIME
    :type poll_interval: float, optional

    :return: Search object
    :rtype: Search
    """
    # create a Search() object
    s = Search(start=start, end=end, programs=programs, platforms=platforms, instrument_types=instrument_types, metadata_filters=metadata_filters)
    if (verbose is True):
        print("[%s] Search object created" % (datetime.datetime.now()))

    # execute the search
    s.execute()
    if (verbose is True):
        print("[%s] Request submitted" % (datetime.datetime.now()))
        print("[%s] Request ID: %s" % (datetime.datetime.now(), s.request_id))
        print("[%s] Request details available at: %s" % (datetime.datetime.now(), s.request_url))

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
        sources = {source.identifier: source for source in aurorax.sources.list()}
        if identifier not in sources.keys():
            raise aurorax.AuroraXValidationException(f"Data source with unique identifier {identifier} could not be found.")

        for record in records:
            # check the identifier, program name, platform name, and instrument type
            try:
                reference = sources[record.data_source.identifier]
            except KeyError:
                raise aurorax.AuroraXValidationException(f"Data source with unique identifier {record.data_source.identifier} could not be found.")

            if not (record.data_source.program == reference.program and 
                    record.data_source.platform == reference.platform and 
                    record.data_source.instrument_type == reference.instrument_type):
                return record

        return None

def upload(identifier: int, records: List[Ephemeris], validate_source: bool = False) -> int:
    """
    Upload ephemeris records to AuroraX

    :param identifier: data source ID
    :type identifier: int
    :param records: Ephemeris records to upload
    :type records: List[Ephemeris]
    :param validate_source: Set to True to validate all records before uploading. This will 
    :type validate_source: bool, optional

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected content error
    :raises aurorax.AuroraXUploadException: upload error
    :raises aurorax.AuroraXValidationException: data source validation error

    :return: 1 for success, raises exception on error
    :rtype: int
    """
    # validate record sources if the flag is set
    if validate_source:
        validation_error = __validate_data_source(identifier, records)
        if validation_error:
            raise aurorax.AuroraXValidationException("Unable to validate data source found in record: {}".format(validation_error))
    
    # translate each ephemeris record to a request-friendly dict (ie. convert datetimes to strings, etc.)
    for i, _ in enumerate(records):
        if (type(records[i]) is Ephemeris):
            records[i] = records[i].to_json_serializable()

    # make request
    url = aurorax.api.urls.ephemeris_upload_url.format(identifier)
    req = aurorax.AuroraXRequest(method="post", url=url, body=records, null_response=True)
    res = req.execute()

    # evaluate response
    if (res.status_code == 400):
        raise aurorax.AuroraXUploadException("%s - %s" % (res.data["error_code"], res.data["error_message"]))
    elif (res.status_code == 202):
        print("Status code 202, stream accepted")
    
    # return
    return 1

def delete(data_source: DataSource, start: datetime.datetime, end: datetime.datetime) -> int:
    """
    Delete a range of ephemeris records. This method is asynchronous.

    :param data_source: data source that the ephemeris record is associated with. Identifier, program, platform, and instrument_type are required.
    :type data_source: aurorax.sources.DataSource
    :param start: start datetime of deletion range
    :type start: datetime.datetime
    :param end: end datetime of deletion range
    :type end: datetime.datetime

    :raises aurorax.AuroraXMaxRetriesException: max retry error
    :raises aurorax.AuroraXUnexpectedContentTypeException: unexpected error
    :raises aurorax.AuroraXBadParametersException: invalid or missing parameters
    :raises aurorax.AuroraXNotFoundException: source not found
    :raises aurorax.AuroraXUnauthorizedException: invalid API key for this operation

    :return: 1 on success
    :rtype: int
    """
    if not all([data_source.identifier, data_source.program, data_source.platform, data_source.instrument_type]):
        raise aurorax.AuroraXBadParametersException("One or more required data source parameters are missing. Delete operation aborted.")

    # do request
    url = aurorax.api.urls.ephemeris_upload_url.format(data_source.identifier)
    params = {
        "program": data_source.program,
        "platform": data_source.platform,
        "instrument_type": data_source.instrument_type,
        "start": start.strftime("%Y-%m-%dT%H:%M:%S"),
        "end": end.strftime("%Y-%m-%dT%H:%M:%S")
    }
    delete_req = aurorax.AuroraXRequest(method="delete", url=url, body=params, null_response=True)
    res = delete_req.execute()

    # evaluate response
    if (res.status_code == 400):
        if type(res.data) is list:
            raise aurorax.AuroraXBadParametersException("%s - %s" % (res.status_code, res.data[0]["message"]))  
        raise aurorax.AuroraXBadParametersException("%s - %s" % (res.data["error_code"], res.data["error_message"]))
    elif (res.status_code == 404):
        raise aurorax.AuroraXNotFoundException("%s - %s" % (res.data["error_code"], res.data["error_message"]))

    # return
    return 1
    