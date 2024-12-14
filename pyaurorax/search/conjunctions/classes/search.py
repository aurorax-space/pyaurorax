# Copyright 2024 University of Calgary
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Class definition for a conjunction search
"""

from __future__ import annotations
import datetime
import itertools
from typing import TYPE_CHECKING, Dict, List, Union, Optional
from .conjunction import Conjunction, CONJUNCTION_TYPE_NBTRACE
from ...api import AuroraXAPIRequest
from ...sources import DataSource, FORMAT_BASIC_INFO
from ....exceptions import AuroraXError, AuroraXAPIError
from ...requests._requests import (
    cancel as requests_cancel,
    wait_for_data as requests_wait_for_data,
    get_data as requests_get_data,
    get_status as requests_get_status,
)
if TYPE_CHECKING:
    from ....pyaurorax import PyAuroraX


class ConjunctionSearch:
    """
    Class representing a conjunction search

    Attributes:
        start: start timestamp of the search (inclusive)
        end: end timestamp of the search (inclusive)
        distance: the maximum distance allowed between data sources when searching for
            conjunctions. This can either be a number (int or float), or a dictionary
            modified from the output of the "get_advanced_distances_combos()" function.
        ground: list of ground instrument search parameters, defaults to []

            Example:

                [{
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
                }]
        space: list of one or more space instrument search parameters, defaults to []

            Example:

                [{
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
                }]
        events: list of one or more events search parameters, defaults to []

            Example:

                [{
                    "programs": [ "events" ],
                    "instrument_types": [ "substorm onsets" ]
                }]
        conjunction_types: list of conjunction types, defaults to ["nbtrace"]. Options are
            in the pyaurorax.conjunctions module, or at the top level using the
            pyaurorax.CONJUNCTION_TYPE_* variables.
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
        logs: all log messages outputted by the AuroraX API for this request
    """

    __STANDARD_POLLING_SLEEP_TIME: float = 1.0

    def __init__(self,
                 aurorax_obj: PyAuroraX,
                 start: datetime.datetime,
                 end: datetime.datetime,
                 distance: Union[int, float, Dict],
                 ground: Optional[List[Dict]] = None,
                 space: Optional[List[Dict]] = None,
                 events: Optional[List[Dict]] = None,
                 conjunction_types: Optional[List[str]] = None,
                 epoch_search_precision: Optional[int] = None,
                 response_format: Optional[Dict] = None):

        # set variables using passed in args
        self.aurorax_obj = aurorax_obj
        self.start = start
        self.end = end
        self.ground = [] if ground is None else ground
        self.space = [] if space is None else space
        self.events = [] if events is None else events
        self.distance = distance
        self.conjunction_types = [CONJUNCTION_TYPE_NBTRACE] if conjunction_types is None else conjunction_types
        self.epoch_search_precision = 60 if epoch_search_precision is None else epoch_search_precision
        self.response_format = response_format

        # initialize additional variables
        self.request = None
        self.request_id = ""
        self.request_url = ""
        self.executed = False
        self.completed = False
        self.data_url = ""
        self.query = {}
        self.status = {}
        self.data = []
        self.logs = []

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "ConjunctionSearch(executed=%s, completed=%s, request_id='%s')" % (
            self.executed,
            self.completed,
            self.request_id,
        )

    def pretty_print(self):
        """
        A special print output for this class.
        """
        # set status and query strings
        max_len = 80
        status_str = str(self.status)
        query_str = str(self.query)
        if (len(status_str) > max_len):
            status_str = "%s..." % (status_str[0:max_len])
        if (len(query_str) > max_len):
            query_str = "%s..." % (query_str[0:max_len])

        # set results string
        if (self.executed is True):
            if (len(self.data) == 0):
                data_str = "[0 conjunction results]"
            elif (len(self.data) == 1):
                data_str = "[1 conjunction result]"
            else:
                data_str = "[%d conjunction results]" % (len(self.data))
        else:
            data_str = ""

        # set logs string
        if (self.executed is True):
            if (len(self.logs) == 0):
                logs_str = "[0 log messages]"
            elif (len(self.logs) == 1):
                logs_str = "[1 log message]"
            else:
                logs_str = "[%d log messages]" % (len(self.logs))
        else:
            logs_str = ""

        # print
        print("ConjunctionSearch:")
        print("  %-13s: %s" % ("executed", self.executed))
        print("  %-13s: %s" % ("completed", self.completed))
        print("  %-13s: %s" % ("request_id", self.request_id))
        print("  %-13s: %s" % ("request", self.request))
        print("  %-13s: %s" % ("request_url", self.request_url))
        print("  %-13s: %s" % ("data_url", self.data_url))
        print("  %-13s: %s" % ("query", query_str))
        print("  %-13s: %s" % ("status", status_str))
        print("  %-13s: %s" % ("data", data_str))
        print("  %-13s: %s" % ("logs", logs_str))

    def __fill_in_missing_distances(self, curr_distances: Dict) -> Dict:
        # get all distances possible
        all_distances = self.get_advanced_distances_combos()

        # go through current distances and fill in the values
        for curr_key, curr_value in curr_distances.items():
            curr_key_split = curr_key.split('-')
            curr_key1 = curr_key_split[0].strip()
            curr_key2 = curr_key_split[1].strip()
            for all_key in all_distances.keys():
                if (curr_key1 in all_key and curr_key2 in all_key):
                    # found the matching key, replace the value
                    all_distances[all_key] = curr_value

        # return
        return all_distances

    def check_criteria_block_count_validity(self) -> None:
        """
        Check the number of of criteria blocks to see if there
        is too many. A max of 10 is allowed by the AuroraX
        conjunction search engine. An exception is raised if
        it was determined to have too many.

        Raises:
            pyaurorax.exceptions.AuroraXError: too many criteria blocks are found
        """
        count_ground = 0
        count_space = 0
        count_events = 0
        if (self.ground is not None):
            count_ground = len(self.ground)
        if (self.space is not None):
            count_space = len(self.space)
        if (self.events is not None):
            count_events = len(self.events)
        if ((count_ground + count_space + count_events) > 10):
            raise AuroraXError("Number of criteria blocks exceeds 10, please reduce the count")

    def get_advanced_distances_combos(self, default_distance: Optional[Union[int, float]] = None) -> Dict:
        """
        Get the advanced distances combinations for this search

        Args:
            default_distance: the default distance to use, defaults to None

        Returns:
            the advanced distances combinations
        """
        # set input arrays
        options = []
        if (self.ground is not None):
            for i in range(0, len(self.ground)):
                options.append("ground%d" % (i + 1))
        if (self.space is not None):
            for i in range(0, len(self.space)):
                options.append("space%d" % (i + 1))
        if (self.events is not None):
            for i in range(0, len(self.events)):
                options.append("events%d" % (i + 1))

        # derive all combinations of options of size 2
        combinations = {}
        for element in itertools.combinations(options, r=2):
            combinations["%s-%s" % (element[0], element[1])] = default_distance

        # return
        return combinations

    @property
    def distance(self) -> Union[int, float, Dict[str, Union[int, float]]]:
        """
        Property for the distance parameter

        Returns:
            the distance dictionary with all combinations
        """
        return self.__distance

    @distance.setter
    def distance(self, distance: Union[int, float, Dict[str, Union[int, float]]]) -> None:
        # set distances to a dict if it's an int or float
        if (isinstance(distance, int) or isinstance(distance, float)):
            self.__distance = self.get_advanced_distances_combos(default_distance=distance)  # type: ignore
        else:
            # is a dict, fill in any gaps
            self.__distance = self.__fill_in_missing_distances(distance)  # type: ignore

    @property
    def query(self) -> Dict:
        """
        Property for the query value

        Returns:
            the query parameter
        """
        self._query = {
            "start": self.start.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": self.end.strftime("%Y-%m-%dT%H:%M:%S"),
            "ground": self.ground,
            "space": self.space,
            "events": self.events,
            "conjunction_types": self.conjunction_types,
            "max_distances": self.distance,
            "epoch_search_precision": self.epoch_search_precision if self.epoch_search_precision in [30, 60] else 60,
        }
        return self._query

    @query.setter
    def query(self, query: Dict) -> None:
        self._query = query

    def execute(self) -> None:
        """
        Initiate a conjunction search request

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        # check number of criteria blocks
        self.check_criteria_block_count_validity()

        # do request
        url = "%s/%s" % (self.aurorax_obj.api_base_url, self.aurorax_obj.search.api.URL_SUFFIX_CONJUNCTION_SEARCH)
        req = AuroraXAPIRequest(self.aurorax_obj, method="post", url=url, body=self.query, null_response=True)
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

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        # get the status if it isn't passed in
        if (status is None):
            status = requests_get_status(self.aurorax_obj, self.request_url)

        # check response
        if (status is None):
            raise AuroraXAPIError("Could not retrieve status for this request")

        # update request status by checking if data URI is set
        if (status["search_result"]["data_uri"] is not None):
            self.completed = True
            self.data_url = "%s/data" % (self.request_url)

        # set class variable "status" and "logs"
        self.status = status
        self.logs = status["logs"]

    def check_for_data(self) -> bool:
        """
        Check to see if data is available for this conjunction
        search request

        Returns:
            True if data is available, else False

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        self.update_status()
        return self.completed

    def get_data(self) -> None:
        """
        Retrieve the data available for this conjunction search request

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        # check if completed yet
        if (self.completed is False):
            print("No data available, update status or check for data first")
            return

        # get data
        raw_data = requests_get_data(self.aurorax_obj, self.data_url, self.response_format, False)

        # set data variable
        if (self.response_format is not None):
            self.data = raw_data
        else:
            # cast data source objects
            for i in range(0, len(raw_data)):
                for j in range(0, len(raw_data[i]["data_sources"])):
                    ds = DataSource(**raw_data[i]["data_sources"][j], format=FORMAT_BASIC_INFO)
                    raw_data[i]["data_sources"][j] = ds

            # cast conjunctions
            self.data = [Conjunction(**c) for c in raw_data]

    def wait(self, poll_interval: float = __STANDARD_POLLING_SLEEP_TIME, verbose: bool = False) -> None:
        """
        Block and wait until the request is complete and data is
        available for retrieval

        Args:
            poll_interval: time in seconds to wait between polling attempts, defaults
                to pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME
            verbose: output poll times and other progress messages, defaults to False

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        url = "%s/%s" % (self.aurorax_obj.api_base_url, self.aurorax_obj.search.api.URL_SUFFIX_CONJUNCTION_REQUEST.format(self.request_id))
        self.update_status(requests_wait_for_data(self.aurorax_obj, url, poll_interval, verbose))

    def cancel(self, wait: bool = False, poll_interval: float = __STANDARD_POLLING_SLEEP_TIME, verbose: bool = False) -> int:
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
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        url = "%s/%s" % (self.aurorax_obj.api_base_url, self.aurorax_obj.search.api.URL_SUFFIX_CONJUNCTION_REQUEST.format(self.request_id))
        return requests_cancel(self.aurorax_obj, url, wait, poll_interval, verbose)
