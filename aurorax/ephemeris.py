import aurorax as _aurorax
import datetime as _datetime
import time as _time
import humanize as _humanize
import pprint as _pprint
from typing import List as _List
from typing import Dict as _Dict
from .location import Location as _Location
from .requests import STANDARD_POLLING_SLEEP_TIME as _STANDARD_POLLING_SLEEP_TIME


class Ephemeris():
    """
    Class representing an AuroraX ephemeris record
    """

    def __init__(self, identifier: int, program: str, platform: str, instrument_type: str,
                 epoch: _datetime, location_geo: _Location, location_gsm: _Location,
                 nbtrace: _Location, sbtrace: _Location, metadata: _Dict) -> None:
        """
        Constructor

        :param identifier: data source ID
        :type identifier: int
        :param program: program name
        :type program: str
        :param platform: platform name
        :type platform: str
        :param instrument_type: instrument type name
        :type instrument_type: str
        :param epoch: timestamp for the record in UTC
        :type epoch: datetime
        :param location_geo: latitude and longitude in geographic coordinates
        :type location_geo: Location
        :param location_gsm: latitude and longitude in GSM coordinates (leave empty for
                             data sources with a type of 'ground')
        :type location_gsm: Location
        :param nbtrace: north B-trace geomagnetic latitude and longitude
        :type nbtrace: Location
        :param sbtrace: south B-trace geomagnetic latitude and longitude
        :type sbtrace: Location
        :param metdata: metadata values for this record
        :type metdata: Dict
        """
        self.identifier = identifier
        self.program = program
        self.platform = platform
        self.instrument_type = instrument_type
        self.epoch = epoch
        self.location_geo = location_geo
        self.location_gsm = location_gsm
        self.nbtrace = nbtrace
        self.sbtrace = sbtrace
        self.metadata = metadata

    def to_json_serializable(self) -> _Dict:
        """
        Convert object to a JSON-serializable object (ie. translate datetime
        objects to strings)

        :return: dictionary JSON-serializable object
        :rtype: Dict
        """
        d = self.__dict__

        # format epoch as str
        if (type(d["epoch"]) is _datetime.datetime):
            d["epoch"] = d["epoch"].strftime("%Y-%m-%dT%H:%M:00.000Z")

        # format location
        if (type(d["location_geo"]) is _Location):
            d["location_geo"] = d["location_geo"].__dict__
        if (type(d["location_gsm"]) is _Location):
            d["location_gsm"] = d["location_gsm"].__dict__
        if (type(d["nbtrace"]) is _Location):
            d["nbtrace"] = d["nbtrace"].__dict__
        if (type(d["sbtrace"]) is _Location):
            d["sbtrace"] = d["sbtrace"].__dict__

        # format metadata
        if (type(self.metadata) is dict):
            for key, value in self.metadata.items():
                if (type(value) is _datetime.datetime or type(value) is _datetime.date):
                    self.metadata[key] = self.metadata[key].strftime("%Y-%m-%dT%H:%M:%S.%f")
        if (type(self.metadata) is list):
            self.metadata = {}

        # return
        return d

    def __str__(self) -> str:
        """String method

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
        return _pprint.pformat(self.__dict__)


class Search():
    """
    Class representing an AuroraX ephemeris search
    """

    def __init__(self, start_dt: _datetime, end_dt: _datetime, programs: _List = [], platforms: _List = [],
                 instrument_types: _List = [], metadata_filters: _List = []) -> None:
        """
        Create a new Search object

        :param start_dt: start timestamp
        :type start_dt: datetime
        :param end_dt: end timestamp
        :type end_dt: datetime
        :param programs: programs to search through, defaults to []
        :type programs: List, optional
        :param platforms: platforms to search through, defaults to []
        :type platforms: List, optional
        :param instrument_types: instrument types to search through, defaults to []
        :type instrument_types: List, optional
        :param metadata_filters: metadata keys and values to filter on, defaults to []
        :type metadata_filters: List, optional
        """
        self.request = None
        self.request_id = ""
        self.request_url = ""
        self.executed = False
        self.data_available = False
        self.data_url = ""
        self.query = {}
        self.status = {}
        self.data = []
        self.logs = []

        self.start_dt = start_dt
        self.end_dt = end_dt
        self.programs = programs
        self.platforms = platforms
        self.instrument_types = instrument_types
        self.metadata_filters = metadata_filters

    def __str__(self) -> str:
        """String method

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
        return _pprint.pformat(self.__dict__)

    def execute(self) -> None:
        """
        Initiate ephemeris search request
        """
        # send request
        url = _aurorax.api.URL_EPHEMERIS_SEARCH
        post_data = {
            "data_sources": {
                "programs": self.programs,
                "platforms": self.platforms,
                "instrument_types": self.instrument_types,
                "ephemeris_metadata_filters": self.metadata_filters,
            },
            "start": self.start_dt.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": self.end_dt.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        self.query = post_data
        req = _aurorax.AuroraXRequest(url, method="POST", json=post_data)
        res = req.execute()

        # set request ID, request_url, executed
        self.executed = True
        if (res.status_code == 202):
            # request successfully dispatched
            self.executed = True
            self.request_url = res.headers["location"]
            self.request_id = self.request_url.rsplit("/", 1)[-1]
        self.request = res

    def update_status(self, status: _Dict = None) -> None:
        """
        Update the status of this ephemeris search request

        :param status: retrieved status (include to avoid requesting it from the API again), defaults to None
        :type status: Dict, optional
        """
        # get the status if it isn't passed in
        if (status is None):
            status = get_request_status(self.request_id)

        # update request status by checking if data URI is set
        if (status["request_status"]["completed"] is True):
            self.data_available = True
            self.data_url = status["request_status"]["data_url"]

        # set class variable "status" and "logs"
        self.status = status
        if (status["status_code"] == 200):
            self.logs = status["data"]["logs"]

    def check_for_data(self) -> None:
        """
        Check to see if data is available for this ephemeris search request
        """
        self.update_status()

    def get_data(self) -> None:
        """
        Retrieve the data available for this ephemeris search request
        """
        if (self.data_url == ""):
            print("No data available, update status first")
            return
        url = self.data_url
        data_res = get_request_data(self.request_id, url=url)
        self.data = data_res["data"]

    def wait(self, poll_interval: float = _STANDARD_POLLING_SLEEP_TIME) -> None:
        """
        Block and wait for the request to complete and data is available for retrieval

        :param poll_interval: time in seconds to wait between polling
                              attempts, defaults to STANDARD_POLLING_SLEEP_TIME
        :type poll_interval: float, optional
        """
        url = _aurorax.api.URL_EPHEMERIS_REQUEST_STATUS.format(self.request_id)
        self.update_status(_aurorax.requests.wait_for_data(url, poll_interval=poll_interval))


def get_metadata_schema(identifier: int) -> _List:
    """
    Get ephemeris metadata schema for a specified data source identifier

    :param identifier: data source ID
    :type identifier: int

    :return: metadata schema
    :rtype: List
    """
    return _aurorax.metadata.get_ephemeris_schema(identifier)


def get_request_status(request_id: str) -> _Dict:
    """
    Retrieve the request status for a given ephemeris search request ID

    :param request_id: ephemeris search request ID
    :type request_id: str

    :return: status response
    :rtype: Dict
    """
    url = _aurorax.api.URL_EPHEMERIS_REQUEST_STATUS.format(request_id)
    return _aurorax.requests.get_status(url)


def get_request_data(request_id: str, url: str = None) -> _Dict:
    """
    Retrieve the request data for a given ephemeris search request ID

    :param request_id: ephemeris search request ID
    :type request_id: str
    :param url: request data URL, optional (derived if not specified)
    :type url: str, optional

    :return: data response
    :rtype: Dict
    """
    if (url is None):
        url = "%s/data" % (_aurorax.api.URL_EPHEMERIS_REQUEST_STATUS.format(request_id))
    return _aurorax.requests.get_data(url)


def get_request_logs(request_id: str) -> _Dict:
    """
    Retrieve the request logs for a given ephemeris search request ID

    :param request_id: ephemeris search request ID
    :type request_id: str

    :return: logs response
    :rtype: Dict
    """
    url = _aurorax.api.URL_EPHEMERIS_REQUEST_STATUS.format(request_id)
    return _aurorax.requests.get_logs(url)


def wait_for_data(request_id: str, poll_interval: float = _STANDARD_POLLING_SLEEP_TIME) -> _Dict:
    """
    Block and wait for the data to be made available for a given ephemeris search request ID

    :param request_id: ephemeris search request ID
    :type request_id: str
    :param poll_interval: time in seconds to wait between polling
                          attempts, defaults to STANDARD_POLLING_SLEEP_TIME
    :type poll_interval: float, optional

    :return: status response
    :rtype: Dict
    """
    url = _aurorax.api.URL_EPHEMERIS_REQUEST_STATUS.format(request_id)
    return _aurorax.requests.wait_for_data(url, poll_interval=poll_interval)


def search_async(start_dt: _datetime, end_dt: _datetime, programs: _List = [], platforms: _List = [],
                 instrument_types: _List = [], metadata_filters: _List = [],
                 show_progress: bool = False) -> _Dict:
    """
    Submit a request for an ephemeris search

    :param start_dt: start timestamp
    :type start_dt: datetime
    :param end_dt: end timestamp
    :type end_dt: datetime
    :param programs: programs to search through, defaults to []
    :type programs: List, optional
    :param platforms: platforms to search through, defaults to []
    :type platforms: List, optional
    :param instrument_types: instrument types to search through, defaults to []
    :type instrument_types: List, optional
    :param metadata_filters: metadata keys and values to filter on, defaults to []
    :type metadata_filters: List, optional
    :param show_progress: show the progress of the request using the request log, defaults to False
    :type show_progress: bool, optional

    :return: request response
    :rtype: Dict
    """
    return search(start_dt,
                  end_dt,
                  programs=programs,
                  platforms=platforms,
                  instrument_types=instrument_types,
                  metadata_filters=metadata_filters,
                  show_progress=show_progress,
                  async_return=True)


def search(start_dt: _datetime, end_dt: _datetime, programs: _List = [], platforms: _List = [],
           instrument_types: _List = [], metadata_filters: _List = [], show_progress: bool = False,
           async_return: bool = False, poll_interval: float = _STANDARD_POLLING_SLEEP_TIME) -> _Dict:
    """
    Search for ephemeris records

    :param start_dt: start timestamp
    :type start_dt: datetime
    :param end_dt: end timestamp
    :type end_dt: datetime
    :param programs: programs to search through, defaults to []
    :type programs: List, optional
    :param platforms: platforms to search through, defaults to []
    :type platforms: List, optional
    :param instrument_types: instrument types to search through, defaults to []
    :type instrument_types: List, optional
    :param metadata_filters: metadata keys and values to filter on, defaults to []
    :type metadata_filters: List, optional
    :param show_progress: show the progress of the request using the request log, defaults to False
    :type show_progress: bool, optional
    :param async_return: return immediately after sending the request, don't wait for data, defaults to False
    :type async_return: bool, optional
    :param poll_interval: seconds to wait between polling calls, defaults to STANDARD_POLLING_SLEEP_TIME
    :type poll_interval: float, optional

    :return: ephemeris data response; or request response if "async_return" is True
    :rtype: Dict
    """
    # init return dict
    return_dict = {
        "status_code": None,
        "data": [],
    }

    # create a Search() object
    s = Search(start_dt, end_dt, programs, platforms, instrument_types, metadata_filters)
    if (show_progress is True):
        print("[%s] Search object created" % (_datetime.datetime.now()))

    # execute the search
    s.execute()
    if (show_progress is True):
        if (s.executed is True):
            print("[%s] Request submitted" % (_datetime.datetime.now()))
            print("[%s] Request ID: %s" % (_datetime.datetime.now(), s.request_id))
            print("[%s] Request details available at: %s" % (_datetime.datetime.now(), s.request_url))
        else:
            print("[%s] Request failed to submit" % (_datetime.datetime.now()))
            return_dict["status_code"] = s.request.status_code
            return_dict["search_object"] = s
            return return_dict

    # check if async return is specified
    if (async_return is True):
        return_dict["status_code"] = s.request.status_code
        return_dict["search_object"] = s
        if (show_progress is True):
            print("[%s] Async return specified, returning immediately" % (_datetime.datetime.now()))
        return return_dict

    # check the request URL for the status of the request (poll for data)
    first_followup = True
    while (s.data_available is False):
        if (first_followup is True):
            _time.sleep(_aurorax.requests.FIRST_FOLLOWUP_SLEEP_TIME)
            first_followup = False
        else:
            _time.sleep(poll_interval)
        if (show_progress is True):
            print("[%s] Checking for data ..." % (_datetime.datetime.now()))
        s.check_for_data()

    # get the data
    if (show_progress is True):
        print("[%s] Request has data available, retrieving it ..." % (_datetime.datetime.now()))
    s.get_data()

    # return response with the data
    return_dict["status_code"] = s.request.status_code
    return_dict["search_object"] = s
    return_dict["data"] = s.data
    if (show_progress is True):
        print("[%s] Retrieved %s of data containing %d records, completed "
              "search request" % (_datetime.datetime.now(),
                                  _humanize.filesize.naturalsize(s.status["data"]["search_result"]["file_size"]),
                                  s.status["data"]["search_result"]["result_count"]))
    return return_dict


def upload(api_key: str, identifier: int, records: _List["Ephemeris"]) -> _Dict:
    """
    Upload ephemeris records to AuroraX

    :param api_key: AuroraX API key
    :type api_key: str
    :param identifier: data source ID
    :type identifier: int
    :param records: Ephemeris records to upload
    :type records: List[Ephemeris]

    :return: upload response
    :rtype: Dict
    """
    # translate each ephemeris record to a request-friendly dict (ie. convert datetimes to strings, etc.)
    for i, record in enumerate(records):
        if (type(records[i]) is Ephemeris):
            records[i] = records[i].to_json_serializable()

    # make request
    url = _aurorax.api.URL_EPHEMERIS_UPLOAD.format(identifier)
    req = _aurorax.AuroraXRequest(url, method="POST", json=records, api_key=api_key)
    res = req.execute()

    # set dict to return
    return_dict = {
        "status_code": res.status_code,
        "data": {},
    }
    if (res.status_code == 400):
        return_dict["data"] = res.data

    # return
    return return_dict
