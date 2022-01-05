"""
AuroraX metadata schemas describe the intended structure of metadata stored in
ephemeris and data product records. This module provides functions for
interacting with the schemas.
"""

# function and class imports
from ._metadata import get_data_products_schema
from ._metadata import get_ephemeris_schema
from ._metadata import validate

# pdoc imports and exports
from ._metadata import __pdoc__ as __metadata_pdoc__
__pdoc__ = __metadata_pdoc__
__all__ = [
    "get_data_products_schema",
    "get_ephemeris_schema",
    "validate",
]
