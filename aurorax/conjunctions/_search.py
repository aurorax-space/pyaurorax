import pprint
import humanize
import aurorax
from aurorax.conjunctions import Conjunction
from aurorax.requests import STANDARD_POLLING_SLEEP_TIME
import datetime
from typing import Dict, List

DEFAULT_CONJUNCTION_DISTANCE = 300

class Search():
    """
    Class representing an AuroraX conjunctions search
    """

    def __init__(self, start: datetime.datetime, end: datetime.datetime, 
                ground: List[Dict], space: List[Dict], conjunction_types: List[str] = ["nbtrace"],
                max_distances: Dict[str, float] = None, default_distance: float = DEFAULT_CONJUNCTION_DISTANCE):
        """
        Create a new conjunction Search object

        :param start: start timestamp
        :type start: datetime.datetime
        :param end: end timestamp
        :type end: datetime.datetime
        :param ground: List of ground instrument search parameters
        :type ground: List[Dict]
        :param space: List of one or more space instrument search parameters
        :type space: List[Dict]
        :param conjunction_types: list of conjunction types, defaults to ["nbtrace"]
        :type conjunction_types: List[str], optional
        :param max_distances: dictionary of ground-space and space-space maximum distances for conjunctions. default_distance will be used for any ground-space and space-space maximum distances not specified.
        :type max_distances: Dict[str, float], optional
        :param default_distance: default maximum distance in kilometers for conjunction. Used when max distance is not specified for any ground-space and space-space instrument pairs.
        :type default_distance: float, optional

        :return: Search object
        :rtype: Search
        """
        self.request = None
        self.request_id = ""
        self.request_url = ""
        self.executed = False
        self.completed = False
        self.data_url = ""
        self.query = {}
        self.status = {}
        self.data: List[Conjunction] = []
        self.logs = []

        self.start = start
        self.end = end
        self.ground = ground
        self.space = space
        self.conjunction_types = conjunction_types
        self.max_distances = max_distances if max_distances else {}
        self.default_distance = default_distance

    def __str__(self):
        """
        String method

        :return: string format
        :rtype: str
        """
        return self.__repr__()

    def __repr__(self):
        """
        Object representation

        :return: object representation
        :rtype: str
        """
        return pprint.pformat(self.__dict__)

    def _set_max_distances(self):
        ground_sources_len = len(self.ground)
        space_sources_len = len(self.space)

        # check for ground-space and space-ground distances
        for g in range(1, ground_sources_len+1):
            for s in range(1, space_sources_len+1):
                if f"ground{g}-space{s}" not in self.max_distances and f"space{s}-ground{g}" not in self.max_distances:
                    self.max_distances[f"ground{g}-space{s}"] = self.default_distance

        # check for space-space distances
        for s in range(1, space_sources_len+1):
            for s2 in range(s+1, space_sources_len+1):
                if s != s2 and f"space{s}-space{s2}" not in self.max_distances and f"space{s2}-space{s}" not in self.max_distances:
                    self.max_distances[f"space{s}-space{s2}"] = self.default_distance

    def execute(self):
        """
        Initiate conjunction search request
        """
        # set up request
        url = aurorax.api.urls.conjunction_search_url
        self._set_max_distances()
        post_data = {
            "start": self.start.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": self.end.strftime("%Y-%m-%dT%H:%M:%S"),
            "ground": self.ground,
            "space": self.space,
            "conjunction_types": self.conjunction_types,
            "max_distances": self.max_distances
        }
        self.query = post_data

        # do request
        req = aurorax.AuroraXRequest(method="post", url=url, body=post_data, null_response=True)
        res = req.execute()

        # set request ID, request_url, executed
        self.executed = True
        if res.status_code == 202:
            # request successfully dispatched
            self.executed = True
            self.request_url = res.request.headers["location"]
            self.request_id = self.request_url.rsplit("/", 1)[-1]

        self.request = res

    def update_status(self, status: Dict = None) -> None:
        """
        Update the status of this conjunctions search

        :param status: retrieved status (include to avoid requestinf it from the API again), defaults to None
        :type status: Dict, optional
        """
        # get the status if it isn't passed in
        if status is None:
            status = aurorax.requests.get_status(self.request_url)

        # update request status by checking if data URI is set
        if status["search_result"]["data_uri"] is not None:
            self.completed = True
            self.data_url = f'{aurorax.api.urls.base_url}{status["search_result"]["data_uri"]}'

        # set class variable "status" and "logs"
        self.status = status
        self.logs = status["logs"]

    def check_for_data(self) -> None:
        """
        Check to see if data is available for this conjunctions search request
        """
        self.update_status()

    def get_data(self) -> None:
        if not self.completed:
            print("No data available, update status first")
            return

        url = self.data_url
        raw_data = aurorax.requests.get_data(url)
        self.data = [Conjunction(**c) for c in raw_data]

    def wait(self, poll_interval: float = STANDARD_POLLING_SLEEP_TIME, verbose: bool = False) -> None:
        """
        Block and wait until the request is complete and data is available for retrieval

        :param poll_interval: time in seconds to wait between polling attempts, defaults to STANDARD_POLLING_SLEEP_TIME
        :type poll_interval: float, optional
        :param verbose: output poll times, defaults to False
        :type verbose: bool, optional
        """
        url = aurorax.api.urls.conjunction_request_url.format(self.request_id)
        self.update_status(aurorax.requests.wait_for_data(url, poll_interval=poll_interval, verbose=verbose))

def search_async(start: datetime.datetime, end: datetime.datetime, 
                ground: List[Dict], space: List[Dict], conjunction_types: List[str] = ["nbtrace"],
                max_distances: Dict[str, float] = {}, default_distance: float = DEFAULT_CONJUNCTION_DISTANCE) -> Search:
    """
    Submit a request for a conjunctions search, return asynchronously

    :param start: start timestamp
    :type start: datetime.datetime
    :param end: end timestamp
    :type end: datetime.datetime
    :param ground: List of ground instrument search parameters
    :type ground: List[Dict]
    :param space: List of one or more space instrument search parameters
    :type space: List[Dict]
    :param conjunction_types: list of conjunction types, defaults to ["nbtrace"]
    :type conjunction_types: List[str], optional
    :param max_distances: dictionary of ground-space and space-space maximum distances for conjunctions. default_distance will be used for any ground-space and space-space maximum distances not specified.
    :type max_distances: Dict[str, float], optional
    :param default_distance: default maximum distance in kilometers for conjunction. Used when max distance is not specified for any ground-space and space-space instrument pairs.
    :type default_distance: float, optional

    :return: Search object
    :rtype: Search
    """
    s = Search(start=start, end=end, ground=ground, space=space, conjunction_types=conjunction_types, max_distances=max_distances, default_distance=default_distance)
    s.execute()

    return s

def search(start: datetime.datetime, end: datetime.datetime, 
            ground: List[Dict], space: List[str], conjunction_types: List[str] = ["nbtrace"],
            max_distances: Dict[str, float] = {}, default_distance: float = DEFAULT_CONJUNCTION_DISTANCE, verbose: bool = False,
            poll_interval: float = STANDARD_POLLING_SLEEP_TIME) -> Search:
    """
    Search for conjunctions 

    :param start: start timestamp
    :type start: datetime.datetime
    :param end: end timestamp
    :type end: datetime.datetime
    :param ground: List of ground instrument search parameters
    :type ground: List[Dict]
    :param space: List of one or more space instrument search parameters
    :type space: List[Dict]
    :param conjunction_types: list of conjunction types, defaults to ["nbtrace"]
    :type conjunction_types: List[str], optional
    :param max_distances: dictionary of ground-space and space-space maximum distances for conjunctions. default_distance will be used for any ground-space and space-space maximum distances not specified.
    :type max_distances: Dict[str, float], optional
    :param default_distance: default maximum distance in kilometers for conjunction. Used when max distance is not specified for any ground-space and space-space instrument pairs.
    :type default_distance: float, optional
    :param verbose: show the progress of the request using the request log, defaults to False
    :type verbose: bool, optional
    :param poll_interval: seconds to wait between polling calls, defaults to STANDARD_POLLING_SLEEP_TIME
    :type poll_interval: float, optional

    :return: Search object
    :rtype: Search
    """
    # create a Search object
    s = Search(start, end, ground, space, conjunction_types, max_distances, default_distance)
    if verbose:
        print(f"[{datetime.datetime.now()}] Search object created")

    # execute the search
    s.execute()
    if verbose:
        print(f"[{datetime.datetime.now()}] Request submitted")
        print(f"[{datetime.datetime.now()}] Request ID: {s.request_id}")
        print(f"[{datetime.datetime.now()}] Request details available at: {s.request_url}")
        print(f"[{datetime.datetime.now()}] Waiting for data ...")

    s.wait(poll_interval=poll_interval, verbose=verbose)

    # get the data
    if verbose:
        print(f"[{datetime.datetime.now()}] Retrieving data ...")

    s.get_data()

    if verbose:
        print(f'[{datetime.datetime.now()}] Retrieved {humanize.filesize.naturalsize(s.status["search_result"]["file_size"])} of data containing {s.status["search_result"]["result_count"]} records')
    
    return s