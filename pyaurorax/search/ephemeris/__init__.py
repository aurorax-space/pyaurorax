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
from typing import Dict, List, Optional, Union, Literal
from .classes.ephemeris import EphemerisData
from .classes.search import EphemerisSearch
from ..metadata_filters import MetadataFilter
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
               metadata_filters: Optional[Union[MetadataFilter, List[Dict]]] = None,
               metadata_filters_logical_operator: Optional[Literal["and", "or", "AND", "OR"]] = None,
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
            start (datetime.datetime): 
                Start timestamp of the search (inclusive)

            end (datetime.datetime): 
                End timestamp of the search (inclusive)

            programs (List[str]): 
                List of programs to search through, defaults to None

            platforms (List[str]): 
                List of platforms to search through, defaults to None

            instrument_types (List[str]): 
                List of instrument types to search through, defaults to None

            metadata_filters (MetadataFilter or List[Dict]): 
                The metadata filters to use when searching, defaults to None

            metadata_filters_logical_operator (str): 
                The logical operator to use when evaluating metadata filters (either `and` or `or`), 
                defaults to `and`. This parameter is deprecated in exchange for passing a 
                MetadataFilter object into the metadata_filters parameter. 

            response_format (Dict): 
                JSON representation of desired data response format

            poll_interval (float): 
                Time in seconds to wait between polling attempts, defaults to 1 second

            return_immediately (bool): 
                Initiate the search and return without waiting for data to be received, defaults to False

            verbose (bool): 
                Output poll times and other progress messages, defaults to False

        Returns:
            A `pyaurorax..search.EphemerisSearch` object

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        # return
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
            identifier (int): 
                AuroraX data source ID

            records (List[EphemerisData]): 
                Ephemeris records to upload

            validate_source (bool): 
                Validate all records before uploading, defaults to False

            chunk_size (int): 
                Number of records to upload in a single call, defaults to 500

        Returns:
            0 for success, raises exception on error

        Raises:
            pyaurorax.exceptions.AuroraXUploadError: Upload error
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        return func_upload(self.__aurorax_obj, identifier, records, validate_source, chunk_size)

    def delete(self, data_source: DataSource, start: datetime.datetime, end: datetime.datetime) -> int:
        """
        Delete ephemeris records between a timeframe.

        The API processes this request asynchronously, so this method will return
        immediately whether or not the data has already been deleted.

        Args:
            data_source (DataSource): 
                Data source associated with the data product records (note that
                identifier, program, platform, and instrument_type are required)

            start (datetime.datetime): 
                Timestamp marking beginning of range to delete records for, inclusive
            
            end (datetime.datetime): 
                Timestamp marking end of range to delete records for, inclusive

        Returns:
            0 on success

        Raises:
            pyaurorax.exceptions.AuroraXNotFoundError: Source not found
            pyaurorax.exceptions.AuroraXUnauthorizedError: Invalid API key for this operation
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        return func_delete(self.__aurorax_obj, data_source, start, end)

    def describe(self, search_obj: Optional[EphemerisSearch] = None, query_dict: Optional[Dict] = None) -> str:
        """
        Describe an ephemeris search as an "SQL-like" string. Either a EphemerisSearch
        object can be supplied, or a dictionary of the raw JSON query.

        Args:
            search_obj (EphemerisSearch): 
                The ephemeris search to describe, optional

            query_dict (Dict): 
                The ephemeris search query represented as a raw dictionary, optional

        Returns:
            The "SQL-like" string describing the ephemeris search object
        """
        return func_describe(self.__aurorax_obj, search_obj, query_dict)

    def get_request_url(self, request_id: str) -> str:
        """
        Get the ephemeris search request URL for a given request ID. This URL can be 
        used for subsequent pyaurorax.requests function calls. Primarily this method 
        facilitates delving into details about a set of already-submitted ephemeris 
        searches.

        Args:
            request_id (str): 
                The request identifier

        Returns:
            The request URL
        """
        return func_get_request_url(self.__aurorax_obj, request_id)

    def create_response_format_template(self, default: bool = True) -> Dict:
        """
        Generate a template dictionary that can be used as the response_format parameter
        in an ephemeris search.

        Args:
            default (bool): 
                The default value to set for every parameter that can be returned, defaults
                to True.

        Returns:
            A template dictionary for the response format
        """
        return {
            "data_source": {
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
            "epoch": default,
            "location_geo": {
                "lat": default,
                "lon": default
            },
            "location_gsm": {
                "lat": default,
                "lon": default
            },
            "nbtrace": {
                "lat": default,
                "lon": default
            },
            "sbtrace": {
                "lat": default,
                "lon": default
            },
            "metadata": default
        }
