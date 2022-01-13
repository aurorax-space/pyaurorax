"""
Class definition for a data source
"""

from pydantic import BaseModel
from typing import List, Dict, Optional
from ...sources import (FORMAT_BASIC_INFO,
                        FORMAT_BASIC_INFO_WITH_METADATA,
                        FORMAT_IDENTIFIER_ONLY,
                        FORMAT_FULL_RECORD)

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
        # init
        max_len = 20

        # for each format type, construct the string to return
        if (self.format == FORMAT_IDENTIFIER_ONLY):
            s = f"DataSource(identifier={self.identifier})"
        elif (self.format == FORMAT_BASIC_INFO):
            s = f"DataSource(identifier={self.identifier}, program='{self.program}', " \
                f"platform='{self.platform}', instrument_type='{self.instrument_type}', " \
                f"source_type='{self.source_type}', display_name='{self.display_name}')"
        elif (self.format == FORMAT_BASIC_INFO_WITH_METADATA):
            # shorten strings
            metadata_str = f"{self.metadata}"
            if (len(metadata_str) > 10):
                metadata_str = metadata_str[0:10] + "...}"

            # set return string
            s = f"DataSource(identifier={self.identifier}, program='{self.program}', " \
                f"platform='{self.platform}', instrument_type='{self.instrument_type}', " \
                f"source_type='{self.source_type}', display_name='{self.display_name}', " \
                f"metadata={metadata_str})"
        elif (self.format == FORMAT_FULL_RECORD):
            # shorten strings
            metadata_str = f"{self.metadata}"
            if (len(metadata_str) > max_len):
                metadata_str = metadata_str[0:max_len] + "...}"
            ephemeris_metadata_schema_str = f"{self.ephemeris_metadata_schema}"
            if (len(ephemeris_metadata_schema_str) > max_len):
                ephemeris_metadata_schema_str = ephemeris_metadata_schema_str[0:max_len] + "...}]"
            data_product_metadata_schema_str = f"{self.data_product_metadata_schema}"
            if (len(data_product_metadata_schema_str) > max_len):
                data_product_metadata_schema_str = data_product_metadata_schema_str[0:max_len] + "...}]"

            # set return string
            s = f"DataSource(identifier={self.identifier}, program='{self.program}', " \
                f"platform='{self.platform}', instrument_type='{self.instrument_type}', " \
                f"source_type='{self.source_type}', display_name='{self.display_name}', " \
                f"metadata={metadata_str}, owner='{self.owner}', maintainers={self.maintainers}, " \
                f"ephemeris_metadata_schema={ephemeris_metadata_schema_str}, " \
                f"data_product_metadata_schema={data_product_metadata_schema_str})"

        # return constructed string
        return s
