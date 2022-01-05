import pyaurorax
import pprint
import datetime
from typing import Dict, List, Union
from ._conjunction import Conjunction

# pdoc init
__pdoc__: Dict = {}

# globals
DEFAULT_CONJUNCTION_DISTANCE = 300


class Search():
    """
    Class representing an AuroraX conjunctions search

    Attributes:
        start: start timestamp of the search (inclusive)
        end: end timestamp of the search (inclusive)
        ground: list of ground instrument search parameters
            e.g. [
                {
                    "programs": ["themis-asi"],
                    "platforms": ["gillam", "rabbit lake"],
                    "instrument_types": ["RGB"]
                }
            ]
        space: list of one or more space instrument search parameters
            e.g. [
                {
                    "programs": ["themis-asi", "swarm"],
                    "platforms": ["themisa", "swarma"],
                    "instrument_types": ["footprint"]
                }
            ]
        conjunction_types: list of conjunction types, defaults to ["nbtrace"]
        max_distances: dictionary of Dict[str, float] ground-space and space-space maximum
            distances for conjunctions. The default_distance will be used for any ground-space
            and space-space maximum distances not specified.

            e.g. distances = {
                "ground1-ground2": None,
                "ground1-space1": 500,
                "ground1-space2": 500,
                "ground2-space1": 500,
                "ground2-space2": 500,
                "space1-space2": None
            }
        default_distance: default maximum distance in kilometers for conjunction. Used when max
            distance is not specified for any ground-space and space-space instrument pairs.
        epoch_search_precision: the time precision to which conjunctions are calculated. Can be
            30 or 60 seconds. Defaults to 60 seconds. Note - this parameter is under active
            development and still considered "alpha".
        response_format: JSON representation of desired data response format
        request: AuroraXResponse object returned when the search is executed
        request_id: unique AuroraX string ID assigned to the request
        request_url: unique AuroraX URL string assigned to the request
        executed: boolean, gets set to True when the search is executed
        completed: boolean, gets set to True when the search is checked to be finished
        data_url: the URL string where data is accessed
        query: dictionary of values sent for the search query
        status: dictionary of status updates
        data: list of pyaurorax.conjunctions.Conjunction objects returned
        logs: list of logging messages from the API

        Returns:
            a pyaurorax.conjunctions.Search object
    """

    def __init__(self, start: datetime.datetime,
                 end: datetime.datetime,
                 ground: List[Dict],
                 space: List[Dict],
                 conjunction_types: List[str] = ["nbtrace"],
                 max_distances: Dict[str, float] = None,
                 default_distance: float = DEFAULT_CONJUNCTION_DISTANCE,
                 epoch_search_precision: int = 60,
                 response_format: Dict = None):

        self.request = None
        self.request_id = ""
        self.request_url = ""
        self.executed = False
        self.completed = False
        self.data_url = ""
        self.query = {}
        self.status = {}
        self.data: List[Union[Conjunction, Dict]] = []
        self.logs = []

        self.start = start
        self.end = end
        self.ground = ground
        self.space = space
        self.conjunction_types = conjunction_types
        self.max_distances = max_distances if max_distances else {}
        self.default_distance = default_distance
        self.epoch_search_precision = epoch_search_precision
        self.response_format = response_format

    def __str__(self):
        """
        String method

        Returns:
            string format of Conjunction Search object
        """
        return self.__repr__()

    def __repr__(self):
        """
        Object representation

        Returns:
            object representation of Conjunction Search object
        """
        return pprint.pformat(self.__dict__)

    def _set_max_distances(self):
        ground_sources_len = len(self.ground)
        space_sources_len = len(self.space)

        # check for ground-space and space-ground distances
        for g in range(1, ground_sources_len + 1):
            for s in range(1, space_sources_len + 1):
                if (f"ground{g}-space{s}" not in self.max_distances
                        and f"space{s}-ground{g}" not in self.max_distances):
                    self.max_distances[f"ground{g}-space{s}"] = self.default_distance

        # check for space-space distances
        for s in range(1, space_sources_len + 1):
            for s2 in range(s + 1, space_sources_len + 1):
                if (s != s2 and f"space{s}-space{s2}" not in self.max_distances
                        and f"space{s2}-space{s}" not in self.max_distances):
                    self.max_distances[f"space{s}-space{s2}"] = self.default_distance

    def _check_num_criteria_blocks(self):
        ground_criteria_len = len(self.ground)
        space_criteria_len = len(self.space)

        if ground_criteria_len + space_criteria_len > 10:
            raise pyaurorax.exceptions.AuroraXBadParametersException("Number of ground + space criteria "
                                                                     "blocks exceeds 10. Please use a smaller "
                                                                     "search criteria.")

        return

    def execute(self):
        """
        Initiate conjunction search request

        Raises:
            pyaurorax.exceptions.AuroraXBadParametersException: too many criteria blocks
        """
        # check number of criteria blocks
        self._check_num_criteria_blocks()

        # set up request
        url = pyaurorax.api.urls.conjunction_search_url
        self._set_max_distances()
        post_data = {
            "start": self.start.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": self.end.strftime("%Y-%m-%dT%H:%M:%S"),
            "ground": self.ground,
            "space": self.space,
            "conjunction_types": self.conjunction_types,
            "max_distances": self.max_distances,
            "epoch_search_precision": self.epoch_search_precision if self.epoch_search_precision in [30, 60] else 60,
        }
        self.query = post_data

        # do request
        req = pyaurorax.AuroraXRequest(method="post",
                                       url=url,
                                       body=post_data,
                                       null_response=True)
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
        Update the status of this conjunctions search.

        Args:
            status: retrieved status dictionary (include to avoid requesting
                    it from the API again), defaults to None.
        """
        # get the status if it isn't passed in
        if status is None:
            status = pyaurorax.requests.get_status(self.request_url)

        # update request status by checking if data URI is set
        if status["search_result"]["data_uri"] is not None:
            self.completed = True
            self.data_url = f'{pyaurorax.api.urls.base_url}{status["search_result"]["data_uri"]}'

        # set class variable "status" and "logs"
        self.status = status
        self.logs = status["logs"]

    def check_for_data(self) -> bool:
        """
        Check to see if data is available for this conjunctions
        search request

        Returns:
            True if data is available, else False
        """
        self.update_status()

        return self.completed

    def get_data(self) -> None:
        """
        Retrieve the data available for this conjunctions search request
        """
        if not self.completed:
            print("No data available, update status or check for data first")
            return

        url = self.data_url
        raw_data = pyaurorax.requests.get_data(url,
                                               post_body=self.response_format)

        if self.response_format is not None:
            self.data = raw_data
        else:
            self.data = [Conjunction(**c) for c in raw_data]

    def wait(self,
             poll_interval: float = pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME,
             verbose: bool = False) -> None:
        """
        Block and wait until the request is complete and data is
        available for retrieval

        Args:
            poll_interval: time in seconds to wait between polling attempts, defaults
                to pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME
            verbose: output poll times, defaults to False
        """
        url = pyaurorax.api.urls.conjunction_request_url.format(self.request_id)
        self.update_status(pyaurorax.requests.wait_for_data(url,
                                                            poll_interval=poll_interval,
                                                            verbose=verbose))

    def cancel(self,
               wait: bool = False,
               verbose: bool = False,
               poll_interval: float = pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME) -> int:
        """
        Cancel the conjunction search request at the API. This method
        returns asynchronously by default.

        Args:
            wait: set to True to block until the cancellation request
                has been completed (may wait for several minutes)
            verbose: if True then output poll times and other
                progress, defaults to False
            poll_interval: seconds to wait between polling
                calls, defaults to STANDARD_POLLING_SLEEP_TIME.

        Returns:
            1 on success

        Raises:
            pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
            pyaurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation
        """
        url = pyaurorax.api.urls.conjunction_request_url.format(self.request_id)
        return pyaurorax.requests.cancel(url, wait=wait, poll_interval=poll_interval, verbose=verbose)
