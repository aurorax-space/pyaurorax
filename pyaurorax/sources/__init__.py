"""
AuroraX data sources are unique instruments that produce ephemeris or data product records.
"""

# function and class imports
from ._sources import get
from ._sources import get_using_filters
from ._sources import get_using_identifier
from ._sources import get_stats
from ._sources import list
from ._sources import add
from ._sources import delete
from ._sources import update
from ._sources import partial_update
from ._classes._data_source import DataSource
from ._classes._data_source_stats import DataSourceStatistics


# pdoc imports and exports
from ._sources import __pdoc__ as __sources_pdoc__
from ._classes._data_source import __pdoc__ as __classes_data_source_pdoc__
from ._classes._data_source_stats import __pdoc__ as __classes_data_source_stats_pdoc__
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
