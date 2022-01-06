"""
Format options used for data sources when retrieving different pieces of data
"""

# basic format
FORMAT_BASIC_INFO = "basic_info"
"""
Data sources are returned with the basic information: identifier,
program, platform, instrument type, source type, and display name
"""

# full record, everything
FORMAT_FULL_RECORD = "full_record"
"""
Data sources are returned with all information about them. This
includes at least: identifier, program, platform, instrument type,
source type, display name, metadata, owner, maintainers, the
ephemeris metadata schema, and the data products meatadata schema.
"""

# basic, but with metadata as well
FORMAT_BASIC_INFO_WITH_METADATA = "with_metadata"
"""
Data sources are returned with the basic information, plus the metadata
"""

# minimal, only the identifier
FORMAT_IDENTIFIER_ONLY = "identifier_only"
"""
Data sources are returned with only the identifier
"""

# default
FORMAT_DEFAULT = FORMAT_BASIC_INFO
"""
Default data source format (basic info)
"""
