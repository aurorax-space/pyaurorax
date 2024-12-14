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
Class definition for an ephemeris search
"""

from __future__ import annotations
import datetime
from typing import TYPE_CHECKING, Dict, List, Optional, Literal
from .ephemeris import EphemerisData
from ...api import AuroraXAPIRequest
from ...sources.classes.data_source import DataSource, FORMAT_BASIC_INFO
from ....exceptions import AuroraXError, AuroraXAPIError
from ...requests._requests import (
    cancel as requests_cancel,
    wait_for_data as requests_wait_for_data,
    get_data as requests_get_data,
    get_status as requests_get_status,
)
if TYPE_CHECKING:
    from ....pyaurorax import PyAuroraX


class EphemerisSearch:
    """
    Class representing an ephemeris search

    Note: At least one search criteria from programs, platforms, or instrument_types
    must be specified.

    Args:
        start: start timestamp of the search (inclusive)
        end: end timestamp of the search (inclusive)
        programs: list of programs to search through, defaults to None
        platforms: list of platforms to search through, defaults to None
        instrument_types: list of instrument types to search through, defaults to None
        metadata_filters: list of dictionaries describing metadata keys and
            values to filter on, defaults to None

            e.g. {
                "key": "string",
                "operator": "=",
                "values": [
                    "string"
                ]
            }
        metadata_filters_logical_operator: the logical operator to use when
            evaluating metadata filters (either 'AND' or 'OR'), defaults
            to "AND"
        response_format: JSON representation of desired data response format
        request: AuroraXResponse object returned when the search is executed
        request_id: unique ID assigned to the request by the AuroraX API
        request_url: unique URL assigned to the request by the AuroraX API
        executed: indicates if the search has been executed/started
        completed: indicates if the search has finished
        data_url: the URL where data is accessed
        query: the query for this request as JSON
        status: the status of the query
        data: the ephemeris records found
        logs: all log messages outputted by the AuroraX API for this request
    """

    __STANDARD_POLLING_SLEEP_TIME: float = 1.0

    def __init__(self,
                 aurorax_obj: PyAuroraX,
                 start: datetime.datetime,
                 end: datetime.datetime,
                 programs: Optional[List[str]] = None,
                 platforms: Optional[List[str]] = None,
                 instrument_types: Optional[List[str]] = None,
                 metadata_filters: Optional[List[Dict]] = None,
                 metadata_filters_logical_operator: Optional[Literal["AND", "OR"]] = None,
                 response_format: Optional[Dict] = None) -> None:

        # set variables using passed in args
        self.aurorax_obj = aurorax_obj
        self.start = start
        self.end = end
        self.programs = programs
        self.platforms = platforms
        self.instrument_types = instrument_types
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
        self.query = {}
        self.status = {}
        self.data = []
        self.logs = []

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "EphemerisSearch(executed=%s, completed=%s, request_id='%s')" % (
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
                data_str = "[0 ephemeris results]"
            elif (len(self.data) == 1):
                data_str = "[1 ephemeris result]"
            else:
                data_str = "[%d ephemeris results]" % (len(self.data))
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
        print("EphemerisSearch:")
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
        self._query = {
            "data_sources": {
                "programs": [] if not self.programs else self.programs,
                "platforms": [] if not self.platforms else self.platforms,
                "instrument_types": [] if not self.instrument_types else self.instrument_types,
                "ephemeris_metadata_filters": {} if not self.metadata_filters else {
                    "logical_operator": self.metadata_filters_logical_operator,
                    "expressions": self.metadata_filters
                },
            },
            "start": self.start.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": self.end.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        return self._query

    @query.setter
    def query(self, query):
        self._query = query

    def execute(self) -> None:
        """
        Initiate ephemeris search request

        Raises:
            pyaurorax.exceptions.AuroraXError: invalid request parameters are set
        """
        # check for at least one filter criteria
        if not (self.programs or self.platforms or self.instrument_types or self.metadata_filters):
            raise AuroraXError("At least one filter criteria parameter besides 'start' and 'end' must be specified")

        # do request
        url = "%s/%s" % (self.aurorax_obj.api_base_url, self.aurorax_obj.search.api.URL_SUFFIX_EPHEMERIS_SEARCH)
        req = AuroraXAPIRequest(self.aurorax_obj, method="post", url=url, body=self.query, null_response=True)
        res = req.execute()

        # set request ID, request_url, executed
        self.executed = True
        if (res.status_code == 202):
            # request successfully dispatched
            self.executed = True
            self.request_url = res.request.headers["location"]
            self.request_id = self.request_url.rsplit("/", 1)[-1]

        # set the request variable
        self.request = res

    def update_status(self, status: Optional[Dict] = None) -> None:
        """
        Update the status of this ephemeris search request

        Args:
            status: the previously-retrieved status of this request (include
                to avoid requesting it from the API again), defaults to None
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
        Check to see if data is available for this ephemeris
        search request

        Returns:
            True if data is available, else False
        """
        self.update_status()
        return self.completed

    def get_data(self) -> None:
        """
        Retrieve the data available for this ephemeris search request
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
                ds = DataSource(**raw_data[i]["data_source"], format=FORMAT_BASIC_INFO)
                raw_data[i]["data_source"] = ds

            # cast ephemeris objects
            self.data = [EphemerisData(**e) for e in raw_data]

    def wait(self, poll_interval: float = __STANDARD_POLLING_SLEEP_TIME, verbose: bool = False) -> None:
        """
        Block and wait for the request to complete and data is
        available for retrieval

        Args:
            poll_interval: time in seconds to wait between polling attempts,
                defaults to pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME
            verbose: output poll times and other progress messages, defaults
                to False
        """
        url = "%s/%s" % (self.aurorax_obj.api_base_url, self.aurorax_obj.search.api.URL_SUFFIX_EPHEMERIS_REQUEST.format(self.request_id))
        self.update_status(requests_wait_for_data(self.aurorax_obj, url, poll_interval, verbose))

    def cancel(self, wait: bool = False, poll_interval: float = __STANDARD_POLLING_SLEEP_TIME, verbose: bool = False) -> int:
        """
        Cancel the ephemeris search request

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
            pyaurorax.exceptions.AuroraXUnauthorizedError: invalid API key for this operation
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        url = "%s/%s" % (self.aurorax_obj.api_base_url, self.aurorax_obj.search.api.URL_SUFFIX_EPHEMERIS_REQUEST.format(self.request_id))
        return requests_cancel(self.aurorax_obj, url, wait, poll_interval, verbose)
