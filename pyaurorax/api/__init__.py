"""
This module is the under-the-hood interface for RESTful API
requests. It provides helper functions that the PyAuroraX library
uses to make robust requests.

Note that all functions and classes from submodules are all imported
at this level of the api module. They can be referenced from here
instead of digging in deeper to the submodules.
"""

# endpoint URLs
DEFAULT_BASE_URL: str = "https://api.aurorax.space"
""" The default API base URL to use when sending requests """

# function and class imports
from .classes.request import (DEFAULT_RETRIES,
                              REQUEST_HEADERS,
                              REQUEST_TIMEOUT,
                              API_KEY_HEADER_NAME,
                              AuroraXRequest)
from .classes.response import AuroraXResponse
from .api import (urls,
                  get_api_key,
                  authenticate,
                  set_base_url,
                  get_base_url,
                  reset_base_url)

# pdoc import and exports
from .api import __pdoc__ as __api_pdoc__
from .classes.request import __pdoc__ as __classes_request_pdoc__
from .classes.response import __pdoc__ as __classes_response_pdoc__
__pdoc__ = __api_pdoc__
__pdoc__ = dict(__pdoc__, **__classes_request_pdoc__)
__pdoc__ = dict(__pdoc__, **__classes_response_pdoc__)
__all__ = [
    "DEFAULT_BASE_URL",
    "DEFAULT_RETRIES",
    "REQUEST_HEADERS",
    "REQUEST_TIMEOUT",
    "API_KEY_HEADER_NAME",
    "AuroraXRequest",
    "AuroraXResponse",
    "urls",
    "get_api_key",
    "authenticate",
    "set_base_url",
    "get_base_url",
    "reset_base_url",
]
