"""
The availability module provides functions to quickly
determine what data exists on the AuroraX platform.
"""

# function and class imports
from ._availability import ephemeris
from ._availability import data_products
from ._classes._availability_result import AvailabilityResult

# pdoc imports and exports
from ._availability import __pdoc__ as __availability_pdoc__
from ._classes._availability_result import __pdoc__ as __classes_avail_result_pdoc__
__pdoc__ = __availability_pdoc__
__pdoc__ = dict(__pdoc__, **__classes_avail_result_pdoc__)
__all__ = [
    "ephemeris",
    "data_products",
    "AvailabilityResult",
]
