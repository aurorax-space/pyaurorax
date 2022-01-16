"""
The util module provides helper methods such as converting
arbitrary geographic locations to North/South B-trace geographic
locations.

Note that all functions and classes from submodules are all imported
at this level of the util module. They can be referenced from
here instead of digging in deeper to the submodules.
"""

# function and class imports
from .calculate_btrace import (ground_geo_to_nbtrace,
                               ground_geo_to_sbtrace)

# pdoc imports and exports
from .calculate_btrace import __pdoc__ as __btrace_pdoc__
__pdoc__ = __btrace_pdoc__
__all__ = [
    "ground_geo_to_nbtrace",
    "ground_geo_to_sbtrace",
]
