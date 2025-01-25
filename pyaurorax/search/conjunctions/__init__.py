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
Use the AuroraX search engine to find conjunctions between groupings 
of data sources.

Note that all functions and classes from submodules are all imported
at this level of the conjunctions module. They can be referenced from
here instead of digging in deeper to the submodules.
"""

import datetime
from typing import Dict, Optional, Union, Sequence, Literal
from .swarmaurora import SwarmAuroraManager
from .classes.search import ConjunctionSearch
from .classes.criteria_block import (
    GroundCriteriaBlock,
    SpaceCriteriaBlock,
    EventsCriteriaBlock,
)
from ._conjunctions import search as func_search
from ._conjunctions import describe as func_describe
from ._conjunctions import get_request_url as func_get_request_url
from ._conjunctions import create_advanced_distance_combos as func_create_advanced_distance_combos

__all__ = ["ConjunctionsManager"]


class ConjunctionsManager:
    """
    The ConjunctionsManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    __STANDARD_POLLING_SLEEP_TIME: float = 1.0  # Polling sleep time when waiting for data (after the initial sleep time), in seconds

    def __init__(self, aurorax_obj):
        self.__aurorax_obj = aurorax_obj

        # initialize sub-modules
        self.__swarmaurora = SwarmAuroraManager(self.__aurorax_obj)

    @property
    def swarmaurora(self):
        """
        Access to the `swarmaurora` submodule from within a PyAuroraX object.
        """
        return self.__swarmaurora

    def search(self,
               start: datetime.datetime,
               end: datetime.datetime,
               distance: Union[int, float, Dict],
               ground: Sequence[Union[GroundCriteriaBlock, Dict]] = [],
               space: Sequence[Union[SpaceCriteriaBlock, Dict]] = [],
               events: Sequence[Union[EventsCriteriaBlock, Dict]] = [],
               conjunction_types: Sequence[Union[str, Literal["nbtrace", "sbtrace"]]] = [],
               response_format: Optional[Dict] = None,
               poll_interval: float = __STANDARD_POLLING_SLEEP_TIME,
               return_immediately: bool = False,
               verbose: bool = False) -> ConjunctionSearch:
        """
        Search for conjunctions between data sources

        By default, this function will block and wait until the request completes and
        all data is downloaded. If you don't want to wait, set the 'return_immediately`
        value to True. The Search object will be returned right after the search has been
        started, and you can use the helper functions as part of that object to get the
        data when it's done.

        Args:
            start (datetime.datetime): 
                Start timestamp of the search (inclusive).

            end (datetime.datetime): 
                End timestamp of the search (inclusive).

            distance (int or float or Dict): 
                The maximum distance allowed between data sources when searching for
                conjunctions. This can either be a number (int or float), or a dictionary
                modified from the output of the "get_advanced_distances_combos()" function.

            ground (List[GroundCriteriaBlock or Dict]): 
                List of ground instrument criteria blocks, defaults to []. List items of Dict 
                types have been deprecated as of v1.14.0.

            space (List[SpaceCriteriaBlock or Dict]): 
                List of space instrument criteria blocks, defaults to []. List items of Dict 
                types have been deprecated as of v1.14.0.

            events (List[EventsCriteriaBlock or Dict]): 
                List of event criteria blocks, defaults to []. List items of Dict types have 
                been deprecated as of v1.14.0.

            conjunction_types (List[str]): 
                List of conjunction types, defaults to [] (meaning all conjunction types). Valid
                options are 'nbtrace' or 'sbtrace'. Defaults to 'nbtrace'.

            response_format (Dict): 
                JSON representation of desired data response format.

            poll_interval (bool): 
                Seconds to wait between polling calls, defaults to 1 second.

            return_immediately (bool): 
                Initiate the search and return without waiting for data to be received, defaults 
                to `False`.

            verbose (bool): 
                Show the progress of the request using the request log, defaults to `False`.

        Returns:
            A `pyaurorax.search.ConjunctionSearch` object

        Raises:
            pyaurorax.exceptions.AuroraXSearchError: The API experienced a search error
        """
        return func_search(
            self.__aurorax_obj,
            start,
            end,
            distance,
            ground,
            space,
            events,
            conjunction_types,
            response_format,
            poll_interval,
            return_immediately,
            verbose,
        )

    def describe(self, search_obj: Optional[ConjunctionSearch] = None, query_dict: Optional[Dict] = None) -> str:
        """
        Describe a conjunction search as an "SQL-like" string. Either a ConjunctionSearch
        object can be supplied, or a dictionary of the raw JSON query.

        Args:
            search_obj (ConjunctionSearch): 
                the conjunction search to describe, optional

            query_dict (Dict): 
                the conjunction search query represented as a raw dictionary, optional

        Returns:
            the "SQL-like" string describing the conjunction search object

        Raises:
            pyaurorax.exceptions.AuroraXError: invalid arguments
        """
        return func_describe(self.__aurorax_obj, search_obj, query_dict)

    def get_request_url(self, request_id: str) -> str:
        """
        Get the conjunction search request URL for a given request ID. This URL 
        can be used for subsequent pyaurorax.requests function calls. Primarily 
        this method facilitates delving into details about a set of already-submitted 
        conjunction searches.

        Args:
            request_id (str): 
                the request identifier

        Returns:
            the request URL
        """
        return func_get_request_url(self.__aurorax_obj, request_id)

    def create_advanced_distance_combos(
        self,
        distance: int,
        ground: int = 0,
        space: int = 0,
        events: int = 0,
    ) -> Dict:
        """
        Get the advanced distances combinations for the specified parameters

        Args:
            default_distance (int): 
                the default distance to use, defaults to None
            
            ground (int): 
                the number of ground criteria blocks, defaults to 0

            space (int): 
                the number of space criteria blocks, defaults to 0

            events (int): 
                the number of events criteria blocks, defaults to 0

        Returns:
            the advanced distances combinations
        """
        return func_create_advanced_distance_combos(distance, ground, space, events)
