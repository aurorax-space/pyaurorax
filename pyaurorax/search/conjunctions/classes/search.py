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
from copy import deepcopy
from typing import TYPE_CHECKING, Dict, Union, Optional, Sequence, Literal
from .conjunction import Conjunction
from .criteria_block import (
    GroundCriteriaBlock,
    SpaceCriteriaBlock,
    EventsCriteriaBlock,
    CustomLocationsCriteriaBlock,
)
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
    from ....pyaurorax import PyAuroraX  # pragma: nocover-ok


class ConjunctionSearch:
    """
    Class representing a conjunction search

    Attributes:
        start (datetime.datetime): 
            Start timestamp of the search (inclusive).

        end (datetime.datetime): 
            End timestamp of the search (inclusive).

        distance (int or float or Dict): 
            The maximum distance allowed between data sources when searching for
            conjunctions. This can either be a number (int or float), or a dictionary
            modified from the output of the "get_advanced_distances_combos()" function.

        ground (List[GroundCriteriaBlock or Dict]): 
            List of ground instrument criteria blocks, defaults to [].

        space (List[SpaceCriteriaBlock or Dict]): 
            List of space instrument criteria blocks, defaults to [].

        events (List[EventsCriteriaBlock or Dict]): 
            List of event criteria blocks, defaults to [].

        custom_locations (List[CustomLocationsCriteriaBlock or Dict]): 
            List of custom location criteria blocks, defaults to [].

        conjunction_types (List[str]): 
            List of conjunction types, defaults to [] (meaning all conjunction types). Valid
            options are 'nbtrace', 'sbtrace', and 'geographic'. Defaults to 'nbtrace'.

        response_format (Dict): 
            JSON representation of desired data response format

        request (AuroraXResponse): 
            AuroraXResponse object returned when the search is executed

        request_id (str): 
            Unique ID assigned to the request by the AuroraX API

        request_url (str): 
            Unique URL assigned to the request by the AuroraX API

        executed (bool): 
            Indicates if the search has been executed/started

        completed (bool): 
            Indicates if the search has finished

        data_url (str): 
            The URL where data is accessed

        query (Dict): 
            The query for this request as JSON

        status (Dict): 
            The status of the query

        data (List[Conjunction, Dict]): 
            A list of the conjunctions found. The results will be dictionaries only if the
            response_format parameter was supplied.

        logs (List[Dict]): 
            All log messages outputted by the AuroraX API for this request
    """

    __STANDARD_POLLING_SLEEP_TIME: float = 1.0

    def __init__(self,
                 aurorax_obj: PyAuroraX,
                 start: datetime.datetime,
                 end: datetime.datetime,
                 distance: Union[int, float, Dict],
                 ground: Sequence[Union[GroundCriteriaBlock, Dict]] = [],
                 space: Sequence[Union[SpaceCriteriaBlock, Dict]] = [],
                 events: Sequence[Union[EventsCriteriaBlock, Dict]] = [],
                 custom_locations: Sequence[Union[CustomLocationsCriteriaBlock, Dict]] = [],
                 conjunction_types: Sequence[Union[str, Literal["nbtrace", "sbtrace", "geographic"]]] = ["nbtrace"],
                 response_format: Optional[Dict] = None):

        # some verification
        for item in ground:
            if (isinstance(item, dict) is False and isinstance(item, GroundCriteriaBlock) is False):
                raise ValueError(
                    "A %s object was found in the 'ground' parameter. Only GroundCriteriaBlock objects are allowed in the ground parameter." %
                    (item.__class__.__name__))
        for item in space:
            if (isinstance(item, dict) is False and isinstance(item, SpaceCriteriaBlock) is False):
                raise ValueError(
                    "A %s object was found in the 'space' parameter. Only SpaceCriteriaBlock objects are allowed in the ground parameter." %
                    (item.__class__.__name__))
        for item in events:
            if (isinstance(item, dict) is False and isinstance(item, EventsCriteriaBlock) is False):
                raise ValueError(
                    "A %s object was found in the 'events' parameter. Only EventsCriteriaBlock objects are allowed in the ground parameter." %
                    (item.__class__.__name__))
        for item in custom_locations:
            if (isinstance(item, dict) is False and isinstance(item, CustomLocationsCriteriaBlock) is False):
                raise ValueError(("A %s object was found in the 'custom_locations' parameter. Only CustomLocationsCriteriaBlock objects " +
                                  "are allowed in the ground parameter.") % (item.__class__.__name__))

        # set variables using passed in args
        self.__aurorax_obj = aurorax_obj
        self.start = start
        self.end = end
        self.ground = ground
        self.space = space
        self.events = events
        self.custom_locations = custom_locations
        self.distance = distance
        self.conjunction_types = conjunction_types
        self.response_format = response_format

        # initialize additional variables
        self.request = None
        self.request_id = ""
        self.request_url = ""
        self.executed = False
        self.completed = False
        self.data_url = ""
        self.__query = {}
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
            if (len(self.data) == 1):
                data_str = "[1 conjunction result]"
            else:
                data_str = "[%d conjunction results]" % (len(self.data))
        else:
            data_str = ""

        # set logs string
        if (self.executed is True):
            if (len(self.logs) == 1):  # pragma: nocover-ok
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
            pyaurorax.exceptions.AuroraXError: Too many criteria blocks are found
        """
        count_ground = 0
        count_space = 0
        count_events = 0
        count_custom_locations = 0
        if (self.ground is not None):
            count_ground = len(self.ground)
        if (self.space is not None):
            count_space = len(self.space)
        if (self.events is not None):
            count_events = len(self.events)
        if (self.custom_locations is not None):
            count_custom_locations = len(self.custom_locations)
        if ((count_ground + count_space + count_events + count_custom_locations) > 10):
            raise AuroraXError("Number of criteria blocks exceeds 10, please reduce the count")

    def get_advanced_distances_combos(self, default_distance: Optional[Union[int, float]] = None) -> Dict:
        """
        Get the advanced distances combinations for this search

        Args:
            default_distance (int): 
                The default distance to use, defaults to None

        Returns:
            The advanced distances combinations
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
        if (self.custom_locations is not None):
            for i in range(0, len(self.custom_locations)):
                options.append("adhoc%d" % (i + 1))

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
            The distance dictionary with all combinations
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
            The query parameter
        """
        # set ground
        ground_param = self.ground
        if (isinstance(self.ground, list) and all(isinstance(item, GroundCriteriaBlock) for item in self.ground)):
            # ground parameter is a list of GroundCriteriaBlock objects, so we
            # want to set the query to the dict version of it
            ground_param = []
            for val in self.ground:
                this_dict = deepcopy(val.__dict__)
                this_dict["ephemeris_metadata_filters"] = this_dict["metadata_filters"]
                del this_dict["metadata_filters"]
                if (this_dict["ephemeris_metadata_filters"] is not None):
                    this_dict["ephemeris_metadata_filters"] = this_dict["ephemeris_metadata_filters"].to_query_dict()
                ground_param.append(this_dict)

        # set space
        space_param = self.space
        if (isinstance(self.space, list) and all(isinstance(item, SpaceCriteriaBlock) for item in self.space)):
            # space parameter is a list of SpaceCriteriaBlock objects, so we
            # want to set the query to the dict version of it
            space_param = []
            for val in self.space:
                this_dict = deepcopy(val.__dict__)
                this_dict["ephemeris_metadata_filters"] = this_dict["metadata_filters"]
                del this_dict["metadata_filters"]
                if (this_dict["ephemeris_metadata_filters"] is not None):
                    this_dict["ephemeris_metadata_filters"] = this_dict["ephemeris_metadata_filters"].to_query_dict()
                space_param.append(this_dict)

        # set events
        events_param = self.events
        if (isinstance(self.events, list) and all(isinstance(item, EventsCriteriaBlock) for item in self.events)):
            # space parameter is a list of EventsCriteriaBlock objects, so we
            # want to set the query to the dict version of it
            events_param = []
            for val in self.events:
                this_dict = deepcopy(val.__dict__)
                this_dict["ephemeris_metadata_filters"] = this_dict["metadata_filters"]
                this_dict["programs"] = ["events"]
                del this_dict["metadata_filters"]
                if (this_dict["ephemeris_metadata_filters"] is not None):
                    this_dict["ephemeris_metadata_filters"] = this_dict["ephemeris_metadata_filters"].to_query_dict()  # pragma: nocover
                events_param.append(this_dict)

        # set custom locations
        custom_param = self.custom_locations
        if (isinstance(self.custom_locations, list) and all(isinstance(item, CustomLocationsCriteriaBlock) for item in self.custom_locations)):
            # space parameter is a list of CustomLocationsCriteriaBlock objects, so we
            # want to set the query to the dict version of it
            custom_param = []
            for val in self.custom_locations:
                this_dict = val.to_search_query_dict()  # type: ignore
                custom_param.append(this_dict)

        # set query
        self.__query = {
            "start": self.start.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": self.end.strftime("%Y-%m-%dT%H:%M:%S"),
            "ground": ground_param,
            "space": space_param,
            "events": events_param,
            "adhoc": custom_param,
            "conjunction_types": self.conjunction_types,
            "max_distances": self.distance,
            "epoch_search_precision": 60,
        }
        return self.__query

    def execute(self) -> None:
        """
        Initiate a conjunction search request

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        # check number of criteria blocks
        self.check_criteria_block_count_validity()

        # do request
        url = "%s/%s" % (self.__aurorax_obj.api_base_url, self.__aurorax_obj.search.api.URL_SUFFIX_CONJUNCTION_SEARCH)
        req = AuroraXAPIRequest(self.__aurorax_obj, method="post", url=url, body=self.query, null_response=True)
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
            status (Dict): 
                The previously-retrieved status of this request (include
                to avoid requesting it from the API again), defaults to None

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        # get the status if it isn't passed in
        if (status is None):
            status = requests_get_status(self.__aurorax_obj, self.request_url)

        # check response
        if (status is None):  # pragma: nocover-ok
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
        raw_data = requests_get_data(self.__aurorax_obj, self.data_url, self.response_format, False)

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
            poll_interval (float): 
                Time in seconds to wait between polling attempts, defaults to 1 second

            verbose (bool): 
                Output poll times and other progress messages, defaults to False

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        url = "%s/%s" % (self.__aurorax_obj.api_base_url, self.__aurorax_obj.search.api.URL_SUFFIX_CONJUNCTION_REQUEST.format(self.request_id))
        self.update_status(requests_wait_for_data(self.__aurorax_obj, url, poll_interval, verbose))

    def cancel(self, wait: bool = False, poll_interval: float = __STANDARD_POLLING_SLEEP_TIME, verbose: bool = False) -> int:
        """
        Cancel the conjunction search request

        This method returns immediately by default since the API processes
        this request asynchronously. If you would prefer to wait for it
        to be completed, set the 'wait' parameter to True. You can adjust
        the polling time using the 'poll_interval' parameter.

        Args:
            wait (bool): 
                Wait until the cancellation request has been completed (may wait for several minutes)

            poll_interval (float): 
                Seconds to wait between polling calls, defaults to STANDARD_POLLING_SLEEP_TIME.

            verbose (bool): 
                Output poll times and other progress messages, defaults to False

        Returns:
            1 on success

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        url = "%s/%s" % (self.__aurorax_obj.api_base_url, self.__aurorax_obj.search.api.URL_SUFFIX_CONJUNCTION_REQUEST.format(self.request_id))
        return requests_cancel(self.__aurorax_obj, url, wait, poll_interval, verbose)

    def describe(self):
        """
        Describe the conjunction search as an "SQL-like" string.

        Returns:
            The "SQL-like" string describing the conjunction search object
        """
        # make request
        url = "%s/%s" % (self.__aurorax_obj.api_base_url, self.__aurorax_obj.search.api.URL_SUFFIX_DESCRIBE_CONJUNCTION_QUERY)
        req = AuroraXAPIRequest(self.__aurorax_obj, method="post", url=url, body=self.query)
        res = req.execute()

        # return
        return res.data
