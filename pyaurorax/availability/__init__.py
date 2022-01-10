"""
The availability module provides functions to quickly
determine what data exists on the AuroraX platform.

Note that all functions and classes from submodules are all imported
at this level of the availability module. They can be referenced from
here instead of digging in deeper to the submodules.
"""

# function and class imports
from .availability import (ephemeris,
                           data_products)
from .classes.availability_result import AvailabilityResult

# pdoc imports and exports
from .availability import __pdoc__ as __availability_pdoc__
from .classes.availability_result import __pdoc__ as __classes_avail_result_pdoc__
__pdoc__ = __availability_pdoc__
__pdoc__ = dict(__pdoc__, **__classes_avail_result_pdoc__)
__all__ = [
    "ephemeris",
    "data_products",
    "AvailabilityResult",
]
