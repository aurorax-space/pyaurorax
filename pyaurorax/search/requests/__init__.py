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
Helper methods for retrieving data from an AuroraX search engine API 
request.

Note that all functions and classes from submodules are all imported
at this level of the requests module. They can be referenced from
here instead of digging in deeper to the submodules.
"""

import datetime
from typing import Dict, List, Optional
from ._requests import get_status as func_get_status
from ._requests import get_data as func_get_data
from ._requests import get_logs as func_get_logs
from ._requests import wait_for_data as func_wait_for_data
from ._requests import list as func_list
from ._requests import delete as func_delete
from ._requests import cancel as func_cancel

__all__ = ["RequestsManager"]


class RequestsManager:
    """
    The RequestsManager object is initialized within every PyAuroraX object. It acts as a way to access 
    the submodules and carry over configuration information in the super class.
    """

    __STANDARD_POLLING_SLEEP_TIME: float = 1.0  # Polling sleep time when waiting for data (after the initial sleep time), in seconds

    def __init__(self, aurorax_obj):
        self.__aurorax_obj = aurorax_obj

    def get_status(self, request_url: str) -> Dict:
        """
        Retrieve the status of a request

        Args:
            request_url: the URL of the request information

        Returns:
            the status information for the request
        """
        return func_get_status(self.__aurorax_obj, request_url)

    def get_data(self, data_url: str, response_format: Optional[Dict] = None, skip_serializing: bool = False) -> List:
        """
        Retrieve the data for a request

        Args:
            data_url: the URL for the data of a request,
            response_format: the response format to send as post data, defaults
                to None
            skip_serializing: skip any object serializing, defaults to False

        Raises:
            pyaurorax.exceptions.AuroraXDataRetrievalError: error retrieving data

        Returns:
            the data for this request
        """
        return func_get_data(self.__aurorax_obj, data_url, response_format, skip_serializing)

    def get_logs(self, request_url: str) -> List:
        """
        Retrieve the logs for a request

        Args:
            request_url: the URL of the request information

        Returns:
            the log messages for the request
        """
        return func_get_logs(self.__aurorax_obj, request_url)

    def wait_for_data(self, request_url: str, poll_interval: float = __STANDARD_POLLING_SLEEP_TIME, verbose: bool = False) -> Dict:
        """
        Block and wait for the data to be made available for a request

        Args:
            request_url: the URL of the request information
            poll_interval: seconds to wait between polling calls, defaults
                to STANDARD_POLLING_SLEEP_TIME
            verbose: output poll times and other progress messages, defaults to False

        Returns:
            the status information for the request
        """
        return func_wait_for_data(self.__aurorax_obj, request_url, poll_interval, verbose)

    def cancel(self, request_url: str, wait: bool = False, poll_interval: float = __STANDARD_POLLING_SLEEP_TIME, verbose: bool = False) -> int:
        """
        Cancel the request at the given URL.

        This method returns immediately by default since the API processes
        this request asynchronously. If you would prefer to wait for it
        to be completed, set the 'wait' parameter to True. You can adjust
        the polling time using the 'poll_interval' parameter.

        Args:
            request_url: the URL string of the request to be canceled
            wait: set to True to block until the cancellation request
                has been completed (may wait for several minutes)
            poll_interval: seconds to wait between polling
                calls, defaults to STANDARD_POLLING_SLEEP_TIME.
            verbose: if True then output poll times and other
                progress, defaults to False

        Returns:
            0 on success

        Raises:
            pyaurorax.exceptions.AuroraXUnauthorizedError: invalid API key for this operation
            pyaurorax.exceptions.AuroraXAPIError: An API error was encountered
        """
        return func_cancel(self.__aurorax_obj, request_url, wait, poll_interval, verbose)

    def list(self,
             search_type: Optional[str] = None,
             active: Optional[bool] = None,
             start: Optional[datetime.datetime] = None,
             end: Optional[datetime.datetime] = None,
             file_size: Optional[int] = None,
             result_count: Optional[int] = None,
             query_duration: Optional[int] = None,
             error_condition: Optional[bool] = None) -> List:
        """
        Retrieve a list of search requests matching certain criteria.  Administrators only.

        Args:
            search_type: the type of search request, valid values are 'conjunction',
                'ephemeris', or 'data_product'. Exclusion of value will return all
                search requests of any type, defaults to None
            active: return searches that are currently active or not, exclude for
                both, defaults to None
            start: start timestamp for narrowing down search timeframes, defaults to None
            end: end timestamp for narrowing down search timeframes, defaults to None
            file_size: filter by result file size, measured in KB, defaults to None
            result_count: filter by result count, defaults to None
            query_duration: filter by query duration, measured in milliseconds, defaults
                to None
            error_condition: filter by if an error occurred or not, exclude for both,
                defaults to None

        Returns:
            list of matching search requests

        Raises:
            pyaurorax.exceptions.AuroraXUnauthorizedError: invalid API key for this operation
        """
        return func_list(self.__aurorax_obj, search_type, active, start, end, file_size, result_count, query_duration, error_condition)

    def delete(self, request_id: str) -> int:
        """
        Entirely remove a search request from the AuroraX
        database. Administrators only.

        Args:
            request_id: search request UUID

        Returns:
            0 on success, raises error on failure

        Raises:
            pyaurorax.exceptions.AuroraXNotFoundError: data source not found
        """
        return func_delete(self.__aurorax_obj, request_id)
