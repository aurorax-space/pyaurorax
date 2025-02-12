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
Functions for interacting with AuroraX requests
"""

import datetime
import time
from ..api.classes.request import AuroraXAPIRequest
from ..location import Location
from ...exceptions import (
    AuroraXDataRetrievalError,
    AuroraXAPIError,
    AuroraXUnauthorizedError,
)

__ALLOWED_SEARCH_LISTING_TYPES = ["conjunction", "data_product", "ephemeris"]


def get_status(aurorax_obj, request_url):
    # do request
    req = AuroraXAPIRequest(aurorax_obj, method="get", url=request_url)
    res = req.execute()

    # return
    return res.data


def get_data(aurorax_obj, data_url, response_format, skip_serializing):
    # do request
    try:
        if (response_format is not None):
            req = AuroraXAPIRequest(aurorax_obj, method="post", url=data_url, body=response_format)
        else:
            req = AuroraXAPIRequest(aurorax_obj, method="get", url=data_url)
        res = req.execute()
    except Exception as e:  # pragma: nocover
        raise AuroraXDataRetrievalError("unable to retrieve data (likely there is none)") from e

    # check for error message
    if ("error" in res.data):  # pragma: nocover
        raise AuroraXDataRetrievalError("%s: %s" % (
            res.data["error"]["error_code"],
            res.data["error"]["error_message"],
        ))

    # set data var
    data_result = res.data["result"]

    # serialize certain values into objects
    #
    # NOTE: this is primarily used when searches were done where the response_format
    # parameter was specified. So we like to serialize a few fields
    if (skip_serializing is False):
        for i in range(0, len(data_result)):
            # ephemeris serializing
            if ("ephemeris" in data_url):
                if ("epoch" in data_result[i]):
                    data_result[i]["epoch"] = datetime.datetime.strptime(data_result[i]["epoch"], "%Y-%m-%dT%H:%M:%S")
                if ("location_geo" in data_result[i]):
                    data_result[i]["location_geo"] = Location(lat=data_result[i]["location_geo"]["lat"], lon=data_result[i]["location_geo"]["lon"])
                if ("location_gsm" in data_result[i]):
                    data_result[i]["location_gsm"] = Location(lat=data_result[i]["location_gsm"]["lat"], lon=data_result[i]["location_gsm"]["lon"])
                if ("nbtrace" in data_result[i]):
                    data_result[i]["nbtrace"] = Location(lat=data_result[i]["nbtrace"]["lat"], lon=data_result[i]["nbtrace"]["lon"])
                if ("sbtrace" in data_result[i]):
                    data_result[i]["sbtrace"] = Location(lat=data_result[i]["sbtrace"]["lat"], lon=data_result[i]["sbtrace"]["lon"])

            # conjunction serializing
            if ("conjunctions" in data_url):
                if ("farthest_epoch" in data_result[i]):
                    data_result[i]["farthest_epoch"] = datetime.datetime.strptime(data_result[i]["farthest_epoch"], "%Y-%m-%dT%H:%M:%S")
                if ("closest_epoch" in data_result[i]):
                    data_result[i]["closest_epoch"] = datetime.datetime.strptime(data_result[i]["closest_epoch"], "%Y-%m-%dT%H:%M:%S")
                if ("start" in data_result[i]):
                    data_result[i]["start"] = datetime.datetime.strptime(data_result[i]["start"], "%Y-%m-%dT%H:%M:%S")
                if ("end" in data_result[i]):
                    data_result[i]["end"] = datetime.datetime.strptime(data_result[i]["end"], "%Y-%m-%dT%H:%M:%S")
                if ("events" in data_result[i]):
                    for j in range(0, len(data_result[i]["events"])):
                        if ("start" in data_result[i]["events"][j]):
                            data_result[i]["events"][j]["start"] = datetime.datetime.strptime(data_result[i]["events"][j]["start"],
                                                                                              "%Y-%m-%dT%H:%M:%S")
                        if ("end" in data_result[i]["events"][j]):
                            data_result[i]["events"][j]["end"] = datetime.datetime.strptime(data_result[i]["events"][j]["end"], "%Y-%m-%dT%H:%M:%S")

            if ("data_products" in data_url):
                if ("start" in data_result[i]):
                    data_result[i]["start"] = datetime.datetime.strptime(data_result[i]["start"], "%Y-%m-%dT%H:%M:%S")
                if ("end" in data_result[i]):
                    data_result[i]["end"] = datetime.datetime.strptime(data_result[i]["end"], "%Y-%m-%dT%H:%M:%S")

    # return
    return data_result


def get_logs(aurorax_obj, request_url):
    # get status
    status = get_status(aurorax_obj, request_url)

    # return
    if ("logs" in status):
        return status["logs"]
    else:  # pragma: nocover
        return []


def wait_for_data(aurorax_obj, request_url, poll_interval, verbose):
    # get status
    status = get_status(aurorax_obj, request_url)

    # wait until request is done
    while (status["search_result"]["data_uri"] is None):
        time.sleep(poll_interval)
        if (verbose is True):
            print("[%s] Checking for data ..." % (datetime.datetime.now()))
        status = get_status(aurorax_obj, request_url)

    # return
    if (verbose is True):
        print("[%s] Data is now available" % (datetime.datetime.now()))
    return status


def cancel(aurorax_obj, request_url, wait, poll_interval, verbose):
    # do request
    req = AuroraXAPIRequest(aurorax_obj, method="delete", url=request_url, null_response=True)
    req.execute()

    # return immediately if we don't want to wait
    if (wait is False):
        return 0

    # get status
    status = get_status(aurorax_obj, request_url)

    # wait for request to be cancelled
    while (status["search_result"]["data_uri"] is None and status["search_result"]["error_condition"] is False):  # pragma: nocover
        time.sleep(poll_interval)
        if (verbose is True):
            print("[%s] Checking for cancellation status ..." % (datetime.datetime.now()))
        status = get_status(aurorax_obj, request_url)

    # return
    if (verbose is True):
        print("[%s] The request has been cancelled" % (datetime.datetime.now()))
    return 0


def list(aurorax_obj, search_type, active, start, end, file_size, result_count, query_duration, error_condition):
    # check the search request type
    if (search_type is not None and search_type not in __ALLOWED_SEARCH_LISTING_TYPES):
        raise ValueError("The search type value '%s' is not one that PyAuroraX knows about. Supported values are: "
                         "%s. Aborting request." % (search_type, ', '.join(__ALLOWED_SEARCH_LISTING_TYPES)))

    # set params
    params = {}
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
    try:
        url = "%s/%s" % (aurorax_obj.api_base_url, aurorax_obj.search.api.URL_SUFFIX_LIST_REQUESTS)
        req = AuroraXAPIRequest(aurorax_obj, method="get", url=url, params=params)
        res = req.execute()
    except AuroraXUnauthorizedError as e:
        raise AuroraXUnauthorizedError("An Administrator API key was not detected, and is required for this function") from e

    # return
    return res.data


def delete(aurorax_obj, request_id):  # pragma: nocover
    # do request
    url = "%s/%s" % (aurorax_obj.api_base_url, aurorax_obj.search.api.URL_SUFFIX_DELETE_REQUESTS.format(request_id))
    req = AuroraXAPIRequest(aurorax_obj, method="delete", url=url, null_response=True)
    res = req.execute()

    # check response and return
    if (res.status_code != 200):
        raise AuroraXAPIError("%s - %s" % (res.data["error_code"], res.data["error_message"]))
    return 0
