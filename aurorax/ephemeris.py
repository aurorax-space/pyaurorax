import datetime
import time
import humanize
from pprint import pformat
from typing import List, Dict
from .api import URL_EPHEMERIS_SEARCH, URL_EPHEMERIS_REQUEST_STATUS
from .api import URL_EPHEMERIS_UPLOAD
from .api import AuroraXRequest
from .requests import get_status as request_get_status
from .requests import get_data as request_get_data
from .requests import get_logs as request_get_logs
from .requests import wait_for_data as request_wait_for_data
from .requests import STANDARD_POLLING_SLEEP_TIME, FIRST_FOLLOWUP_SLEEP_TIME
from .location import Location


class Ephemeris():
    """
    Class representing an AuroraX ephemeris record
    """

    def __init__(self, identifier: int, program: str, platform: str, instrument_type: str,
                 epoch: datetime, location_geo: Location, location_gsm: Location, nbtrace: Location,
                 sbtrace: Location, metadata: Dict) -> None:
        """
        Constructor

        :param identifier: ephemeris source ID
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
                             ephemeris sources with a type of 'ground')
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

    def to_json_serializable(self) -> Dict:
        """
        Convert object to a JSON-serializable object (ie. translate datetime
        objects to strings)

        :return: dictionary JSON-serializable object
        :rtype: Dict
        """
        d = self.__dict__
        d["epoch"] = d["epoch"].strftime("%Y-%m-%dT%H:%M:00.000Z")
        d["location_geo"] = d["location_geo"].__dict__
        d["location_gsm"] = d["location_gsm"].__dict__
        d["nbtrace"] = d["nbtrace"].__dict__
        d["sbtrace"] = d["sbtrace"].__dict__
        return d

    def __str__(self) -> str:
        """String method

        :return: string format
        :rtype: str
        """
        return pformat(self.__dict__)

    def __repr__(self) -> str:
        """
        Object representation

        :return: object representation
        :rtype: str
        """
        return self.__str__()


class Search():
    """
    Class representing an AuroraX ephemeris search
    """

    def __init__(self, start_dt: datetime, end_dt: datetime, programs: List = [], platforms: List = [],
                 instrument_types: List = [], metadata_filters: List = []) -> None:
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

    def execute(self) -> None:
        """
        Initiate ephemeris search request
        """
        # send request
        url = URL_EPHEMERIS_SEARCH
        post_data = {
            "ephemeris_sources": {
                "programs": self.programs,
                "platforms": self.platforms,
                "instrument_types": self.instrument_types,
            },
            "metadata_filters": self.metadata_filters,
            "start": self.start_dt.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": self.end_dt.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        self.query = post_data
        req = AuroraXRequest(url, method="POST", json=post_data)
        res = req.execute()

        # set request ID, request_url, executed
        self.executed = True
        if (res.status_code == 202):
            # request successfully dispatched
            self.executed = True
            self.request_url = res.headers["location"]
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

    def wait_for_data(self, poll_interval: float = STANDARD_POLLING_SLEEP_TIME) -> None:
        """
        Block and wait for the request to complete and data is available for retrieval

        :param poll_interval: time in seconds to wait between polling
                              attempts, defaults to STANDARD_POLLING_SLEEP_TIME
        :type poll_interval: float, optional
        """
        url = URL_EPHEMERIS_REQUEST_STATUS.format(self.request_id)
        self.update_status(request_wait_for_data(url))


def get_request_status(request_id: str) -> Dict:
    """
    Retrieve the request status for a given ephemeris search request ID

    :param request_id: ephemeris search request ID
    :type request_id: str

    :return: status response
    :rtype: Dict
    """
    url = URL_EPHEMERIS_REQUEST_STATUS.format(request_id)
    return request_get_status(url)


def get_request_data(request_id: str, url: str = None) -> Dict:
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
        url = "%s/data" % (URL_EPHEMERIS_REQUEST_STATUS.format(request_id))
    return request_get_data(url)


def get_request_logs(request_id: str) -> Dict:
    """
    Retrieve the request logs for a given ephemeris search request ID

    :param request_id: ephemeris search request ID
    :type request_id: str

    :return: logs response
    :rtype: Dict
    """
    url = URL_EPHEMERIS_REQUEST_STATUS.format(request_id)
    return request_get_logs(url)


def wait_for_data(request_id: str) -> Dict:
    """
    Block and wait for the data to be made available for a given ephemeris search request ID

    :param request_id: ephemeris search request ID
    :type request_id: str

    :return: status response
    :rtype: Dict
    """
    url = URL_EPHEMERIS_REQUEST_STATUS.format(request_id)
    return request_wait_for_data(url)


def search(start_dt: datetime, end_dt: datetime, programs: List = [], platforms: List = [],
           instrument_types: List = [], metadata_filters: List = [], show_progress: bool = False,
           async_return: bool = False, poll_interval: float = STANDARD_POLLING_SLEEP_TIME) -> Dict:
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
        "search_object": None,
        "data": [],
    }

    # create a Search() object
    s = Search(start_dt, end_dt, programs, platforms, instrument_types, metadata_filters)
    if (show_progress is True):
        print("[%s] Search object created" % (datetime.datetime.now()))

    # execute the search
    s.execute()
    if (show_progress is True):
        if (s.executed is True):
            print("[%s] Request submitted" % (datetime.datetime.now()))
            print("[%s] Request ID: %s" % (datetime.datetime.now(), s.request_id))
            print("[%s] Request details available at: %s" % (datetime.datetime.now(), s.request_url))
        else:
            print("[%s] Request failed to submit" % (datetime.datetime.now()))
            return_dict["status_code"] = s.request.status_code
            return_dict["search_object"] = s
            return return_dict

    # check if async return is specified
    if (async_return is True):
        return_dict["status_code"] = s.request.status_code
        return_dict["search_object"] = s
        if (show_progress is True):
            print("[%s] Async return specified, returning immediately" % (datetime.datetime.now()))
        return return_dict

    # check the request URL for the status of the request (poll for data)
    first_followup = True
    while (s.data_available is False):
        if (first_followup is True):
            time.sleep(FIRST_FOLLOWUP_SLEEP_TIME)
            first_followup = False
        else:
            time.sleep(poll_interval)
        if (show_progress is True):
            print("[%s] Checking for data ..." % (datetime.datetime.now()))
        s.check_for_data()

    # get the data
    if (show_progress is True):
        print("[%s] Request has data available, retrieving it ..." % (datetime.datetime.now()))
    s.get_data()

    # return response with the data
    return_dict["status_code"] = s.request.status_code
    return_dict["search_object"] = s
    return_dict["data"] = s.data
    if (show_progress is True):
        print("[%s] Retrieved %s of data containing %d records, completed "
              "search request" % (datetime.datetime.now(),
                                  humanize.filesize.naturalsize(s.status["data"]["search_result"]["file_size"]),
                                  s.status["data"]["search_result"]["result_count"]))
    return return_dict


def upload(api_key: str, identifier: int, records: List["Ephemeris"]) -> Dict:
    """
    Upload ephemeris records to AuroraX

    :param api_key: AuroraX API key
    :type api_key: str
    :param identifier: ephemeris source ID
    :type identifier: int
    :param records: Ephemeris records to upload
    :type records: List[Ephemeris]

    :return: upload response
    :rtype: Dict
    """
    # translate each ephemeris record to a request-friendly dict (ie. convert datetimes to strings)
    for i, record in enumerate(records):
        records[i] = records[i].to_request_format()

    # make request
    url = URL_EPHEMERIS_UPLOAD.format(identifier)
    req = AuroraXRequest(url, method="POST", json=records, api_key=api_key)
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
