"""
Class definition for a conjunction search
"""

import pprint
import datetime
from typing import Dict, List, Union, Optional
from .conjunction import Conjunction
from ...conjunctions import (DEFAULT_CONJUNCTION_DISTANCE,
                             CONJUNCTION_TYPE_NBTRACE)
from ...api import AuroraXRequest, AuroraXResponse, urls
from ...exceptions import (AuroraXBadParametersException)
from ...requests import (STANDARD_POLLING_SLEEP_TIME,
                         cancel as requests_cancel,
                         wait_for_data as requests_wait_for_data,
                         get_data as requests_get_data,
                         get_status as requests_get_status)

# pdoc init
__pdoc__: Dict = {}


class Search():
    """
    Class representing a conjunction search

    Attributes:
        start: start timestamp of the search (inclusive)
        end: end timestamp of the search (inclusive)
        ground: list of ground instrument search parameters, defaults to []
            e.g. [
                {
                    "programs": ["themis-asi"],
                    "platforms": ["gillam", "rabbit lake"],
                    "instrument_types": ["RGB"],
                    "ephemeris_metadata_filters": {
                        "logical_operator": "AND",
                        "expressions": [
                            {
                                "key": "calgary_apa_ml_v1",
                                "operator": "in",
                                "values": [ "classified as APA" ]
                            }
                        ]
                    }
                }
            ]
        space: list of one or more space instrument search parameters, defaults to []
            e.g. [
                {
                    "programs": ["themis-asi", "swarm"],
                    "platforms": ["themisa", "swarma"],
                    "instrument_types": ["footprint"],
                    "ephemeris_metadata_filters": {
                        "logical_operator": "AND",
                        "expressions": [
                            {
                                "key": "nbtrace_region",
                                "operator": "in",
                                "values": [ "north auroral oval" ]
                            }
                        ]
                    },
                    "hemisphere": [
                        "northern"
                    ]
                }
            ]
        events: list of one or more events search parameters, defaults to []
            e.g. [
                {
                "programs": [
                    "events"
                ],
                "platforms": [
                    "toshi"
                ],
                "instrument_types": [
                    "substorm onsets"
                ]
            ]
        conjunction_types: list of conjunction types, defaults to ["nbtrace"]. Options are
            in the pyaurorax.conjunctions module, or at the top level using the
            pyaurorax.CONJUNCTION_TYPE_* variables.
        max_distances: dictionary of ground-space and space-space maximum
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
        default_distance: maximum distance in kilometers to find conjunctions for. Used when max
            distance is not specified for any ground-space and space-space instrument pairs.
        epoch_search_precision: the time precision to which conjunctions are calculated. Can be
            30 or 60 seconds. Defaults to 60 seconds. Note - this parameter is under active
            development and still considered "alpha".
        response_format: JSON representation of desired data response format
        request: AuroraXResponse object returned when the search is executed
        request_id: unique ID assigned to the request by the AuroraX API
        request_url: unique URL assigned to the request by the AuroraX API
        executed: indicates if the search has been executed/started
        completed: indicates if the search has finished
        data_url: the URL where data is accessed
        query: the query for this request as JSON
        status: the status of the query
        data: the conjunctions found
        logs: all log messages outputed by the AuroraX API for this request

        Returns:
            a pyaurorax.conjunctions.Search object
    """

    def __init__(self, start: datetime.datetime,
                 end: datetime.datetime,
                 ground: Optional[List[Dict]] = [],
                 space: Optional[List[Dict]] = [],
                 events: Optional[List[Dict]] = [],
                 conjunction_types: Optional[List[str]] = [CONJUNCTION_TYPE_NBTRACE],
                 max_distances: Optional[Dict[str, float]] = None,
                 default_distance: Optional[float] = DEFAULT_CONJUNCTION_DISTANCE,
                 epoch_search_precision: Optional[int] = 60,
                 response_format: Optional[Dict] = None):

        # set variables using passed in args
        self.start = start
        self.end = end
        self.ground = ground
        self.space = space
        self.events = events
        self.conjunction_types = conjunction_types
        self.max_distances = max_distances if max_distances else {}
        self.default_distance = default_distance
        self.epoch_search_precision = epoch_search_precision
        self.response_format = response_format

        # initialize additional variables
        self.request: AuroraXResponse = None
        self.request_id: str = ""
        self.request_url: str = ""
        self.executed: bool = False
        self.completed: bool = False
        self.data_url: str = ""
        self.query: Dict = {}
        self.status: Dict = {}
        self.data: List[Union[Conjunction, Dict]] = []
        self.logs: List[Dict] = []

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
        # check for ground-space and space-ground distances
        for g in range(1, len(self.ground) + 1):
            for s in range(1, len(self.space) + 1):
                if (f"ground{g}-space{s}" not in self.max_distances
                        and f"space{s}-ground{g}" not in self.max_distances):
                    self.max_distances[f"ground{g}-space{s}"] = self.default_distance

        # check for space-space distances
        for s in range(1, len(self.space) + 1):
            for s2 in range(s + 1, len(self.space) + 1):
                if (s != s2 and f"space{s}-space{s2}" not in self.max_distances
                        and f"space{s2}-space{s}" not in self.max_distances):
                    self.max_distances[f"space{s}-space{s2}"] = self.default_distance

        # check for ground-events and events-ground distances
        for g in range(1, len(self.ground) + 1):
            for s in range(1, len(self.events) + 1):
                if (f"ground{g}-events{s}" not in self.max_distances
                        and f"events{s}-ground{g}" not in self.max_distances):
                    self.max_distances[f"ground{g}-events{s}"] = self.default_distance

        # check for space-events and events-space distances
        for g in range(1, len(self.space) + 1):
            for s in range(1, len(self.events) + 1):
                if (f"space{g}-events{s}" not in self.max_distances
                        and f"events{s}-space{g}" not in self.max_distances):
                    self.max_distances[f"space{g}-events{s}"] = self.default_distance

    def _check_num_criteria_blocks(self):
        if ((len(self.ground) + len(self.space) + len(self.events)) > 10):
            raise AuroraXBadParametersException("Number of criteria blocks exceeds 10, "
                                                "please reduce the count")

    @property
    def query(self):
        self._set_max_distances()
        self._query = {
            "start": self.start.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": self.end.strftime("%Y-%m-%dT%H:%M:%S"),
            "ground": self.ground,
            "space": self.space,
            "events": self.events,
            "conjunction_types": self.conjunction_types,
            "max_distances": self.max_distances,
            "epoch_search_precision": self.epoch_search_precision if self.epoch_search_precision in [30, 60] else 60,
        }
        return self._query

    @query.setter
    def query(self, query):
        self._query = query

    def execute(self):
        """
        Initiate a conjunction search request

        Raises:
            pyaurorax.exceptions.AuroraXBadParametersException: too many criteria blocks
        """
        # check number of criteria blocks
        self._check_num_criteria_blocks()

        # do request
        url = urls.conjunction_search_url
        req = AuroraXRequest(method="post",
                             url=url,
                             body=self.query,
                             null_response=True)
        res = req.execute()

        # set request ID, request_url, executed
        self.executed = True
        if res.status_code == 202:
            # request successfully dispatched
            self.executed = True
            self.request_url = res.request.headers["location"]
            self.request_id = self.request_url.rsplit("/", 1)[-1]

        # set request variable
        self.request = res

    def update_status(self, status: Optional[Dict] = None) -> None:
        """
        Update the status of this conjunction search request

        Args:
            status: the previously-retrieved status of this request (include
                to avoid requesting it from the API again), defaults to None
        """
        # get the status if it isn't passed in
        if (status is None):
            status = requests_get_status(self.request_url)

        # update request status by checking if data URI is set
        if (status["search_result"]["data_uri"] is not None):
            self.completed = True
            self.data_url = f'{urls.base_url}{status["search_result"]["data_uri"]}'

        # set class variable "status" and "logs"
        self.status = status
        self.logs = status["logs"]

    def check_for_data(self) -> bool:
        """
        Check to see if data is available for this conjunction
        search request

        Returns:
            True if data is available, else False
        """
        self.update_status()
        return self.completed

    def get_data(self) -> None:
        """
        Retrieve the data available for this conjunction search request
        """
        # check if request is completed
        if (self.completed is False):
            print("No data available, update status or check for data first")
            return

        # get data
        raw_data = requests_get_data(self.data_url, response_format=self.response_format)

        # set data variable
        if (self.response_format is not None):
            self.data = raw_data
        else:
            self.data = [Conjunction(**c) for c in raw_data]

    def wait(self,
             poll_interval: Optional[float] = STANDARD_POLLING_SLEEP_TIME,
             verbose: Optional[bool] = False) -> None:
        """
        Block and wait until the request is complete and data is
        available for retrieval

        Args:
            poll_interval: time in seconds to wait between polling attempts, defaults
                to pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME
            verbose: output poll times and other progress messages, defaults to False
        """
        url = urls.conjunction_request_url.format(self.request_id)
        self.update_status(requests_wait_for_data(url,
                                                  poll_interval=poll_interval,
                                                  verbose=verbose))

    def cancel(self,
               wait: Optional[bool] = False,
               poll_interval: Optional[float] = STANDARD_POLLING_SLEEP_TIME,
               verbose: Optional[bool] = False) -> int:
        """
        Cancel the conjunction search request

        This method returns immediately by default since the API processes
        this request asynchronously. If you would prefer to wait for it
        to be completed, set the 'wait' parameter to True. You can adjust
        the polling time using the 'poll_interval' parameter.

        Args:
            wait: wait until the cancellation request has been
                completed (may wait for several minutes)
            poll_interval: seconds to wait between polling
                calls, defaults to STANDARD_POLLING_SLEEP_TIME.
            verbose: output poll times and other progress messages, defaults
                to False

        Returns:
            1 on success

        Raises:
            pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
            pyaurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation
        """
        url = urls.conjunction_request_url.format(self.request_id)
        return requests_cancel(url, wait=wait, poll_interval=poll_interval, verbose=verbose)
