"""
AuroraX metadata schemas describe the intended structure of metadata stored in
ephemeris and data product records.
"""
import pyaurorax
from typing import Dict, List


def validate(schema: List[Dict], record: Dict, quiet: bool = False) -> bool:
    """
    Validate the metadata record against a schema. This checks that the key names match and there aren't
    fewer or more keys than expected.

    Attributes:
        schema: list of dictionaries representing the metadata schema to validate against.
        record: metadata record dictionary to validate.

    Returns:
        True if the metadata record is valid.
    """
    # check keys
    schema_keys = sorted([i["field_name"] for i in schema])
    record_keys = sorted(record.keys())
    if (schema_keys != record_keys):
        if (quiet is False):
            print("Metadata invalid, keys don't match")
        return False
    return True


def get_ephemeris_schema(identifier: int) -> List[Dict]:
    """
    Retrieve the metadata schema for an ephemeris record.

    Attributes:
        identifier: ephemeris source ID.

    Returns:
        Metadata schema associated with the record.

    """
    source_info = pyaurorax.sources.get_using_identifier(
        identifier, format="full_record")
    if source_info.ephemeris_metadata_schema:
        return source_info.ephemeris_metadata_schema
    else:
        return []


def get_data_products_schema(identifier: int) -> List[Dict]:
    """
    Retrieve the metadata schema for a data products record.

    Attributes:
        identifier: ephemeris source ID.

    Returns:
        Metadata schema associated with the record.

    """
    source_info = pyaurorax.sources.get_using_identifier(
        identifier, format="full_record")
    if source_info.data_product_metadata_schema:
        return source_info.data_product_metadata_schema
    else:
        return []
