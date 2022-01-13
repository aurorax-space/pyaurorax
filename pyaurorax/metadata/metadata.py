"""
Functions for interacting with metadata filters
"""

from typing import Dict, List, Optional
from ..sources import get_using_identifier, FORMAT_FULL_RECORD

# pdoc init
__pdoc__: Dict = {}


def validate(schema: List[Dict],
             record: Dict,
             quiet: Optional[bool] = False) -> bool:
    """
    Validate a metadata record against a schema. This checks that the
    key names match and there aren't fewer or more keys than expected.

    Args:
        schema: the metadata schema to validate against
        record: metadata record to validate

    Returns:
        True if the metadata record is valid, False if it is not
    """
    # set keys from schema and record
    schema_keys = sorted([i["field_name"] for i in schema])
    record_keys = sorted(record.keys())

    # look for bad keys
    if (schema_keys != record_keys):
        if (quiet is False):
            print("Metadata invalid, keys don't match")
        return False

    # found no bad keys
    return True


def get_ephemeris_schema(identifier: int) -> List[Dict]:
    """
    Retrieve the ephemeris metadata schema for a data source

    Args:
        identifier: the AuroraX data source ID

    Returns:
        the ephemeris metadata schema for the data source
    """
    # get the data source
    source_info = get_using_identifier(identifier, format=FORMAT_FULL_RECORD)

    # if there's an ephemeris metadata schema, return it
    if source_info.ephemeris_metadata_schema:
        return source_info.ephemeris_metadata_schema
    else:
        return []


def get_data_products_schema(identifier: int) -> List[Dict]:
    """
    Retrieve the data products metadata schema for a data source

    Args:
        identifier: the AuroraX data source ID

    Returns:
        the data products metadata schema for the data source
    """
    # get the data source
    source_info = get_using_identifier(identifier, format=FORMAT_FULL_RECORD)

    # if there's a data products metadata schema, return it
    if source_info.data_product_metadata_schema:
        return source_info.data_product_metadata_schema
    else:
        return []
