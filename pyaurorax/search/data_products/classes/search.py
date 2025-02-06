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
Class definition for a data product search
"""

from __future__ import annotations
import datetime
from typing import TYPE_CHECKING, Dict, List, Optional, Literal, Union
from .data_product import DataProductData
from ...metadata_filters import MetadataFilter
from ...api import AuroraXAPIRequest
from ...sources import DataSource, FORMAT_BASIC_INFO
from ....exceptions import AuroraXAPIError
from ...requests._requests import (
    cancel as requests_cancel,
    wait_for_data as requests_wait_for_data,
    get_data as requests_get_data,
    get_status as requests_get_status,
)
from ...._util import show_warning
if TYPE_CHECKING:
    from ....pyaurorax import PyAuroraX  # pragma: nocover-ok


class DataProductSearch:
    """
    Class representing a data product search

    Attributes:
        start (datetime.datetime): 
            Start timestamp of the search (inclusive)

        end (datetime.datetime): 
            End timestamp of the search (inclusive)

        programs (List[str]): 
            List of program names to search

        platforms (List[str]): 
            List of platform names to search

        instrument_types (List[str]): 
            List of instrument types to search

        data_product_types (List[str]): 
            List of strings describing data product types to filter on e.g. "keogram", defaults 
            to None. Valid options are: `keogram`, `montage`, `movie`, `summary_plot`, and 
            `data_availability`.
    
        metadata_filters (MetadataFilter or List[Dict]): 
            The metadata filters to use when searching, defaults to None

        metadata_filters_logical_operator (str): 
            The logical operator to use when evaluating metadata filters (either `and` or `or`), 
            defaults to `and`. This parameter is deprecated in exchange for passing a 
            MetadataFilter object into the metadata_filters parameter. 

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

        data (List[DataProductData]): 
            The data product records found

        logs (List[Dict]): 
            All log messages outputted by the AuroraX API for this request
    """

    __STANDARD_POLLING_SLEEP_TIME: float = 1.0

    def __init__(self,
                 aurorax_obj: PyAuroraX,
                 start: datetime.datetime,
                 end: datetime.datetime,
                 programs: Optional[List[str]] = None,
                 platforms: Optional[List[str]] = None,
                 instrument_types: Optional[List[str]] = None,
                 data_product_types: Optional[List[Literal["keogram", "montage", "movie", "summary_plot", "data_availability"]]] = None,
                 metadata_filters: Optional[Union[MetadataFilter, List[Dict]]] = None,
                 metadata_filters_logical_operator: Optional[Literal["and", "or", "AND", "OR"]] = None,
                 response_format: Optional[Dict] = None) -> None:

        # show warnings
        if (isinstance(metadata_filters, MetadataFilter) and metadata_filters_logical_operator is not None):
            # logical operator supplied, but MetadataFilter supplied too
            show_warning("Supplying a MetadataFilter object in addition to the metadata_filters_logical_operator " +
                         "parameter is redundant. Only the MetadataFilter object is needed. The " +
                         "metadata_filters_logical_operator parameter will be ignored")

        # set variables using passed in args
        self.__aurorax_obj = aurorax_obj
        self.start = start
        self.end = end
        self.programs = programs
        self.platforms = platforms
        self.instrument_types = instrument_types
        self.data_product_types = data_product_types
        self.metadata_filters = metadata_filters
        self.metadata_filters_logical_operator = "AND" if metadata_filters_logical_operator is None else metadata_filters_logical_operator
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

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "DataProductSearch(executed=%s, completed=%s, request_id='%s')" % (
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
                data_str = "[1 data product result]"
            else:
                data_str = "[%d data product results]" % (len(self.data))
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
        print("DataProductSearch:")
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

    @property
    def query(self):
        """
        Property for the query value
        """
        # set metadata filter value
        if (self.metadata_filters is None):
            metadata_filters_dict = {}
        elif (isinstance(self.metadata_filters, MetadataFilter) is True):
            # metadata filter is a class
            metadata_filters_dict = self.metadata_filters.to_query_dict()  # type: ignore
        else:
            # metadata filter is a dictionary
            metadata_filters_dict = {
                "expressions": self.metadata_filters,
                "logical_operator": self.metadata_filters_logical_operator,
            }

        # set query
        self.__query = {
            "data_sources": {
                "programs": [] if not self.programs else self.programs,
                "platforms": [] if not self.platforms else self.platforms,
                "instrument_types": [] if not self.instrument_types else self.instrument_types,
                "data_product_metadata_filters": metadata_filters_dict,
            },
            "start": self.start.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": self.end.strftime("%Y-%m-%dT%H:%M:%S"),
            "data_product_type_filters": [] if not self.data_product_types else self.data_product_types,
        }

        # return
        return self.__query

    def execute(self) -> None:
        """
        Initiate a data product search request
        """
        # do request
        url = "%s/%s" % (self.__aurorax_obj.api_base_url, self.__aurorax_obj.search.api.URL_SUFFIX_DATA_PRODUCTS_SEARCH)
        req = AuroraXAPIRequest(self.__aurorax_obj, method="post", url=url, body=self.query, null_response=True)
        res = req.execute()

        # set request ID, request_url, executed
        self.executed = True
        if (res.status_code == 202):
            # request successfully dispatched
            self.executed = True
            self.request_url = res.request.headers["location"]
            self.request_id = self.request_url.rsplit("/", 1)[-1]

        # set request variable
        self.request = res

    def update_status(self, status: Optional[Dict] = None) -> None:
        """
        Update the status of this data product search request

        Args:
            status (Dict): 
                The previously-retrieved status of this request (include
                to avoid requesting it from the API again), defaults to None
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
        Check to see if data is available for this data product
        search request

        Returns:
            True if data is available, else False
        """
        self.update_status()
        return self.completed

    def get_data(self) -> None:
        """
        Retrieve the data available for this data product search request
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
                ds = DataSource(**raw_data[i]["data_source"], format=FORMAT_BASIC_INFO)
                raw_data[i]["data_source"] = ds

            # cast data product objects
            self.data = [DataProductData(**dp) for dp in raw_data]

    def wait(self, poll_interval: float = __STANDARD_POLLING_SLEEP_TIME, verbose: bool = False) -> None:
        """
        Block and wait for the request to complete and data is available
        for retrieval

        Args:
            poll_interval (float): 
                Time in seconds to wait between polling attempts, defaults to 1 second

            verbose (bool): 
                Output poll times and other progress messages, defaults to False
        """
        url = "%s/%s" % (self.__aurorax_obj.api_base_url, self.__aurorax_obj.search.api.URL_SUFFIX_DATA_PRODUCTS_REQUEST.format(self.request_id))
        self.update_status(requests_wait_for_data(self.__aurorax_obj, url, poll_interval, verbose))

    def cancel(self, wait: bool = False, poll_interval: float = __STANDARD_POLLING_SLEEP_TIME, verbose: bool = False) -> int:
        """
        Cancel the data product search request

        This method returns immediately by default since the API processes
        this request asynchronously. If you would prefer to wait for it
        to be completed, set the 'wait' parameter to True. You can adjust
        the polling time using the 'poll_interval' parameter.

        Args:
            wait (bool): 
                Wait until the cancellation request has been completed (may wait 
                for several minutes)
            
            poll_interval (float): 
                Seconds to wait between polling calls, defaults to 1 second.
            
            verbose (bool): 
                Output poll times and other progress messages, defaults to False

        Returns:
            1 on success

        Raises:
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
            pyaurorax.exceptions.AuroraXUnauthorizedError: Invalid API key for this operation
        """
        url = "%s/%s" % (self.__aurorax_obj.api_base_url, self.__aurorax_obj.search.api.URL_SUFFIX_DATA_PRODUCTS_REQUEST.format(self.request_id))
        return requests_cancel(self.__aurorax_obj, url, wait, poll_interval, verbose)

    def describe(self):
        """
        Describe the data products search as an "SQL-like" string.

        Returns:
            The "SQL-like" string describing the data products search object
        """
        # make request
        url = "%s/%s" % (self.__aurorax_obj.api_base_url, self.__aurorax_obj.search.api.URL_SUFFIX_DESCRIBE_DATA_PRODUCTS_QUERY)
        req = AuroraXAPIRequest(self.__aurorax_obj, method="post", url=url, body=self.query)
        res = req.execute()

        # return
        return res.data
