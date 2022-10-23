"""
The conjunction module is used for finding conjunctions between
groupings of data sources.

Note that all functions and classes from submodules are all imported
at this level of the conjunctions module. They can be referenced from
here instead of digging in deeper to the submodules.
"""

# conjunction type - north b-trace
CONJUNCTION_TYPE_NBTRACE: str = "nbtrace"
"""
Conjunction search 'conjunction_type' category for
finding conjunctions using the north B-trace data
"""

# conjunction type - south b-trace
CONJUNCTION_TYPE_SBTRACE: str = "sbtrace"
"""
Conjunction search 'conjunction_type' category for
finding conjunctions using the south B-trace data
"""

# function and class imports
from .conjunctions import (search,
                           describe,
                           get_request_url)
from .swarmaurora import __all__ as swarmaurora_all
from .classes.conjunction import Conjunction
from .classes.search import Search

# pdoc imports and exports
from .conjunctions import __pdoc__ as __conjunctions_pdoc__
from .classes.conjunction import __pdoc__ as __classes_conjunctions_pdoc__
from .classes.search import __pdoc__ as __classes_search_pdoc__
__pdoc__ = __conjunctions_pdoc__
__pdoc__ = dict(__pdoc__, **__classes_conjunctions_pdoc__)
__pdoc__ = dict(__pdoc__, **__classes_search_pdoc__)
__all__ = [
    "CONJUNCTION_TYPE_NBTRACE",
    "CONJUNCTION_TYPE_SBTRACE",
    "search",
    "describe",
    "get_request_url",
    "Conjunction",
    "Search",
    "swarmaurora_all",
]
