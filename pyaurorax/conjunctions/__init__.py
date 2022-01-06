"""
The conjunction module is used for finding conjunctions between
groupings of data sources.

Note that all functions and classes from submodules are all imported
at this level of the conjunctions module. They can be referenced from
here instead of digging in deeper to the submodules.
"""

# function and class imports
from .conjunctions import search_async
from .conjunctions import search
from .classes.conjunction import Conjunction
from .classes.search import Search
from .classes.search import DEFAULT_CONJUNCTION_DISTANCE

# pdoc imports and exports
from .conjunctions import __pdoc__ as __conjunctions_pdoc__
from .classes.conjunction import __pdoc__ as __classes_conjunctions_pdoc__
from .classes.search import __pdoc__ as __classes_search_pdoc__
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
