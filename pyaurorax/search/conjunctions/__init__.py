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
from typing import Dict, List, Optional, Union
from .swarmaurora import SwarmAuroraManager
from .classes.search import ConjunctionSearch
from ._conjunctions import search as func_search
from ._conjunctions import describe as func_describe
from ._conjunctions import get_request_url as func_get_request_url

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
               ground: Optional[List[Dict]] = [],
               space: Optional[List[Dict]] = [],
               events: Optional[List[Dict]] = [],
               conjunction_types: Optional[List[str]] = [],
               epoch_search_precision: Optional[int] = 60,
               response_format: Optional[Dict] = None,
               poll_interval: Optional[float] = __STANDARD_POLLING_SLEEP_TIME,
               return_immediately: Optional[bool] = False,
               verbose: Optional[bool] = False) -> ConjunctionSearch:
        """
        Search for conjunctions between data sources

        By default, this function will block and wait until the request completes and
        all data is downloaded. If you don't want to wait, set the 'return_immediately`
        value to True. The Search object will be returned right after the search has been
        started, and you can use the helper functions as part of that object to get the
        data when it's done.

        Args:
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
            conjunction_types: list of conjunction types, defaults to [] (meaning all conjunction
                types). Options are in the pyaurorax.conjunctions module, or at the top level using
                the pyaurorax.CONJUNCTION_TYPE_* variables.
            epoch_search_precision: the time precision to which conjunctions are calculated. Can be
                30 or 60 seconds. Defaults to 60 seconds. Note - this parameter is under active
                development and still considered "alpha".
            response_format: JSON representation of desired data response format
            poll_interval: seconds to wait between polling calls, defaults to
                pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME
            return_immediately: initiate the search and return without waiting for data to
                be received, defaults to False
            verbose: show the progress of the request using the request log, defaults

        Returns:
            a `pyaurorax.search.ConjunctionSearch` object
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
            epoch_search_precision,
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
            search_obj: the conjunction search to describe, optional
            query_dict: the conjunction search query represented as a raw dictionary, optional

        Returns:
            the "SQL-like" string describing the conjunction search object
        """
        return func_describe(self.__aurorax_obj, search_obj, query_dict)

    def get_request_url(self, request_id: str) -> str:
        """
        Get the conjunction search request URL for a given
        request ID. This URL can be used for subsequent
        pyaurorax.requests function calls. Primarily this method
        facilitates delving into details about a set of already-submitted
        conjunction searches.

        Args:
            request_id: the request identifier

        Returns:
            the request URL
        """
        return func_get_request_url(self.__aurorax_obj, request_id)
