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
Functions for performing conjunction searches
"""

import datetime
import humanize
import itertools
import json
from copy import deepcopy
from ...exceptions import AuroraXSearchError, AuroraXError
from .classes.search import ConjunctionSearch
from ..api import AuroraXAPIRequest


def search(aurorax_obj, start, end, distance, ground, space, events, custom_locations, conjunction_types, response_format, poll_interval,
           return_immediately, verbose):
    # create a Search object
    s = ConjunctionSearch(aurorax_obj,
                          start,
                          end,
                          distance,
                          ground=ground,
                          space=space,
                          events=events,
                          custom_locations=custom_locations,
                          conjunction_types=conjunction_types,
                          response_format=response_format)
    if (verbose is True):
        print(f"[{datetime.datetime.now()}] Search object created")

    # execute the search
    s.execute()
    if (verbose is True):
        print("[%s] Request submitted" % (datetime.datetime.now()))
        print("[%s] Request ID: %s" % (datetime.datetime.now(), s.request_id))
        print("[%s] Request details available at: %s" % (datetime.datetime.now(), s.request_url))

    # return immediately if we wanted to
    if (return_immediately is True):
        return s

    # wait for data
    if (verbose is True):
        print("[%s] Waiting for data ..." % (datetime.datetime.now()))
    s.wait(poll_interval=poll_interval, verbose=verbose)

    # check if error condition encountered
    if (s.status["search_result"]["error_condition"] is True):  # pragma: nocover-ok
        # error encountered
        raise AuroraXSearchError(s.logs[-1]["summary"])

    # get the data
    if (verbose is True):
        print("[%s] Retrieving data ..." % (datetime.datetime.now()))
    s.get_data()

    # return response with the data
    if (verbose is True):
        print("[%s] Retrieved %s of data containing %d records" % (
            datetime.datetime.now(),
            humanize.filesize.naturalsize(s.status["search_result"]["file_size"]),  # type: ignore
            s.status["search_result"]["result_count"],
        ))

    # return
    return s


def search_from_raw_query(aurorax_obj, query, poll_interval, return_immediately, verbose):
    # deep copy the query first
    query = deepcopy(query)

    # convert to dict
    if (isinstance(query, str) is True):
        # query is a string, so presumably it is a JSON-valid string; convert it to dict
        query = json.loads(query)

    # set required values
    if ("start" not in query):
        raise AuroraXError("The 'start' parameter is missing from the query. This parameter is required.")
    query["start"] = datetime.datetime.fromisoformat(query["start"][0:-1])
    if ("end" not in query):
        raise AuroraXError("The 'end' parameter is missing from the query. This parameter is required.")
    query["end"] = datetime.datetime.fromisoformat(query["end"][0:-1])
    if ("max_distances" not in query):
        raise AuroraXError("The 'max_distances' parameter is missing from the query. This parameter is required.")

    # change name of distance
    query["distance"] = deepcopy(query["max_distances"])
    del query["max_distances"]

    # change name of adhoc
    if ("adhoc" in query):
        query["custom_locations"] = deepcopy(query["adhoc"])
        del query["adhoc"]

    # create ConjunctionSearch object
    s = ConjunctionSearch(aurorax_obj=aurorax_obj, **query)
    if (verbose is True):
        print(f"[{datetime.datetime.now()}] Search object created")

    # execute the search
    s.execute()
    if (verbose is True):
        print("[%s] Request submitted" % (datetime.datetime.now()))
        print("[%s] Request ID: %s" % (datetime.datetime.now(), s.request_id))
        print("[%s] Request details available at: %s" % (datetime.datetime.now(), s.request_url))

    # return immediately if we wanted to
    if (return_immediately is True):
        return s

    # wait for data
    if (verbose is True):
        print("[%s] Waiting for data ..." % (datetime.datetime.now()))
    s.wait(poll_interval=poll_interval, verbose=verbose)

    # check if error condition encountered
    if (s.status["search_result"]["error_condition"] is True):  # pragma: nocover-ok
        # error encountered
        raise AuroraXSearchError(s.logs[-1]["summary"])

    # get the data
    if (verbose is True):
        print("[%s] Retrieving data ..." % (datetime.datetime.now()))
    s.get_data()

    # return response with the data
    if (verbose is True):
        print("[%s] Retrieved %s of data containing %d records" % (
            datetime.datetime.now(),
            humanize.filesize.naturalsize(s.status["search_result"]["file_size"]),  # type: ignore
            s.status["search_result"]["result_count"],
        ))

    # return
    return s


def describe(aurorax_obj, search_obj, query_dict):
    # set query
    if (search_obj is not None):
        query = search_obj.query
    elif (query_dict is not None):
        query = query_dict
    else:
        raise AuroraXError("One of 'search_obj' or 'query_dict' must be supplied")

    # make request
    url = "%s/%s" % (aurorax_obj.api_base_url, aurorax_obj.search.api.URL_SUFFIX_DESCRIBE_CONJUNCTION_QUERY)
    req = AuroraXAPIRequest(aurorax_obj, method="post", url=url, body=query)
    res = req.execute()

    # return
    return res.data


def get_request_url(aurorax_obj, request_id):
    url = "%s/%s" % (aurorax_obj.api_base_url, aurorax_obj.search.api.URL_SUFFIX_CONJUNCTION_REQUEST.format(request_id))
    return url


def create_advanced_distance_combos(distance, ground, space, events, custom):
    # set input arrays
    options = []
    for i in range(0, ground):
        options.append("ground%d" % (i + 1))
    for i in range(0, space):
        options.append("space%d" % (i + 1))
    for i in range(0, events):
        options.append("events%d" % (i + 1))
    for i in range(0, custom):
        options.append("adhoc%d" % (i + 1))

    # derive all combinations of options of size 2
    combinations = {}
    for element in itertools.combinations(options, r=2):
        combinations["%s-%s" % (element[0], element[1])] = distance

    # return
    return combinations
