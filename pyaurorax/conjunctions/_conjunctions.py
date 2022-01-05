import datetime
import humanize
import pyaurorax
from typing import Dict, List
from ._classes._search import Search, DEFAULT_CONJUNCTION_DISTANCE

# pdoc init
__pdoc__: Dict = {}


def search_async(start: datetime.datetime,
                 end: datetime.datetime,
                 ground: List[Dict],
                 space: List[Dict],
                 conjunction_types: List[str] = ["nbtrace"],
                 max_distances: Dict[str, float] = {},
                 default_distance: float = DEFAULT_CONJUNCTION_DISTANCE,
                 epoch_search_precision: int = 60,
                 response_format: Dict = None) -> Search:
    """
    Submit a request for a conjunctions search, return asynchronously.

    Args:
        start: start timestamp of the search
        end: end timestamp of the search
        ground: List of ground instrument search parameters
            e.g. [
                {
                    "programs": ["themis-asi"],
                    "platforms": ["gillam", "rabbit lake"],
                    "instrument_types": ["RGB"]
                }
            ]
        space: List of one or more space instrument search parameters
            e.g. [
                {
                    "programs": ["themis-asi", "swarm"],
                    "platforms": ["themisa", "swarma"],
                    "instrument_types": ["footprint"]
                }
            ]
        conjunction_types: list of conjunction types, defaults to ["nbtrace"]
        max_distances: dictionary of Dict[str, float] ground-space and space-space maximum
            distances for conjunctions. The default_distance will be used for any ground-space
            and space-space maximum distances not specified.

            e.g. distances = {
                "ground1-ground2": None,
                "ground1-space1": 500,
                "ground1-space2": 500,
                "ground2-space1": 500,
                "ground2-space2": 500,
                "space1-space2": None
            }
        default_distance: default maximum distance in kilometers for conjunction. Used when max
            distance is not specified for any ground-space and space-space instrument pairs.
        epoch_search_precision: the time precision to which conjunctions are calculated. Can be
            30 or 60 seconds. Defaults to 60 seconds. Note - this parameter is under active
            development and still considered "alpha".
        response_format: JSON representation of desired data response format

    Returns:
        A pyaurorax.conjunctions.Search object
    """
    s = Search(start=start,
               end=end,
               ground=ground,
               space=space,
               conjunction_types=conjunction_types,
               max_distances=max_distances,
               default_distance=default_distance,
               epoch_search_precision=epoch_search_precision,
               response_format=response_format)
    s.execute()

    return s


def search(start: datetime.datetime,
           end: datetime.datetime,
           ground: List[Dict],
           space: List[Dict],
           conjunction_types: List[str] = ["nbtrace"],
           max_distances: Dict[str, float] = {},
           default_distance: float = DEFAULT_CONJUNCTION_DISTANCE,
           verbose: bool = False,
           poll_interval: float = pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME,
           epoch_search_precision: int = 60,
           response_format: Dict = None) -> Search:
    """
    Search for conjunctions and block until results are returned

    Args:
        start: start timestamp of the search
        end: end timestamp of the search
        ground: list of ground instrument search parameters
            e.g. [
                {
                    "programs": ["themis-asi"],
                    "platforms": ["gillam", "rabbit lake"],
                    "instrument_types": ["RGB"]
                }
            ]
        space: list of one or more space instrument search parameters
            e.g. [
                {
                    "programs": ["themis-asi", "swarm"],
                    "platforms": ["themisa", "swarma"],
                    "instrument_types": ["footprint"]
                }
            ]
        conjunction_types: list of conjunction types, defaults to ["nbtrace"]
        max_distances: dictionary of Dict[str, float] ground-space and space-space
            maximum distances for conjunctions. The default_distance will be used for
            any ground-space and space-space maximum distances not specified.

            e.g. distances = {
                "ground1-ground2": None,
                "ground1-space1": 500,
                "ground1-space2": 500,
                "ground2-space1": 500,
                "ground2-space2": 500,
                "space1-space2": None
            }
        default_distance: default maximum distance in kilometers for conjunction. Used
            when max distance is not specified for any ground-space and space-space
            instrument pairs.
        verbose: boolean to show the progress of the request using the request
            log, defaults to False
        poll_interval: seconds to wait between polling calls, defaults to
            pyaurorax.requests.STANDARD_POLLING_SLEEP_TIME
        response_format: JSON representation of desired data response format

    Returns:
        A pyaurorax.conjunctions.Search object
    """
    # create a Search object
    s = Search(start=start,
               end=end,
               ground=ground,
               space=space,
               conjunction_types=conjunction_types,
               max_distances=max_distances,
               default_distance=default_distance,
               epoch_search_precision=epoch_search_precision,
               response_format=response_format)
    if verbose:
        print(f"[{datetime.datetime.now()}] Search object created")

    # execute the search
    s.execute()
    if verbose:
        print(f"[{datetime.datetime.now()}] Request submitted")
        print(f"[{datetime.datetime.now()}] Request ID: {s.request_id}")
        print(f"[{datetime.datetime.now()}] Request details available at: {s.request_url}")
        print(f"[{datetime.datetime.now()}] Waiting for data ...")

    # wait for data
    s.wait(poll_interval=poll_interval, verbose=verbose)

    # get the data
    if verbose:
        print(f"[{datetime.datetime.now()}] Retrieving data ...")
    s.get_data()

    # finish
    if verbose:
        print(f'[{datetime.datetime.now()}] Retrieved \
              {humanize.filesize.naturalsize(s.status["search_result"]["file_size"])} of data containing \
              {s.status["search_result"]["result_count"]} records')

    # return
    return s
