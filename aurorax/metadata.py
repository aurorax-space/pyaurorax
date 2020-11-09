import aurorax as _aurorax
from typing import Dict as _Dict
from typing import List as _List


def validate(schema: _List, record: _Dict, quiet: bool = False) -> bool:
    """
    Validate the metadata record against a schema. This checks
    that the key names match and there aren't fewer or more keys
    than expected.

    :param schema: metadata schema to validate against
    :type schema: List
    :param record: metadata record to validate
    :type record: Dict

    :return: metadata record is valid
    :rtype: bool
    """
    # check keys
    schema_keys = sorted([i["field_name"] for i in schema])
    record_keys = sorted(record.keys())
    if (schema_keys != record_keys):
        if (quiet is False):
            print("Metadata invalid, keys don't match")
        return False
    return True


def get_ephemeris_schema(identifier: int) -> _List:
    """
    Retrieve the metadata schema for an ephemeris record

    :param identifier: ephemeris source ID
    :type identifier: int

    :return: metadata schema
    :rtype: List
    """
    source_info = _aurorax.sources.get_source_using_identifier(identifier, format="full_record")
    if ("ephemeris_metadata_schema" in source_info["data"]):
        return source_info["data"]["ephemeris_metadata_schema"]
    else:
        return []


def get_data_products_schema(identifier: int) -> _List:
    """
    Retrieve the metadata schema for a data products record

    :param identifier: ephemeris source ID
    :type identifier: int

    :return: metadata schema
    :rtype: List
    """
    source_info = _aurorax.sources.get_source_using_identifier(identifier, format="full_record")
    if ("data_products_metadata_schema" in source_info["data"]):
        return source_info["data"]["data_products_metadata_schema"]
    else:
        return []