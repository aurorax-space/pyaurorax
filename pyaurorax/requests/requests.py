"""
Functions for interacting with AuroraX requests
"""

import datetime
import time
import warnings
from typing import Dict, List, Optional, Any
from ..api.classes.request import AuroraXRequest
from ..api import urls
from ..exceptions import (
    AuroraXDataRetrievalException,
    AuroraXException,
    AuroraXUnauthorizedException)
from ..location import Location

# pdoc init
__pdoc__: Dict = {}

# globals
FIRST_FOLLOWUP_SLEEP_TIME: float = 0.050  # 50ms
""" Initial sleep time when waiting for data """

STANDARD_POLLING_SLEEP_TIME: float = 1.0  # 1s
""" Polling sleep time when waiting for data (after the initial sleep time) """

ALLOWED_SEARCH_LISTING_TYPES = ["conjunction", "data_product", "ephemeris"]
""" Allowed types when listing search requests """


def get_status(request_url: str) -> Dict:
    """
    Retrieve the status of a request

    Args:
        request_url: the URL of the request information

    Returns:
        the status information for the request
    """
    # do request
    req = AuroraXRequest(method="get", url=request_url)
    res = req.execute()

    # return
    return res.data


def get_data(data_url: str,
             response_format: Optional[Dict] = None,
             skip_serializing: Optional[bool] = False) -> List:
    """
    Retrieve the data for a request

    Args:
        data_url: the URL for the data of a request,
        response_format: the response format to send as post data, defaults
            to None
        skip_serializing: skip any object serializing, defaults to False

    Raises:
        pyaurorax.exceptions.AuroraXDataRetrievalException: error retrieving data

    Returns:
        the data for this request
    """
    # do request
    if (response_format is not None):
        req = AuroraXRequest(method="post",
                             url=data_url,
                             body=response_format)
    else:
        req = AuroraXRequest(method="get", url=data_url)
    res = req.execute()

    # check for error message
    if ("error" in res.data):
        raise AuroraXDataRetrievalException("%s: %s" % (res.data["error"]["error_code"],
                                                        res.data["error"]["error_message"]))

    # set data var
    data_result = res.data["result"]

    # serialize epochs and locations into datetimes and Locations
    if (skip_serializing is False):
        for i in range(0, len(data_result)):
            if ("epoch" in data_result[i]):
                data_result[i]["epoch"] = datetime.datetime.strptime(data_result[i]["epoch"],
                                                                     "%Y-%m-%dT%H:%M:%S")
            if ("location_geo" in data_result[i]):
                data_result[i]["location_geo"] = Location(lat=data_result[i]["location_geo"]["lat"],
                                                          lon=data_result[i]["location_geo"]["lon"])
            if ("location_gsm" in data_result[i]):
                data_result[i]["location_gsm"] = Location(lat=data_result[i]["location_gsm"]["lat"],
                                                          lon=data_result[i]["location_gsm"]["lon"])
            if ("nbtrace" in data_result[i]):
                data_result[i]["nbtrace"] = Location(lat=data_result[i]["nbtrace"]["lat"],
                                                     lon=data_result[i]["nbtrace"]["lon"])
            if ("sbtrace" in data_result[i]):
                data_result[i]["sbtrace"] = Location(lat=data_result[i]["sbtrace"]["lat"],
                                                     lon=data_result[i]["sbtrace"]["lon"])

    # return
    return data_result


def get_logs(request_url: str) -> List:
    """
    Retrieve the logs for a request

    Args:
        request_url: the URL of the request information

    Returns:
        the log messages for the request
    """
    # get status
    status = get_status(request_url)

    # return
    if ("logs" in status):
        return status["logs"]
    else:
        return []


def wait_for_data(request_url: str,
                  poll_interval: Optional[float] = STANDARD_POLLING_SLEEP_TIME,
                  verbose: Optional[bool] = False) -> Dict:
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
    # get status
    status = get_status(request_url)

    # wait until request is done
    while (status["search_result"]["data_uri"] is None):
        time.sleep(poll_interval)
        if (verbose is True):
            print("[%s] Checking for data ..." % (datetime.datetime.now()))
        status = get_status(request_url)

    # return
    if (verbose is True):
        print("[%s] Data is now available" % (datetime.datetime.now()))
    return status


def cancel(request_url: str,
           wait: Optional[bool] = False,
           poll_interval: Optional[float] = STANDARD_POLLING_SLEEP_TIME,
           verbose: Optional[bool] = False) -> int:
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
        pyaurorax.exceptions.AuroraXUnexpectedContentTypeException: unexpected error
        pyaurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation
    """
    # do request
    req = AuroraXRequest(method="delete",
                         url=request_url,
                         null_response=True)
    req.execute()

    # return immediately if we don't want to wait
    if (wait is False):
        return 0

    # get status
    status = get_status(request_url)

    # wait for request to be cancelled
    while (status["search_result"]["data_uri"] is None and status["search_result"]["error_condition"] is False):
        time.sleep(poll_interval)
        if (verbose is True):
            print("[%s] Checking for cancellation status ..." % (datetime.datetime.now()))
        status = get_status(request_url)

    # return
    if (verbose is True):
        print("[%s] The request has been cancelled" % (datetime.datetime.now()))
    return 0


def list(search_type: Optional[str] = None,
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
        pyaurorax.exceptions.AuroraXUnauthorizedException: invalid API key for this operation
    """
    # check the search request type
    if (search_type is not None and search_type not in ALLOWED_SEARCH_LISTING_TYPES):
        warnings.warn("The search type value '%s' is not one that "
                      "PyAuroraX knows about. Supported values are: "
                      "%s. Aborting request." % (search_type,
                                                 ', '.join(ALLOWED_SEARCH_LISTING_TYPES)))
        return []

    # set params
    params: Dict[str, Any] = {}
    if (search_type is not None):
        params["search_type"] = search_type
    if (active is not None):
        params["active"] = active
    if (start is not None):
        params["start"] = start.strftime("%Y-%m-%dT%H:%M:%S")
    if (end is not None):
        params["end"] = end.strftime("%Y-%m-%dT%H:%M:%S")
    if (file_size is not None):
        params["file_size"] = file_size
    if (result_count is not None):
        params["result_count"] = result_count
    if (query_duration is not None):
        params["query_duration"] = query_duration
    if (error_condition is not None):
        params["query_duration"] = query_duration

    # do request
    url = urls.list_requests_url
    req = AuroraXRequest(method="get",
                         url=url,
                         params=params)
    res = req.execute()

    # check responses
    if (res.status_code == 401):
        raise AuroraXUnauthorizedException("API key not detected, please authenticate first.")
    if (res.status_code == 403):
        raise AuroraXUnauthorizedException("Administrator account required. API key not valid "
                                           "for this level of access")

    # return
    return res.data


def delete(request_id: str) -> int:
    """
    Entirely remove a search request from the AuroraX
    database. Administrators only.

    Args:
        request_id: search request UUID

    Returns:
        0 on success, raises error on failure

    Raises:
        pyaurorax.exceptions.AuroraXNotFoundException: data source not found
    """
    # do request
    url = urls.delete_requests_url.format(request_id)
    req = AuroraXRequest(method="delete",
                         url=url,
                         null_response=True)
    res = req.execute()

    # check response and return
    if (res.status_code != 200):
        raise AuroraXException("%s - %s" % (res.data["error_code"],
                                            res.data["error_message"]))
    return 0
