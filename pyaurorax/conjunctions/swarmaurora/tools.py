"""
Functions for using conjunction searches with Swarm-Aurora
"""

import webbrowser
import json
from typing import Dict, Union
from ...api import AuroraXRequest
from ...exceptions import AuroraXException
from ..classes.search import Search

# pdoc init
__pdoc__: Dict = {}


def get_url(search_obj: Search) -> str:
    """
    Get a URL that displays a conjunction search in the Swarm-Aurora
    Conjunction Finder

    Args:
        search_obj: a conjunction search object, must be a completed
                    search with the 'request_id' value populated

    Returns:
        the Swarm-Aurora Conjunction Finder URL for this conjunction search
    """
    return "https://swarm-aurora.com/conjunctionFinder/?aurorax_request_id=%s" % (search_obj.request_id)


def open_in_browser(search_obj: Search, browser: str = None) -> None:
    """
    In a browser, open a conjunction search in the Swarm-Aurora
    Conjunction Finder.

    Args:
        search_obj: a conjunction search object, must be a completed
                    search with the 'request_id' value populated
        browser: the browser type to load using. Default is your
                 default browser. Some common other options are
                 "google-chrome", "firefox", or "safari". For all available
                 options, refer to https://docs.python.org/3/library/webbrowser.html#webbrowser.get
    """
    url = get_url(search_obj)
    try:
        w = webbrowser.get(using=browser)
        w.open_new_tab(url)
    except Exception as e:
        if ("could not locate runnable browser" in str(e)):
            raise AuroraXException(("Error: selected browser '%s' not found, please try "
                                   "another. For the list of options, refer to "
                                    "https://docs.python.org/3/library/webbrowser.html#webbrowser.get") % (browser))


def create_custom_import_file(search_obj: Search,
                              filename: str = None,
                              returnDict: bool = False) -> Union[str, Dict]:
    """
    Generate a Swarm-Aurora custom import file for a given
    conjunction search

    Args:
        search_obj: a conjunction search object, must be a completed
                    search with the 'request_id' value populated
        filename: the output filename, default is 'swarmaurora_custom_import_file_{requestID}.json'
        returnDict: return the custom import file contents as a dictionary
                    instead of saving a file, default is False

    Returns:
        the filename of the saved custom import file, or a dictionary with the
        file contents if `returnDict` is set to True
    """
    # make request
    url = "https://swarm-aurora.com/conjunctionFinder/generate_custom_import_json?aurorax_request_id=%s" % (
        search_obj.request_id)
    req = AuroraXRequest(method="get",
                         url=url,
                         body=search_obj.query)
    res = req.execute()

    # return the contents as a dict if requested
    if (returnDict is True):
        return res.data

    # set default filename
    if (filename is None):
        filename = "swarmaurora_custom_import_%s.json" % (search_obj.request_id)

    # save data to file
    with open(filename, 'w', encoding='utf-8') as fp:
        json.dump(res.data, fp, indent=4)

    # return
    return filename
