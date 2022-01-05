"""
The conjunction module is used for finding conjunctions between
groupings of data sources.
"""

# function and class imports
from ._conjunctions import search_async
from ._conjunctions import search
from ._classes._conjunction import Conjunction
from ._classes._search import Search
from ._classes._search import DEFAULT_CONJUNCTION_DISTANCE

# pdoc imports and exports
from ._conjunctions import __pdoc__ as __conjunctions_pdoc__
from ._classes._conjunction import __pdoc__ as __classes_conjunctions_pdoc__
from ._classes._search import __pdoc__ as __classes_search_pdoc__
__pdoc__ = __conjunctions_pdoc__
__pdoc__ = dict(__pdoc__, **__classes_conjunctions_pdoc__)
__pdoc__ = dict(__pdoc__, **__classes_search_pdoc__)
__all__ = [
    "search_async",
    "search",
    "Conjunction",
    "Search",
    "DEFAULT_CONJUNCTION_DISTANCE",
]
