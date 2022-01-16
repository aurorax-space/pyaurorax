"""
Functions for performing conjunction searches
"""

import datetime
import humanize
import warnings
from typing import Dict, List, Optional, Union
from .classes.search import Search
from ..api import AuroraXRequest, urls
from ..conjunctions import CONJUNCTION_TYPE_NBTRACE
from ..requests import STANDARD_POLLING_SLEEP_TIME

# pdoc init
__pdoc__: Dict = {}


def search(start: datetime.datetime,
           end: datetime.datetime,
           distance: Union[int, float, Dict[str, Union[int, float]]],
           ground: Optional[List[Dict[str, str]]] = [],
           space: Optional[List[Dict[str, str]]] = [],
           events: Optional[List[Dict[str, str]]] = [],
           conjunction_types: Optional[List[str]] = [CONJUNCTION_TYPE_NBTRACE],
           epoch_search_precision: Optional[int] = 60,
           response_format: Optional[Dict[str, bool]] = None,
           poll_interval: Optional[float] = STANDARD_POLLING_SLEEP_TIME,
           return_immediately: Optional[bool] = False,
           verbose: Optional[bool] = False) -> Search:
    """
    Search for conjunctions between data sources

    By default, this function will block and wait until the request completes and
    all data is downloaded. If you don't want to wait, set the 'return_immediately`
    value to True. The Search object will be returned right after the search has been
    started, and you can use the helper functions as part of that object to get the
    data when it's done.

    Args:
        start: start timestamp of the search (inclusive)
        end: end timestamp of the search (inclusive)
        distance: the maximum distance allowed between data sources when searching for
            conjunctions. This can either be a number (int or float), or a dictionary
            modified from the output of the "get_advanced_distances_combos()" function.
        ground: list of ground instrument search parameters, defaults to []

            Example:

                [{
                    "programs": ["themis-asi"],
                    "platforms": ["gillam", "rabbit lake"],
                    "instrument_types": ["RGB"],
                    "ephemeris_metadata_filters": {
                        "logical_operator": "AND",
                        "expressions": [
                            {
                                "key": "calgary_apa_ml_v1",
                                "operator": "in",
                                "values": [ "classified as APA" ]
                            }
                        ]
                    }
                }]
        space: list of one or more space instrument search parameters, defaults to []

            Example:

                [{
                    "programs": ["themis-asi", "swarm"],
                    "platforms": ["themisa", "swarma"],
                    "instrument_types": ["footprint"],
                    "ephemeris_metadata_filters": {
                        "logical_operator": "AND",
                        "expressions": [
                            {
                                "key": "nbtrace_region",
                                "operator": "in",
                                "values": [ "north auroral oval" ]
                            }
                        ]
                    },
                    "hemisphere": [
                        "northern"
                    ]
                }]
        events: list of one or more events search parameters, defaults to []

            Example:

                [{
                    "programs": [ "events" ],
                    "platforms": [ "toshi" ],
                    "instrument_types": [ "substorm onsets" ]
                }]
        conjunction_types: list of conjunction types, defaults to ["nbtrace"]. Options are
            in the pyaurorax.conjunctions module, or at the top level using the
            pyaurorax.CONJUNCTION_TYPE_* variables.
        epoch_search_precision: the time precision to which conjunctions are calculated. Can be
            30 or 60 seconds. Defaults to 60 seconds. Note - this parameter is under active
            development and still considered "alpha".
        response_format: JSON representation of desired data response format
        poll_interval: seconds to wait between polling calls, defaults to
            pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME
        return_immediately: initiate the search and return without waiting for data to
            be received, defaults to False
        verbose: show the progress of the request using the request log, defaults

    Returns:
        a pyaurorax.conjunctions.Search object
    """
    # create a Search object
    s = Search(start,
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
        print("[%s] Request details available at: %s" % (datetime.datetime.now(),
                                                         s.request_url))

    # return immediately if we wanted to
    if (return_immediately is True):
        return s

    # wait for data
    if (verbose is True):
        print("[%s] Waiting for data ..." % (datetime.datetime.now()))
    s.wait(poll_interval=poll_interval, verbose=verbose)

    # get the data
    if (verbose is True):
        print("[%s] Retrieving data ..." % (datetime.datetime.now()))
    s.get_data()

    # return response with the data
    if (verbose is True):
        print("[%s] Retrieved %s of data containing %d records" % (datetime.datetime.now(),
                                                                   humanize.filesize.naturalsize(
                                                                       s.status["search_result"]["file_size"]),
                                                                   s.status["search_result"]["result_count"]))

    # return
    return s


def search_async(start: datetime.datetime,
                 end: datetime.datetime,
                 distance: Union[int, float, Dict[str, Union[int, float]]],
                 ground: Optional[List[Dict[str, str]]] = [],
                 space: Optional[List[Dict[str, str]]] = [],
                 events: Optional[List[Dict[str, str]]] = [],
                 conjunction_types: Optional[List[str]] = [CONJUNCTION_TYPE_NBTRACE],
                 epoch_search_precision: Optional[int] = 60,
                 response_format: Optional[Dict[str, bool]] = None) -> Search:
    """
    Submit a request for a conjunctions search, return immediately

    The request will be done asynchronously by the API. Use the helper functions
    as part of the Search object returned to check for data and/or download it.
    If you don't want the search to return immediately and rather block until
    all data is downloaded, please use the 'search' function instead.

    .. deprecated::
        This function is deprecated as of 0.9.0. Please use the 'search' function
        with the 'return_immediately' flag set to True to get the same behaviour.
        This function will be removed in a future release.

    Args:
        start: start timestamp of the search (inclusive)
        end: end timestamp of the search (inclusive)
        distance: the maximum distance allowed between data sources when searching for
            conjunctions. This can either be a number (int or float), or a dictionary
            modified from the output of the "get_advanced_distances_combos()" function.
        ground: list of ground instrument search parameters, defaults to []

            Example:

                [{
                    "programs": ["themis-asi"],
                    "platforms": ["gillam", "rabbit lake"],
                    "instrument_types": ["RGB"],
                    "ephemeris_metadata_filters": {
                        "logical_operator": "AND",
                        "expressions": [
                            {
                                "key": "calgary_apa_ml_v1",
                                "operator": "in",
                                "values": [ "classified as APA" ]
                            }
                        ]
                    }
                }]
        space: list of one or more space instrument search parameters, defaults to []

            Example:

                [{
                    "programs": ["themis-asi", "swarm"],
                    "platforms": ["themisa", "swarma"],
                    "instrument_types": ["footprint"],
                    "ephemeris_metadata_filters": {
                        "logical_operator": "AND",
                        "expressions": [
                            {
                                "key": "nbtrace_region",
                                "operator": "in",
                                "values": [ "north auroral oval" ]
                            }
                        ]
                    },
                    "hemisphere": [
                        "northern"
                    ]
                }]
        events: list of one or more events search parameters, defaults to []

            Example:

                [{
                    "programs": [ "events" ],
                    "platforms": [ "toshi" ],
                    "instrument_types": [ "substorm onsets" ]
                }]
        conjunction_types: list of conjunction types, defaults to ["nbtrace"]. Options are
            in the pyaurorax.conjunctions module, or at the top level using the
            pyaurorax.CONJUNCTION_TYPE_* variables.
        epoch_search_precision: the time precision to which conjunctions are calculated. Can be
            30 or 60 seconds. Defaults to 60 seconds. Note - this parameter is under active
            development and still considered "alpha".
        response_format: JSON representation of desired data response format

    Returns:
        a pyaurorax.conjunctions.Search object
    """
    warnings.warn("This function is deprecated and will be removed in a future release. Please "
                  "use the 'search' function with the 'return_immediately' flag to produce the "
                  "same behaviour.", DeprecationWarning, stacklevel=2)
    s = Search(start,
               end,
               distance,
               ground=ground,
               space=space,
               events=events,
               conjunction_types=conjunction_types,
               epoch_search_precision=epoch_search_precision,
               response_format=response_format)
    s.execute()
    return s


def describe(search_obj: Search) -> str:
    """
    Describe a conjunction search as an "SQL-like" string

    Args:
        search_obj: the conjunction search object to describe

    Returns:
        the "SQL-like" string describing the conjunction search object
    """
    # make request
    req = AuroraXRequest(method="post",
                         url=urls.describe_conjunction_query,
                         body=search_obj.query)
    res = req.execute()

    # return
    return res.data
