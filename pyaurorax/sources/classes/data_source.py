"""
Class definition for a data source
"""

from pydantic import BaseModel
from typing import List, Dict, Optional
from ...sources import (FORMAT_BASIC_INFO,
                        FORMAT_BASIC_INFO_WITH_METADATA,
                        FORMAT_IDENTIFIER_ONLY,
                        FORMAT_FULL_RECORD)
from .data_source_stats import DataSourceStatistics

# pdoc init
__pdoc__: Dict = {}


class DataSource(BaseModel):
    """
    Data source object

    Attributes:
        identifier: the unique AuroraX ID for this data source
        program: the program for this data source
        platform: the platform for this data source
        instrument_type: the instrument type for this data source
        source_type: the data source type for this data source. Options are
            in the pyaurorax.sources module, or at the top level using the
            pyaurorax.SOURCE_TYPE_* variables.
        display_name: the display name for this data source
        metadata: metadata for this data source (arbitrary keys and values)
        owner: the owner's email address of this data source
        maintainers: the email addresses of AuroraX accounts that can alter
            this data source and its associated records
        ephemeris_metadata_schema: a list of dictionaries capturing the metadata
            keys and values that can appear in ephemeris records associated with
            this data source
        data_product_metadata_schema: a list of dictionaries capturing the metadata
            keys and values that can appear in data product records associated with
            this data source
        format: the format used when printing the data source, defaults to
            "full_record". Other options are in the pyaurorax.sources module, or
            at the top level using the pyaurorax.FORMAT_* variables.
    """
    identifier: Optional[int] = None
    program: Optional[str] = None
    platform: Optional[str] = None
    instrument_type: Optional[str] = None
    source_type: Optional[str] = None
    display_name: Optional[str] = None
    metadata: Optional[Dict] = None
    owner: Optional[str] = None
    maintainers: Optional[List[str]] = None
    ephemeris_metadata_schema: Optional[List[Dict]] = None
    data_product_metadata_schema: Optional[List[Dict]] = None
    format: Optional[str] = FORMAT_FULL_RECORD
    stats: Optional[DataSourceStatistics] = None

    def __str__(self) -> str:
        """
        String method

        Returns:
            string format of DataSource object
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation

        Returns:
            object representation of DataSource object
        """
        # set each attribute string
        attr_identifier = "None" if self.identifier is None else f"{self.identifier}"
        attr_program = "None" if self.program is None else f"'{self.program}'"
        attr_platform = "None" if self.platform is None else f"'{self.platform}'"
        attr_instrument_type = "None" if self.instrument_type is None else f"'{self.instrument_type}'"
        attr_source_type = "None" if self.source_type is None else f"'{self.source_type}'"
        attr_display_name = "None" if self.display_name is None else f"'{self.display_name}'"
        attr_metadata = "None" if self.metadata is None else f"{self.metadata}"
        attr_owner = "None" if self.owner is None else f"'{self.owner}'"
        attr_maintainers = "None" if self.maintainers is None else f"{self.maintainers}"
        attr_eph_schema = "None" if self.ephemeris_metadata_schema is None else f"{self.ephemeris_metadata_schema}"
        attr_dp_schema = "None" if self.data_product_metadata_schema is None else f"{self.data_product_metadata_schema}"
        attr_stats = "None" if self.stats is None else f"{self.stats}"

        # shorten strings
        max_len = 20
        if (len(attr_metadata) > max_len):
            attr_metadata = attr_metadata[0:max_len] + "...}"
        if (len(attr_eph_schema) > max_len):
            attr_eph_schema = attr_eph_schema[0:max_len] + "...}]"
        if (len(attr_dp_schema) > max_len):
            attr_dp_schema = attr_dp_schema[0:max_len] + "...}]"

        # for each format type, construct the repr to return
        if (self.format == FORMAT_IDENTIFIER_ONLY):
            r = "DataSource(identifier=%s)" % (attr_identifier)
        elif (self.format == FORMAT_BASIC_INFO):
            r = "DataSource(identifier=%s, program=%s, platform=%s, " \
                "instrument_type=%s, source_type=%s, display_name=%s, " \
                "stats=%s)" % (attr_identifier,
                               attr_program,
                               attr_platform,
                               attr_instrument_type,
                               attr_source_type,
                               attr_display_name,
                               attr_stats)
        elif (self.format == FORMAT_BASIC_INFO_WITH_METADATA):
            r = "DataSource(identifier=%s, program=%s, platform=%s, " \
                "instrument_type=%s, source_type=%s, display_name=%s, " \
                "metadata=%s, stats=%s)" % (attr_identifier,
                                            attr_program,
                                            attr_platform,
                                            attr_instrument_type,
                                            attr_source_type,
                                            attr_display_name,
                                            attr_metadata,
                                            attr_stats)
        elif (self.format == FORMAT_FULL_RECORD):
            r = "DataSource(identifier=%s, program=%s, platform=%s, " \
                "instrument_type=%s, source_type=%s, display_name=%s, " \
                "metadata=%s, owner=%s, maintainers=%s, ephemeris_metadata_schema=%s, " \
                "data_product_metadata_schema=%s, stats=%s)" % (attr_identifier,
                                                                attr_program,
                                                                attr_platform,
                                                                attr_instrument_type,
                                                                attr_source_type,
                                                                attr_display_name,
                                                                attr_metadata,
                                                                attr_owner,
                                                                attr_maintainers,
                                                                attr_eph_schema,
                                                                attr_dp_schema,
                                                                attr_stats)

        # return constructed repr
        return r
