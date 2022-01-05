"""
The utility module provides helper methods such as converting
arbitrary geographic locations to North/South B-trace geographic
locations.
"""

# function and class imports
from ._calculate_btrace import ground_geo_to_nbtrace
from ._calculate_btrace import ground_geo_to_sbtrace

# pdoc imports and exports
from ._calculate_btrace import __pdoc__ as __btrace_pdoc__
__pdoc__ = __btrace_pdoc__
__all__ = [
    "ground_geo_to_nbtrace",
    "ground_geo_to_sbtrace",
]
