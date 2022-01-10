"""
The data_products module is used to search and upload data
product records within AuroraX. One example of a data product
is a keogram.

Note that all functions and classes from submodules are all imported
at this level of the data_products module. They can be referenced from
here instead of digging in deeper to the submodules.
"""

# function and class imports
from .data_products import search
from .data_products import search_async
from .data_products import upload
from .data_products import delete
from .data_products import delete_daterange
from .classes.data_product import DataProduct
from .classes.search import Search

# pdoc imports and exports
from .data_products import __pdoc__ as __data_products_pdoc__
from .classes.data_product import __pdoc__ as __classes_data_product_pdoc__
from .classes.search import __pdoc__ as __classes_search_pdoc__
__pdoc__ = __data_products_pdoc__
__pdoc__ = dict(__pdoc__, **__classes_data_product_pdoc__)
__pdoc__ = dict(__pdoc__, **__classes_search_pdoc__)
__all__ = [
    "search",
    "search_async",
    "upload",
    "delete",
    "delete_daterange",
    "DataProduct",
    "Search",
]
