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
Functions for interacting with metadata filters
"""

from ..sources import FORMAT_FULL_RECORD
from ..sources._sources import get_using_identifier


def validate(schema, record, quiet):
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


def get_ephemeris_schema(aurorax_obj, identifier):
    # get the data source
    source_info = get_using_identifier(aurorax_obj, identifier, FORMAT_FULL_RECORD, False)

    # if there's an ephemeris metadata schema, return it
    if source_info.ephemeris_metadata_schema:
        return source_info.ephemeris_metadata_schema
    else:
        return []


def get_data_products_schema(aurorax_obj, identifier):
    # get the data source
    source_info = get_using_identifier(aurorax_obj, identifier, FORMAT_FULL_RECORD, False)

    # if there's a data products metadata schema, return it
    if source_info.data_product_metadata_schema:
        return source_info.data_product_metadata_schema
    else:
        return []
