"""
The data_products module is used to search and upload data
product records within AuroraX. One example of a data product
is a keogram.

Note that all functions and classes from submodules are all imported
at this level of the data_products module. They can be referenced from
here instead of digging in deeper to the submodules.
"""

# keogram data product type
DATA_PRODUCT_TYPE_KEOGRAM = "keogram"
"""
Data product type for keograms. Keograms are a 2-D
representation of a series of images, and are one of
the most popular data products that auroral science
uses. More information can be found at
https://docs.aurorax.space/about_the_data/standards/#keograms.
"""

# montage data product type
DATA_PRODUCT_TYPE_MONTAGE = "montage"
"""
Data product type for montages. Like keograms, montages are
another representation of a series of images. However, montages
are not a 2D representation but rather a collage of thumnbail
images for the period of time. An example can be found at
https://data.phys.ucalgary.ca/sort_by_project/THEMIS/asi/stream2/2021/12/28/gill_themis19/20211228__gill_themis19_full-montage.pgm.jpg
"""

# movie data product type
DATA_PRODUCT_TYPE_MOVIE = "movie"
"""
Data product type for movies. Movies are timelapse video
files of auroral data, usually as MP4 or MPEG. They can
consist of frames for a whole night, or an hour, and can
be at any cadence that is most appropriate.
"""

# summary plot data product type
DATA_PRODUCT_TYPE_SUMMARY_PLOT = "summary_plot"
"""
Data product type for summary plots. A summary plot can be any type
of plot that shows auroral data in a summary format, for example a
background-subtracted meridian scanning photometer plot showing
counts in Rayleighs.
"""

# data availability data product type
DATA_PRODUCT_TYPE_DATA_AVAILABILITY = "data_availability"
"""
Data product type for data availability. The AuroraX data availability
system does not account for times when data was not expected to be
collected, such as summer shutdowns due to inadequate night hours. This
data product type for 'data availbility' is meant to be used as a smarter
data availability mechanism for Aurora.
"""

# function and class imports
from .data_products import (search,
                            upload,
                            delete_urls,
                            delete,
                            describe,
                            get_request_url)
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
    "DATA_PRODUCT_TYPE_KEOGRAM",
    "DATA_PRODUCT_TYPE_MONTAGE",
    "DATA_PRODUCT_TYPE_MOVIE",
    "DATA_PRODUCT_TYPE_SUMMARY_PLOT",
    "DATA_PRODUCT_TYPE_DATA_AVAILABILITY",
    "search",
    "upload",
    "delete_urls",
    "delete",
    "describe",
    "get_request_url",
    "DataProduct",
    "Search",
]
