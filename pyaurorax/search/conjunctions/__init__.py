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
    CustomLocationsCriteriaBlock,
)
from ._conjunctions import search as func_search
from ._conjunctions import search_from_raw_query as func_search_from_raw_query
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
               custom_locations: Sequence[Union[CustomLocationsCriteriaBlock, Dict]] = [],
               conjunction_types: Sequence[Union[str, Literal["nbtrace", "sbtrace", "geographic"]]] = [],
               response_format: Optional[Dict] = None,
               poll_interval: float = __STANDARD_POLLING_SLEEP_TIME,
               return_immediately: bool = False,
               verbose: bool = False) -> ConjunctionSearch:
        """
        Search for conjunctions

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
            custom_locations,
            conjunction_types,
            response_format,
            poll_interval,
            return_immediately,
            verbose,
        )

    def search_from_raw_query(self,
                              query: Union[Dict, str],
                              poll_interval: float = __STANDARD_POLLING_SLEEP_TIME,
                              return_immediately: bool = False,
                              verbose: bool = False) -> ConjunctionSearch:
        """
        Search for conjunctions, using a query dictionary as the input. 
        
        This is especially useful if you're working in the AuroraX Conjunction Search webpage 
        to create a search and you'd like to port it over to this Python library with ease.

        Args:
            query (Dict or str): 
                A query in dictionary or string format. If it's in string format, it should valid
                JSON.

                In the conjunction search web page (https://aurorax.space/conjunctionSearch/standard), 
                click on the 'More' button under the 'Tools' section on the right of the page. Then click 
                on 'About query' to bring up a modal. Copy the query in JSON format using the clipboard 
                icon, and use this JSON string as input to the function.

                Many JSON strings can be pasted as a dictionary object without any adjustments, however, 
                there are a few edge cases. For example, if the max_distances field has 'null' values in 
                it, then it is not valid Python. In this case, enclose the JSON in a multi-line string 
                (using the triple-quotes), and pass the query as a string to the function.

            poll_interval (bool): 
                Seconds to wait between polling calls, defaults to 1 second.

            return_immediately (bool): 
                Initiate the search and return without waiting for data to be received, defaults 
                to `False`.

            verbose (bool): 
                Show the progress of the request using the request log, defaults to `False`.

        Returns:
            A `ConjunctionSearch` object.

        Raises:
            pyaurorax.exceptions.AuroraXSearchError: An error was encountered during the search process
        """
        return func_search_from_raw_query(self.__aurorax_obj, query, poll_interval, return_immediately, verbose)

    def describe(self, search_obj: Optional[ConjunctionSearch] = None, query_dict: Optional[Dict] = None) -> str:
        """
        Describe a conjunction search as an "SQL-like" string. Either a ConjunctionSearch
        object can be supplied, or a dictionary of the raw JSON query.

        Args:
            search_obj (ConjunctionSearch): 
                The conjunction search to describe, optional

            query_dict (Dict): 
                The conjunction search query represented as a raw dictionary, optional

        Returns:
            The "SQL-like" string describing the conjunction search object

        Raises:
            pyaurorax.exceptions.AuroraXError: Invalid arguments
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
                The request identifier

        Returns:
            The request URL
        """
        return func_get_request_url(self.__aurorax_obj, request_id)

    def create_advanced_distance_combos(
        self,
        distance: Optional[int] = None,
        ground: int = 0,
        space: int = 0,
        events: int = 0,
        custom: int = 0,
    ) -> Dict:
        """
        Get the advanced distances combinations for the specified parameters

        Args:
            distance (int): 
                The default distance to use, defaults to None
            
            ground (int): 
                The number of ground criteria blocks, defaults to 0

            space (int): 
                The number of space criteria blocks, defaults to 0

            events (int): 
                The number of events criteria blocks, defaults to 0

            custom (int): 
                The number of custom location criteria blocks, defaults to 0

        Returns:
            The advanced distances combinations
        """
        return func_create_advanced_distance_combos(distance, ground, space, events, custom)

    def create_response_format_template(self, default: bool = True) -> Dict:
        """
        Generate a template dictionary that can be used as the response_format parameter
        in a conjunction search.

        Args:
            default (bool): 
                The default value to set for every parameter that can be returned, defaults
                to True.

        Returns:
            A template dictionary for the response format
        """
        return {
            "conjunction_type": default,
            "start": default,
            "end": default,
            "min_distance": default,
            "max_distance": default,
            "closest_epoch": default,
            "farthest_epoch": default,
            "data_sources": {
                "identifier": default,
                "program": default,
                "platform": default,
                "instrument_type": default,
                "source_type": default,
                "display_name": default,
                "ephemeris_metadata_schema": {
                    "field_name": default,
                    "description": default,
                    "data_type": default,
                    "allowed_values": default,
                    "additional_description": default
                },
                "data_product_metadata_schema": {
                    "field_name": default,
                    "description": default,
                    "data_type": default,
                    "allowed_values": default,
                    "additional_description": default
                },
                "owner": default,
                "maintainers": default,
                "metadata": default
            },
            "events": {
                "conjunction_type": default,
                "e1_source": {
                    "identifier": default,
                    "program": default,
                    "platform": default,
                    "instrument_type": default,
                    "source_type": default,
                    "display_name": default,
                    "ephemeris_metadata_schema": {
                        "field_name": default,
                        "description": default,
                        "data_type": default,
                        "allowed_values": default,
                        "additional_description": default
                    },
                    "data_product_metadata_schema": {
                        "field_name": default,
                        "description": default,
                        "data_type": default,
                        "allowed_values": default,
                        "additional_description": default
                    },
                    "owner": default,
                    "maintainers": default,
                    "metadata": default
                },
                "e2_source": {
                    "identifier": default,
                    "program": default,
                    "platform": default,
                    "instrument_type": default,
                    "source_type": default,
                    "display_name": default,
                    "ephemeris_metadata_schema": {
                        "field_name": default,
                        "description": default,
                        "data_type": default,
                        "allowed_values": default,
                        "additional_description": default
                    },
                    "data_product_metadata_schema": {
                        "field_name": default,
                        "description": default,
                        "data_type": default,
                        "allowed_values": default,
                        "additional_description": default
                    },
                    "owner": default,
                    "maintainers": default,
                    "metadata": default
                },
                "start": default,
                "end": default,
                "min_distance": default,
                "max_distance": default,
                "generated_e1_ephemeris_query": {
                    "request_id": default,
                    "data_sources": {
                        "programs": default,
                        "platforms": default,
                        "instrument_types": default,
                        "ephemeris_metadata_filters": {
                            "logicalOperator": default,
                            "expressions": {
                                "key": default,
                                "operator": default,
                                "values": default
                            }
                        }
                    },
                    "start": default,
                    "end": default
                },
                "generated_e2_ephemeris_query": {
                    "request_id": default,
                    "data_sources": {
                        "programs": default,
                        "platforms": default,
                        "instrument_types": default,
                        "ephemeris_metadata_filters": {
                            "logicalOperator": default,
                            "expressions": {
                                "key": default,
                                "operator": default,
                                "values": default
                            }
                        }
                    },
                    "start": default,
                    "end": default
                }
            }
        }
