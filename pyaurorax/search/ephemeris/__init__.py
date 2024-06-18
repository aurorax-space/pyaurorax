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
Use the AuroraX search engine to search and upload ephemeris records.

Note that all functions and classes from submodules are all imported
at this level of the ephemeris module. They can be referenced from
here instead of digging in deeper to the submodules.
"""

import datetime
from typing import Dict, List, Optional
from .classes.ephemeris import EphemerisData
from .classes.search import EphemerisSearch
from ..sources.classes.data_source import DataSource
from ._ephemeris import search as func_search
from ._ephemeris import upload as func_upload
from ._ephemeris import delete as func_delete
from ._ephemeris import describe as func_describe
from ._ephemeris import get_request_url as func_get_request_url

__all__ = ["EphemerisManager"]


class EphemerisManager:
    """
    The EphemerisManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    __STANDARD_POLLING_SLEEP_TIME: float = 1.0  # polling sleep time when waiting for data (after the initial sleep time), in seconds
    __UPLOAD_CHUNK_SIZE = 500  # number of ephemeris records to upload at a time

    def __init__(self, aurorax_obj):
        self.__aurorax_obj = aurorax_obj

    def search(self,
               start: datetime.datetime,
               end: datetime.datetime,
               programs: Optional[List[str]] = None,
               platforms: Optional[List[str]] = None,
               instrument_types: Optional[List[str]] = None,
               metadata_filters: Optional[List[Dict]] = None,
               metadata_filters_logical_operator: Optional[str] = None,
               response_format: Optional[Dict] = None,
               poll_interval: float = __STANDARD_POLLING_SLEEP_TIME,
               return_immediately: bool = False,
               verbose: bool = False) -> EphemerisSearch:
        """
        Search for ephemeris records

        By default, this function will block and wait until the request completes and
        all data is downloaded. If you don't want to wait, set the 'return_immediately`
        value to True. The Search object will be returned right after the search has been
        started, and you can use the helper functions as part of that object to get the
        data when it's done.

        Note: At least one search criteria from programs, platforms, or
        instrument_types, must be specified.

        Args:
            start: start timestamp of the search (inclusive)
            end: end timestamp of the search (inclusive)
            programs: list of programs to search through, defaults to None
            platforms: list of platforms to search through, defaults to None
            instrument_types: list of instrument types to search through, defaults to None
            metadata_filters: list of dictionaries describing metadata keys and
                values to filter on, defaults to None

                Example:

                    [{
                        "key": "nbtrace_region",
                        "operator": "in",
                        "values": ["north polar cap"]
                    }]
            metadata_filters_logical_operator: the logical operator to use when
                evaluating metadata filters (either 'AND' or 'OR'), defaults
                to "AND"
            response_format: JSON representation of desired data response format
            poll_interval: time in seconds to wait between polling attempts, defaults
                to pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME
            return_immediately: initiate the search and return without waiting for data to
                be received, defaults to False
            verbose: output poll times and other progress messages, defaults to False

        Returns:
            A `pyaurorax..search.EphemerisSearch` object

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        return func_search(
            self.__aurorax_obj,
            start,
            end,
            programs,
            platforms,
            instrument_types,
            metadata_filters,
            metadata_filters_logical_operator,
            response_format,
            poll_interval,
            return_immediately,
            verbose,
        )

    def upload(self, identifier: int, records: List[EphemerisData], validate_source: bool = False, chunk_size: int = __UPLOAD_CHUNK_SIZE) -> int:
        """
        Upload ephemeris records to AuroraX

        Args:
            identifier: AuroraX data source ID
            records: ephemeris records to upload
            validate_source: validate all records before uploading, defaults to False
            chunk_size: number of records to upload in a single call, defaults to 500

        Returns:
            0 for success, raises exception on error

        Raises:
            pyaurorax.exceptions.AuroraXUploadError: upload error
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        return func_upload(self.__aurorax_obj, identifier, records, validate_source, chunk_size)

    def delete(self, data_source: DataSource, start: datetime.datetime, end: datetime.datetime) -> int:
        """
        Delete ephemeris records between a timeframe.

        The API processes this request asynchronously, so this method will return
        immediately whether or not the data has already been deleted.

        Args:
            data_source: data source associated with the data product records (note that
                identifier, program, platform, and instrument_type are required)
            start: timestamp marking beginning of range to delete records for, inclusive
            end: timestamp marking end of range to delete records for, inclusive

        Returns:
            0 on success

        Raises:
            pyaurorax.exceptions.AuroraXNotFoundError: source not found
            pyaurorax.exceptions.AuroraXUnauthorizedError: invalid API key for this operation
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        return func_delete(self.__aurorax_obj, data_source, start, end)

    def describe(self, search_obj: Optional[EphemerisSearch] = None, query_dict: Optional[Dict] = None) -> str:
        """
        Describe an ephemeris search as an "SQL-like" string. Either a EphemerisSearch
        object can be supplied, or a dictionary of the raw JSON query.

        Args:
            search_obj: the ephemeris search to describe, optional
            query_dict: the ephemeris search query represented as a raw dictionary, optional

        Returns:
            the "SQL-like" string describing the ephemeris search object
        """
        return func_describe(self.__aurorax_obj, search_obj, query_dict)

    def get_request_url(self, request_id: str) -> str:
        """
        Get the ephemeris search request URL for a given
        request ID. This URL can be used for subsequent
        pyaurorax.requests function calls. Primarily this method
        facilitates delving into details about a set of already-submitted
        ephemeris searches.

        Args:
            request_id: the request identifier

        Returns:
            the request URL
        """
        return func_get_request_url(self.__aurorax_obj, request_id)
