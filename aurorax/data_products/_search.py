import datetime
import pprint
import aurorax
from aurorax.data_products import DataProduct
import humanize
from typing import Dict, List
from aurorax.requests import STANDARD_POLLING_SLEEP_TIME


class Search():
    """
    Class representing an AuroraX data products search
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
        :type start: datetime.datetime
        :param end: end timestamp
        :type end: datetime.datetime
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
        self.data: List[DataProduct] = []
        self.logs = []

        self.start = start
        self.end = end
        self.programs = programs
        self.platforms = platforms
        self.instrument_types = instrument_types
        self.metadata_filters = metadata_filters

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
        Initiate data products search request
        """
        # set up request
        url = aurorax.api.urls.data_products_search_url
        post_data = {
            "data_sources": {
                "programs": [] if not self.programs else self.programs,
                "platforms": [] if not self.platforms else self.platforms,
                "instrument_types": [] if not self.instrument_types else self.instrument_types,
                "data_product_metadata_filters": [] if not self.metadata_filters else self.metadata_filters,
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
        Update the status of this data products search request

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
        Check to see if data is available for this data products search request
        """
        self.update_status()

    def get_data(self) -> None:
        """
        Retrieve the data available for this data products search request
        """
        if (self.completed is False):
            print("No data available, update status first")
            return
            
        url = self.data_url
        raw_data = aurorax.requests.get_data(url)

        self.data = [DataProduct(**dp) for dp in raw_data]

    def wait(self, poll_interval: float = STANDARD_POLLING_SLEEP_TIME, verbose: bool = False) -> None:
        """
        Block and wait for the request to complete and data is available for retrieval

        :param poll_interval: time in seconds to wait between polling
                              attempts, defaults to STANDARD_POLLING_SLEEP_TIME
        :type poll_interval: float, optional
        :param verbose: output poll times, defaults to False
        :type verbose: bool, optional
        """
        url = aurorax.api.urls.data_products_request_url.format(self.request_id)
        self.update_status(aurorax.requests.wait_for_data(url, poll_interval=poll_interval, verbose=verbose))


def search_async(start: datetime.datetime,
                 end: datetime.datetime,
                 programs: List[str] = None,
                 platforms: List[str] = None,
                 instrument_types: List[str] = None,
                 metadata_filters: List[Dict] = None) -> Search:
    """
    Submit a request for an data products search, return asynchronously

    :param start: start timestamp
    :type start: datetime.datetime
    :param end: end timestamp
    :type end: datetime.datetime
    :param programs: programs to search through, defaults to None
    :type programs: List[str], optional
    :param platforms: platforms to search through, defaults to None
    :type platforms: List[str], optional
    :param instrument_types: instrument types to search through, defaults to None
    :type instrument_types: List[str], optional
    :param metadata_filters: metadata keys and values to filter on, defaults to None
    :type metadata_filters: List[str], optional

    :return: Search object
    :rtype: Search
    """
    s = aurorax.data_products.Search(start,
                                     end,
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
    Search for data products records

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
    :param verbose: show the progress of the request using the request log, defaults to False
    :type verbose: bool, optional
    :param poll_interval: seconds to wait between polling calls, defaults to STANDARD_POLLING_SLEEP_TIME
    :type poll_interval: float, optional

    :return: Search object
    :rtype: Search
    """
    # create a Search() object
    s = Search(start, end, programs, platforms, instrument_types, metadata_filters)
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
