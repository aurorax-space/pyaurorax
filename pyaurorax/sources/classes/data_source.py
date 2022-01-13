"""
Class definition for a data source
"""

import pprint
from pydantic import BaseModel
from typing import List, Dict, Optional

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
        return pprint.pformat(self.__dict__)
