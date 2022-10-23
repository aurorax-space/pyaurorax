"""
The ephemeris module is used to search and upload ephemeris records
within AuroraX.

Note that all functions and classes from submodules are all imported
at this level of the ephemeris module. They can be referenced from
here instead of digging in deeper to the submodules.
"""

# function and class imports
from .ephemeris import (search,
                        upload,
                        delete,
                        describe,
                        get_request_url)
from .classes.ephemeris import Ephemeris
from .classes.search import Search

# pdoc imports and exports
from .ephemeris import __pdoc__ as __ephemeris_pdoc__
from .classes.ephemeris import __pdoc__ as __classes_ephemeris_pdoc__
from .classes.search import __pdoc__ as __classes_search_pdoc__
__pdoc__ = __ephemeris_pdoc__
__pdoc__ = dict(__pdoc__, **__classes_ephemeris_pdoc__)
__pdoc__ = dict(__pdoc__, **__classes_search_pdoc__)
__all__ = [
    "search",
    "upload",
    "delete",
    "describe",
    "get_request_url",
    "Ephemeris",
    "Search",
]
