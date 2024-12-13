# Copyright 2024 University of Calgary
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
AuroraX data source record
"""

from typing import List, Dict, Optional
from .data_source_stats import DataSourceStatistics

# basic format
FORMAT_BASIC_INFO: str = "basic_info"
"""
Data sources are returned with basic information: identifier,
program, platform, instrument type, source type, and display name
"""

# basic, but with metadata as well
FORMAT_BASIC_INFO_WITH_METADATA: str = "with_metadata"
"""
Data sources are returned with basic information, plus the metadata
"""

# minimal, only the identifier
FORMAT_IDENTIFIER_ONLY: str = "identifier_only"
"""
Data sources are returned with only the identifier
"""

# full record, everything
FORMAT_FULL_RECORD: str = "full_record"
"""
Data sources are returned with all information.
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


class DataSource:
    """
    AuroraX data source record

    Attributes:
        identifier (int): the unique AuroraX data source identifier
        program (str): the program for this data source
        platform (str): the platform for this data source
        instrument_type (str): the instrument type for this data source
        source_type (str): the data source type for this data source. Options are
            in the pyaurorax.search.sources module, or at the top level using the
            pyaurorax.search.SOURCE_TYPE_* variables.
        display_name (str): the display name for this data source
        metadata (Dict): metadata for this data source (arbitrary keys and values)
        owner (str): the owner's email address of this data source
        maintainers (List[str]): the email addresses of AuroraX accounts that can alter
            this data source and its associated records
        ephemeris_metadata_schema (Dict): a list of dictionaries capturing the metadata
            keys and values that can appear in ephemeris records associated with
            this data source
        data_product_metadata_schema (Dict): a list of dictionaries capturing the metadata
            keys and values that can appear in data product records associated with
            this data source
        format (str): the format used when printing the data source, defaults to
            "full_record". Other options are in the pyaurorax.search.sources module, or
            at the top level using the pyaurorax.search.FORMAT_* variables.
    """

    def __init__(self,
                 identifier: Optional[int] = None,
                 program: Optional[str] = None,
                 platform: Optional[str] = None,
                 instrument_type: Optional[str] = None,
                 source_type: Optional[str] = None,
                 display_name: Optional[str] = None,
                 metadata: Optional[Dict] = None,
                 owner: Optional[str] = None,
                 maintainers: Optional[List[str]] = None,
                 ephemeris_metadata_schema: Optional[List[Dict]] = None,
                 data_product_metadata_schema: Optional[List[Dict]] = None,
                 stats: Optional[DataSourceStatistics] = None,
                 format: str = FORMAT_FULL_RECORD):
        self.identifier = identifier
        self.program = program
        self.platform = platform
        self.instrument_type = instrument_type
        self.source_type = source_type
        self.display_name = display_name
        self.metadata = metadata
        self.owner = owner
        self.maintainers = maintainers
        self.ephemeris_metadata_schema = ephemeris_metadata_schema
        self.data_product_metadata_schema = data_product_metadata_schema
        self.stats = stats
        self.format = format

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "DataSource(identifier=%s, program='%s', platform='%s', instrument_type='%s', source_type='%s', display_name='%s', ...)" % (
            self.identifier,
            self.program,
            self.platform,
            self.instrument_type,
            self.source_type,
            self.display_name,
        )

    def pretty_print(self):
        """
        A special print output for this class.
        """
        max_len = 80
        print("DataSource:")
        print("  %-30s: %d" % ("identifier", self.identifier))
        print("  %-30s: %s" % ("program", self.program))
        print("  %-30s: %s" % ("platform", self.platform))
        print("  %-30s: %s" % ("instrument_type", self.instrument_type))
        print("  %-30s: %s" % ("source_type", self.source_type))
        print("  %-30s: %s" % ("display_name", self.display_name))
        print("  %-30s: %s" % ("metadata", self.metadata))
        print("  %-30s: %s" % ("owner", self.owner))
        print("  %-30s: %s" % ("maintainers", self.maintainers))
        if (self.ephemeris_metadata_schema is not None and len(str(self.ephemeris_metadata_schema)) > max_len):
            ephemeris_metadata_schema_str = "%s..." % (str(self.ephemeris_metadata_schema)[0:max_len])
        else:
            ephemeris_metadata_schema_str = self.ephemeris_metadata_schema
        print("  %-30s: %s" % ("ephemeris_metadata_schema", ephemeris_metadata_schema_str))
        if (self.data_product_metadata_schema is not None and len(str(self.data_product_metadata_schema)) > max_len):
            data_product_metadata_schema_str = "%s..." % (str(self.data_product_metadata_schema)[0:max_len])
        else:
            data_product_metadata_schema_str = self.data_product_metadata_schema
        print("  %-30s: %s" % ("data_product_metadata_schema", data_product_metadata_schema_str))
        if (self.stats is not None and len(str(self.stats)) > max_len):
            stats_str = "%s..." % (str(self.stats)[0:max_len])
        else:
            stats_str = self.data_product_metadata_schema
        print("  %-30s: %s" % ("stats", stats_str))
        print("  %-30s: %s" % ("format", self.format))
