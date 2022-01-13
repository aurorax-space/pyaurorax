"""
AuroraX metadata schemas describe the intended structure of metadata stored in
ephemeris and data product records. This module provides functions for
interacting with the schemas.

Note that all functions and classes from submodules are all imported
at this level of the metadata module. They can be referenced from
here instead of digging in deeper to the submodules.
"""

# function and class imports
from .metadata import (get_data_products_schema,
                       get_ephemeris_schema,
                       validate)

# pdoc imports and exports
from .metadata import __pdoc__ as __metadata_pdoc__
__pdoc__ = __metadata_pdoc__
__all__ = [
    "get_data_products_schema",
    "get_ephemeris_schema",
    "validate",
]
