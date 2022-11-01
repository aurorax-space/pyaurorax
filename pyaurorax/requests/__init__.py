"""
The requests module contains helper methods for retrieving data from
an AuroraX request.

Note that all functions and classes from submodules are all imported
at this level of the requests module. They can be referenced from
here instead of digging in deeper to the submodules.
"""

# function and class imports
from .requests import (FIRST_FOLLOWUP_SLEEP_TIME,
                       STANDARD_POLLING_SLEEP_TIME,
                       ALLOWED_SEARCH_LISTING_TYPES,
                       get_data,
                       get_logs,
                       get_status,
                       wait_for_data,
                       cancel,
                       list,
                       delete)

# pdoc imports and exports
from .requests import __pdoc__ as __requests_pdoc__
__pdoc__ = __requests_pdoc__
__all__ = [
    "FIRST_FOLLOWUP_SLEEP_TIME",
    "STANDARD_POLLING_SLEEP_TIME",
    "ALLOWED_SEARCH_LISTING_TYPES",
    "get_data",
    "get_logs",
    "get_status",
    "wait_for_data",
    "cancel",
    "list",
    "delete",
]
