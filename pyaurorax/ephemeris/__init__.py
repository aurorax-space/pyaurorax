"""
The ephemeris module is used to search and upload ephemeris records
within AuroraX
"""

# function and class imports
from ._ephemeris import search_async
from ._ephemeris import search
from ._ephemeris import upload
from ._ephemeris import delete
from ._classes._ephemeris import Ephemeris
from ._classes._search import Search

# pdoc imports and exports
from ._ephemeris import __pdoc__ as __ephemeris_pdoc__
from ._classes._ephemeris import __pdoc__ as __classes_ephemeris_pdoc__
from ._classes._search import __pdoc__ as __classes_search_pdoc__
__pdoc__ = __ephemeris_pdoc__
__pdoc__ = dict(__pdoc__, **__classes_ephemeris_pdoc__)
__pdoc__ = dict(__pdoc__, **__classes_search_pdoc__)
__all__ = [
    "search_async",
    "search",
    "upload",
    "delete",
    "Ephemeris",
    "Search",
]
