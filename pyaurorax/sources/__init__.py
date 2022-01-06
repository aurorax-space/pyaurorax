"""
AuroraX data sources are unique instruments that produce ephemeris or
data product records.

Note that all functions and classes from submodules are all imported
at this level of the sources module. They can be referenced from
here instead of digging in deeper to the submodules.
"""

# function and class imports
from .sources import get
from .sources import get_using_filters
from .sources import get_using_identifier
from .sources import get_stats
from .sources import list
from .sources import add
from .sources import delete
from .sources import update
from .sources import partial_update
from .classes.data_source import DataSource
from .classes.data_source_stats import DataSourceStatistics

# pdoc imports and exports
from .sources import __pdoc__ as __sources_pdoc__
from .classes.data_source import __pdoc__ as __classes_data_source_pdoc__
from .classes.data_source_stats import __pdoc__ as __classes_data_source_stats_pdoc__
__pdoc__ = __sources_pdoc__
__pdoc__ = dict(__pdoc__, **__classes_data_source_pdoc__)
__pdoc__ = dict(__pdoc__, **__classes_data_source_stats_pdoc__)
__all__ = [
    "get",
    "get_using_filters",
    "get_using_identifier",
    "get_stats",
    "list",
    "add",
    "delete",
    "update",
    "partial_update",
    "DataSource",
    "DataSourceStatistics",
]
