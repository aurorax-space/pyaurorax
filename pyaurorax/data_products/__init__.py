"""
The data_products module is used to search and upload data
product records within AuroraX. One example of a data product
is a keogram.
"""

# function and class imports
from ._data_products import search_async
from ._data_products import search
from ._data_products import upload
from ._data_products import delete
from ._data_products import delete_daterange
from ._classes._data_product import DataProduct
from ._classes._search import Search

# pdoc imports and exports
from ._data_products import __pdoc__ as __data_products_pdoc__
from ._classes._data_product import __pdoc__ as __classes_data_product_pdoc__
from ._classes._search import __pdoc__ as __classes_search_pdoc__
__pdoc__ = __data_products_pdoc__
__pdoc__ = dict(__pdoc__, **__classes_data_product_pdoc__)
__pdoc__ = dict(__pdoc__, **__classes_search_pdoc__)
__all__ = [
    "search_async",
    "search",
    "upload",
    "delete",
    "delete_daterange",
    "DataProduct",
    "Search",
]
