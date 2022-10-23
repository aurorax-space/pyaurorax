"""
AuroraX data sources are unique instruments that produce ephemeris or
data product records.

Note that all functions and classes from submodules are all imported
at this level of the sources module. They can be referenced from
here instead of digging in deeper to the submodules.
"""

# basic format
FORMAT_BASIC_INFO: str = "basic_info"
"""
Data sources are returned with the basic information: identifier,
program, platform, instrument type, source type, and display name
"""

# basic, but with metadata as well
FORMAT_BASIC_INFO_WITH_METADATA: str = "with_metadata"
"""
Data sources are returned with the basic information, plus the metadata
"""

# minimal, only the identifier
FORMAT_IDENTIFIER_ONLY: str = "identifier_only"
"""
Data sources are returned with only the identifier
"""

# full record, everything
FORMAT_FULL_RECORD: str = "full_record"
"""
Data sources are returned with all information about them. This
includes at least: identifier, program, platform, instrument type,
source type, display name, metadata, owner, maintainers, the
ephemeris metadata schema, and the data products meatadata schema.
"""

# default
FORMAT_DEFAULT: str = FORMAT_BASIC_INFO
"""
Default data source format (basic info)
"""

# ground source type
SOURCE_TYPE_GROUND: str = "ground"
"""
Data source 'source_type' category for a ground instrument
"""

# low-earth orbiting spacecraft source type
SOURCE_TYPE_LEO: str = "leo"
"""
Data source 'source_type' category for a low-earth orbiting satellite
"""

# highly-elliptical orbiting spacecraft source type
SOURCE_TYPE_HEO: str = "heo"
"""
Data source 'source_type' category for a highly-elliptical orbiting satellite
"""

# lunar orbiting spacecraft source type
SOURCE_TYPE_LUNAR: str = "lunar"
"""
Data source 'source_type' category for a lunar orbiting satellite
"""

# event list source type
SOURCE_TYPE_EVENT_LIST: str = "event_list"
"""
Data source 'source_type' category for a specially-curated event list
"""

# not applicable source type
SOURCE_TYPE_NOT_APPLICABLE: str = "not_applicable"
"""
Data source 'source_type' category for a specially-curated event list
"""

# function and class imports
from .sources import (get,
                      get_using_filters,
                      get_using_identifier,
                      get_stats,
                      list,
                      search,
                      add,
                      delete,
                      update,
                      update_partial)
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
    "FORMAT_BASIC_INFO",
    "FORMAT_BASIC_INFO_WITH_METADATA",
    "FORMAT_FULL_RECORD",
    "FORMAT_IDENTIFIER_ONLY",
    "FORMAT_DEFAULT",
    "SOURCE_TYPE_NOT_APPLICABLE",
    "SOURCE_TYPE_EVENT_LIST",
    "SOURCE_TYPE_GROUND",
    "SOURCE_TYPE_HEO",
    "SOURCE_TYPE_LEO",
    "SOURCE_TYPE_LUNAR",
    "list",
    "search",
    "get",
    "get_using_filters",
    "get_using_identifier",
    "get_stats",
    "add",
    "delete",
    "update",
    "update_partial",
    "DataSource",
    "DataSourceStatistics",
]
