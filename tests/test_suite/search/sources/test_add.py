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

import pytest
import string
import random
from pyaurorax.search.sources import DataSource, SOURCE_TYPE_GROUND


@pytest.mark.search_rw
def test_specific_identifier(aurorax):
    # set values
    identifier = 400
    program = "test-program"
    platform = "test-platform"
    instrument_type = "testing::test_add_source_specific_identifier"
    source_type = SOURCE_TYPE_GROUND
    display_name = "Test Instrument"
    metadata_schema_ephemeris = [{
        "field_name": "test_meta1",
        "description": "testing metadata field 1",
        "data_type": "string",
        "allowed_values": [],
    }, {
        "field_name": "test_meta2",
        "description": "testing metadata field 2",
        "data_type": "string",
        "allowed_values": [],
    }]
    metadata_schema_data_products = [{
        "field_name": "test_meta1",
        "description": "testing metadata field 1",
        "data_type": "string",
        "allowed_values": [],
    }, {
        "field_name": "test_meta2",
        "description": "testing metadata field 2",
        "data_type": "string",
        "allowed_values": [],
    }]

    # make request
    ds_to_create = DataSource(identifier=identifier,
                              program=program,
                              platform=platform,
                              instrument_type=instrument_type,
                              source_type=source_type,
                              display_name=display_name,
                              ephemeris_metadata_schema=metadata_schema_ephemeris,
                              data_product_metadata_schema=metadata_schema_data_products)

    added_ds = aurorax.search.sources.add(ds_to_create)

    # check attributes of added data source
    assert ds_to_create.identifier == added_ds.identifier
    assert added_ds.program == added_ds.program
    assert added_ds.platform == added_ds.platform
    assert added_ds.instrument_type == added_ds.instrument_type
    assert added_ds.source_type == added_ds.source_type
    assert added_ds.display_name == added_ds.display_name
    assert added_ds.ephemeris_metadata_schema == added_ds.ephemeris_metadata_schema
    assert added_ds.data_product_metadata_schema == added_ds.data_product_metadata_schema

    # cleanup by deleting the data source
    aurorax.search.sources.delete(identifier)


@pytest.mark.search_rw
def test_arbitrary_identifier(aurorax):
    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "testing::test_add_source_arbitrary_identifier"
    source_type = SOURCE_TYPE_GROUND
    display_name = "Test Instrument"
    metadata_schema_ephemeris = [{
        "field_name": "test_meta1",
        "description": "testing metadata field 1",
        "data_type": "string",
        "allowed_values": [],
    }, {
        "field_name": "test_meta2",
        "description": "testing metadata field 2",
        "data_type": "string",
        "allowed_values": [],
    }]
    metadata_schema_data_products = [{
        "field_name": "test_meta1",
        "description": "testing metadata field 1",
        "data_type": "string",
        "allowed_values": [],
    }, {
        "field_name": "test_meta2",
        "description": "testing metadata field 2",
        "data_type": "string",
        "allowed_values": [],
    }]

    # make request
    ds_to_create = DataSource(program=program,
                              platform=platform,
                              instrument_type=instrument_type,
                              source_type=source_type,
                              display_name=display_name,
                              ephemeris_metadata_schema=metadata_schema_ephemeris,
                              data_product_metadata_schema=metadata_schema_data_products)

    added_ds = aurorax.search.sources.add(ds_to_create)

    # check attributes of added data source
    assert added_ds.identifier is not None
    assert added_ds.program == added_ds.program
    assert added_ds.platform == added_ds.platform
    assert added_ds.instrument_type == added_ds.instrument_type
    assert added_ds.source_type == added_ds.source_type
    assert added_ds.display_name == added_ds.display_name
    assert added_ds.ephemeris_metadata_schema == added_ds.ephemeris_metadata_schema
    assert added_ds.data_product_metadata_schema == added_ds.data_product_metadata_schema

    # cleanup by deleting the data source
    aurorax.search.sources.delete(added_ds.identifier)


@pytest.mark.search_rw
def test_bad_input1(aurorax):
    # make request
    ds_to_create = DataSource(
        program="something",
        platform="something",
    )

    with pytest.raises(ValueError) as e_info:
        aurorax.search.sources.add(ds_to_create)
    assert "Missing required fields" in str(e_info)


@pytest.mark.search_rw
def test_bad_input2(aurorax):
    # make request
    ds_to_create = DataSource(
        program=''.join(random.choices(string.ascii_lowercase, k=250)),
        platform="something",
        instrument_type="something",
        display_name="something",
        source_type="ground",
    )

    with pytest.raises(ValueError) as e_info:
        aurorax.search.sources.add(ds_to_create)
    assert "Program too long" in str(e_info)


@pytest.mark.search_rw
def test_bad_input3(aurorax):
    # make request
    ds_to_create = DataSource(
        program="something",
        platform=''.join(random.choices(string.ascii_lowercase, k=75)),
        instrument_type="something",
        display_name="something",
        source_type="ground",
    )

    with pytest.raises(ValueError) as e_info:
        aurorax.search.sources.add(ds_to_create)
    assert "Platform too long" in str(e_info)


@pytest.mark.search_rw
def test_bad_input4(aurorax):
    # make request
    ds_to_create = DataSource(
        program="something",
        platform="something",
        instrument_type=''.join(random.choices(string.ascii_lowercase, k=250)),
        display_name="something",
        source_type="ground",
    )

    with pytest.raises(ValueError) as e_info:
        aurorax.search.sources.add(ds_to_create)
    assert "Instrument type too long" in str(e_info)


@pytest.mark.search_rw
def test_bad_input5(aurorax):
    # make request
    ds_to_create = DataSource(
        program="something",
        platform="something",
        instrument_type="something",
        display_name=''.join(random.choices(string.ascii_lowercase, k=75)),
        source_type="ground",
    )

    with pytest.raises(ValueError) as e_info:
        aurorax.search.sources.add(ds_to_create)
    assert "Display name too long" in str(e_info)
