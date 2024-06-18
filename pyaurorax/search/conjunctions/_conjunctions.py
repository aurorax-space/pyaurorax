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
from ...exceptions import AuroraXSearchError, AuroraXError
from .classes.search import ConjunctionSearch
from ..api import AuroraXAPIRequest


def search(aurorax_obj, start, end, distance, ground, space, events, conjunction_types, epoch_search_precision, response_format, poll_interval,
           return_immediately, verbose):
    # create a Search object
    s = ConjunctionSearch(aurorax_obj,
                          start,
                          end,
                          distance,
                          ground=ground,
                          space=space,
                          events=events,
                          conjunction_types=conjunction_types,
                          epoch_search_precision=epoch_search_precision,
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
    if (s.status["search_result"]["error_condition"] is True):
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
