import pyaurorax
from typing import Dict, List

# pdoc init
__pdoc__: Dict = {}


def validate(schema: List[Dict], record: Dict, quiet: bool = False) -> bool:
    """
    Validate a metadata record against a schema. This checks that the
    key names match and there aren't fewer or more keys than expected.

    Args:
        schema: list of dictionaries representing the metadata schema
            to validate against
        record: metadata record dictionary to validate

    Returns:
        True if the metadata record is valid, False if it is not
    """
    # set keys from schema and record
    schema_keys = sorted([i["field_name"] for i in schema])
    record_keys = sorted(record.keys())

    # check keys
    if (schema_keys != record_keys):
        if (quiet is False):
            print("Metadata invalid, keys don't match")
        return False
    return True


def get_ephemeris_schema(identifier: int) -> List[Dict]:
    """
    Retrieve the metadata schema for an ephemeris record

    Args:
        identifier: the AuroraX data source ID

    Returns:
        the metadata schema associated with the record
    """
    source_info = pyaurorax.sources.get_using_identifier(identifier, format="full_record")
    if source_info.ephemeris_metadata_schema:
        return source_info.ephemeris_metadata_schema
    else:
        return []


def get_data_products_schema(identifier: int) -> List[Dict]:
    """
    Retrieve the metadata schema for a data products record

    Args:
        identifier: the AuroraX data source ID

    Returns:
        the metadata schema associated with the record
    """
    source_info = pyaurorax.sources.get_using_identifier(identifier, format="full_record")
    if source_info.data_product_metadata_schema:
        return source_info.data_product_metadata_schema
    else:
        return []
