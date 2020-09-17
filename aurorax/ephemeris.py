import datetime
import time
import humanize
from typing import List, Dict
from .api import URL_EPHEMERIS_SOURCES, URL_EPHEMERIS_SEARCH, URL_EPHEMERIS_REQUEST_STATUS
from .api import AuroraXRequest, AuroraXResponse
from .api import get_request_status, get_request_data

# globals
__FIRST_FOLLOWUP_SLEEP_TIME = 0.050  # 50ms
__STANDARD_POLLING_SLEEP_TIME = 1.0  # 1s


def get_all_sources(format: str = "basic_info") -> Dict:
    """
    Retrieves all ephemeris source records

    :param format: the format of the ephemeris source returned Available values: "identifier_only", \
                   "basic_info", "full_record". Default is "basic_info"

    :return: information about all ephemeris sources
    """
    # make request
    url = URL_EPHEMERIS_SOURCES
    params = {
        "format": format,
    }
    req = AuroraXRequest(url, params=params)
    res = req.execute()

    # set dict to return
    return_dict = {
        "status_code": res.status_code,
        "data": [],
    }
    if (res.status_code == 200):
        return_dict["data"] = res.data

    # return
    return return_dict


def get_source_using_identifier(identifier: int, format: str = "basic_info") -> Dict:
    """
    Retrieves ephemeris source record matching identifier

    :param identifier: ephemeris source unique identifier
    :param format: the format of the ephemeris source returned (identifier_only, basic_info, \
                   full_record. Default is basic_info

    :return: information the specific ephemeris source
    """
    # make request
    url = "%s/%d" % (URL_EPHEMERIS_SOURCES, identifier)
    params = {
        "format": format
    }
    req = AuroraXRequest(url, params=params)
    res = req.execute()

    # set dict to return
    return_dict = {
        "status_code": res.status_code,
        "data": {},
    }
    if (res.status_code == 200):
        return_dict["data"] = res.data

    # return
    return return_dict


def get_source_using_filters(program: str = None, platform: str = None, instrument_type: str = None,
                             source_type: str = None, owner: str = None, format: str = "basic_info") -> Dict:
    """
    Retrieves all ephemeris source records matching the specified filters

    :param program: program name
    :param platform: platform name
    :param instrument_type: instrument type
    :param source_type: source type (leo, heo, lunar, or ground)
    :param owner: owner account name
    :param format: the format of the ephemeris source returned (identifier_only, basic_info, \
                   full_record. Default is basic_info

    :return: information about the specific ephemeris sources matching the filter criteria
    """
    # make request
    url = "%s" % (URL_EPHEMERIS_SOURCES)
    params = {
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "source_type": source_type,
        "owner": owner,
        "format": format,
    }
    req = AuroraXRequest(url, params=params)
    res = req.execute()

    # set dict to return
    return_dict = {
        "status_code": res.status_code,
        "data": [],
    }
    if (res.status_code == 200):
        return_dict["data"] = res.data

    # return
    return return_dict


def get_source_statistics(identifier: int) -> Dict:
    """
    Retrieves additional statistics about the specified ephemeris source such as
    the earliest/latest ephemeris record and the total number of ephemeris records
    available

    :param identifier: ephemeris source identifier

    :return: the ephemeris source statistics
    """
    # make request
    url = "%s/%d/stats" % (URL_EPHEMERIS_SOURCES, identifier)
    req = AuroraXRequest(url)
    res = req.execute()

    # set dict to return
    return_dict = {
        "status_code": res.status_code,
        "data": {},
    }
    if (res.status_code == 200):
        return_dict["data"] = res.data

    # return
    return return_dict


def add_source(api_key: str, program: str, platform: str, instrument_type: str, source_type: str,
               metadata_schema: List[Dict] = [], maintainers: List = []) -> Dict:
    """
    Create a new ephemeris source record

    :param api_key: API key associated with your account
    :param program: program name
    :param platform: platform name
    :param instrument_type: instrument type
    :param source_type: source type (heo, leo, lunar, ground)
    :param metadata_schema: metadata schema
    :param maintainers: list of users to give maintainer permissions to

    :return: the created ephemeris source record details
    """
    # make request
    url = URL_EPHEMERIS_SOURCES
    post_data = {
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "source_type": source_type,
        "metadata_schema": metadata_schema,
        "maintainers": maintainers,
    }
    req = AuroraXRequest(url, method="POST", api_key=api_key, json=post_data)
    res = req.execute()

    # set dict to return
    return_dict = {
        "status_code": res.status_code,
        "data": {},
    }
    if (res.status_code == 200 or res.status_code == 409):
        return_dict["data"] = res.request.json()

    # return
    return return_dict


def remove_source(api_key: str, identifier: str) -> Dict:
    """
    Remove an ephemeris source record

    :param api_key: API key associated with your account
    :param identifier: unique ephemeris source identifier

    :return: status summary
    """
    # make request
    url = "%s/%s" % (URL_EPHEMERIS_SOURCES, str(identifier))
    req = AuroraXRequest(url, method="DELETE", api_key=api_key)
    res = req.execute()

    # set dict to return
    return_dict = {
        "status_code": res.status_code,
        "data": {},
    }
    if (res.status_code == 409):
        return_dict["data"] = res.request.json()

    # return
    return return_dict


def update_source(api_key: str, identifier: str, program: str = None, platform: str = None,
                  instrument_type: str = None, source_type: str = None, metadata_schema: List[Dict] = None,
                  owner: str = None, maintainers: List = None) -> Dict:
    """
    Create a new ephemeris source record

    :param api_key: API key associated with your account
    :param identifier: ephemeris source identifier
    :param program: program name
    :param platform: platform name
    :param instrument_type: instrument type
    :param source_type: source type (heo, leo, lunar, ground)
    :param metadata_schema: metadata schema
    :param owner: owner ID
    :param maintainers: list of users to give maintainer permissions to

    :return: the new ephemeris source record details
    """
    # set new information based on current values and function parameters
    # post_data = {}
    # if (program is not None):
    #     post_data["program"] = program
    # if (platform is not None):
    #     post_data["platform"] = platform
    # if (instrument_type is not None):
    #     post_data["instrument_type"] = instrument_type
    # if (source_type is not None):
    #     post_data["source_type"] = source_type
    # if (metadata_schema is not None):
    #     post_data["metadata_schema"] = metadata_schema
    # if (owner is not None):
    #     post_data["owner"] = owner
    # if (maintainers is not None):
    #     post_data["maintainers"] = maintainers

    # # make request
    # url = "%s/%s" % (URL_EPHEMERIS_SOURCES, str(identifier))
    # print(url)
    # req = AuroraXRequest(url, method="PUT", api_key=api_key, json=post_data)
    # res = req.execute()
    # if (res.status_code != 200 and res.status_code != 409):
    #     res.data = ""
    # elif (res.status_code == 409):
    #     res.data = res.request.json()
    # return res
    pass


class Search():

    def __init__(self, start_dt: datetime, end_dt: datetime, programs: List = [], platforms: List = [],
                 instrument_types: List = [], metadata_filters: List = []) -> None:
        """
        Create a new Search object

        :param start_dt: start timestamp
        :param end_dt: end timestamp
        :param programs: programs to search through
        :param platforms: platforms to search through
        :param instrument_types: instrument types to search through
        :param metadata_filters: metadata keys and values to filter on
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

    def execute(self) -> AuroraXResponse:
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

    def update_status(self):
        # get the status
        url = URL_EPHEMERIS_REQUEST_STATUS.format(self.request_id)
        status = get_request_status(url)

        # update request status by checking if data URI is set
        if (status["request_status"]["completed"] is True):
            self.data_available = True
            self.data_url = status["request_status"]["data_url"]

        # set class variable "status" and "logs"
        self.status = status
        if (status["status_code"] == 200):
            self.logs = status["data"]["logs"]

    def check_for_data(self):
        self.update_status()

    def get_data(self):
        url = self.data_url
        data_res = get_request_data(url)
        self.data = data_res["data"]


def search(start_dt: datetime, end_dt: datetime, programs: List = [], platforms: List = [],
           instrument_types: List = [], metadata_filters: List = [], show_progress: bool = False,
           async_return: bool = False, poll_interval: int = __STANDARD_POLLING_SLEEP_TIME) -> Dict:
    """
    Search for ephemeris records

    :param start_dt: start timestamp
    :param end_dt: end timestamp
    :param programs: programs to search through
    :param platforms: platforms to search through
    :param instrument_types: instrument types to search through
    :param metadata_filters: metadata keys and values to filter on
    :param show_progress: show the progress of the request using the request log
    :param async_return: return immediately after sending the request, don't wait for data
    :param poll_interval: seconds to wait between polling calls

    :return: an AuroraXResponse object with the retrieved ephemeris data or URL of the data
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
            time.sleep(__FIRST_FOLLOWUP_SLEEP_TIME)
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


def upload():
    pass
