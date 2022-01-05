"""
This module is the under-the-hood interface for RESTful API
requests. It provides helper functions that the PyAuroraX library
uses to make robust requests.
"""

# function and class imports
from ._api import AuroraXRequest
from ._api import AuroraXResponse
from ._api import urls
from ._api import get_api_key
from ._api import authenticate
from ._api import set_base_url
from ._api import get_base_url
from ._api import reset_base_url
from ._api import DEFAULT_RETRIES
from ._api import REQUEST_HEADERS
from ._api import API_KEY_HEADER_NAME
from ._api import DEFAULT_BASE_URL

# pdoc import and exports
from ._api import __pdoc__
__all__ = [
    "AuroraXRequest",
    "AuroraXResponse",
    "urls",
    "get_api_key",
    "authenticate",
    "set_base_url",
    "get_base_url",
    "reset_base_url",
    "DEFAULT_RETRIES",
    "REQUEST_HEADERS",
    "API_KEY_HEADER_NAME",
    "DEFAULT_BASE_URL",
]
