"""
Functions for using conjunction searches with Swarm-Aurora
"""

import webbrowser
from typing import Dict
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
            print("Error: selected browser '%s' not found, please try " +
                  "another. For the list of options, refer to " +
                  "https://docs.python.org/3/library/webbrowser.html#webbrowser.get")
