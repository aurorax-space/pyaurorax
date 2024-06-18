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
import pyaurorax
from pyaurorax.search.sources import (
    DataSource,
    DataSourceStatistics,
    FORMAT_FULL_RECORD,
    FORMAT_IDENTIFIER_ONLY,
    SOURCE_TYPE_GROUND,
)


@pytest.mark.search_sources
def test_get_single_source(aurorax):
    source = aurorax.search.sources.get("swarm", "swarma", "footprint", format=FORMAT_FULL_RECORD)
    assert isinstance(source, DataSource) is True


@pytest.mark.search_sources
def test_search_sources(aurorax):
    # get sources
    sources = aurorax.search.sources.search(programs=["swarm"], format=FORMAT_FULL_RECORD, include_stats=True)

    # check count and type
    assert len(sources) == 3
    for s in sources:
        assert isinstance(s, DataSource) is True


@pytest.mark.search_sources
def test_get_source_by_filter(aurorax):
    # get sources
    sources = aurorax.search.sources.get_using_filters(program="swarm", instrument_type="footprint", format=FORMAT_FULL_RECORD)

    # check count and type
    assert len(sources) == 3
    for s in sources:
        assert isinstance(s, DataSource) is True


@pytest.mark.search_sources
def test_get_source_by_id(aurorax):
    source = aurorax.search.sources.get("swarm", "swarma", "footprint", format=FORMAT_IDENTIFIER_ONLY)
    source_using_id = aurorax.search.sources.get_using_identifier(source.identifier, format=FORMAT_FULL_RECORD)
    assert isinstance(source_using_id, DataSource) is True
    assert source.identifier == source_using_id.identifier


@pytest.mark.search_sources
def test_get_source_not_found(aurorax):
    with pytest.raises(pyaurorax.AuroraXNotFoundError):
        aurorax.search.sources.get("definitely", "doesnt", "exist")


@pytest.mark.search_sources
def test_get_source_using_filters_not_found(aurorax):
    sources = aurorax.search.sources.get_using_filters("definitely", "doesnt", "exist")
    assert len(sources) == 0


@pytest.mark.search_sources
def test_get_source_using_identifier_not_found(aurorax):
    identifier = 12345678
    with pytest.raises(pyaurorax.AuroraXAPIError) as e_info:
        aurorax.search.sources.get_using_identifier(identifier)
    assert "No Data Source record found in AuroraX for identifier %d" % (identifier) in str(e_info)


@pytest.mark.search_sources
def test_get_source_stats(aurorax):
    # get data source with stats
    program = "themis"
    platform = "themise"
    instrument_type = "footprint"
    sources = aurorax.search.sources.get_using_filters(
        program=program,
        platform=platform,
        instrument_type=instrument_type,
        include_stats=True,
    )

    # check types
    for source in sources:
        assert isinstance(source, DataSource) is True
        assert source.stats is not None
        assert isinstance(source.stats, DataSourceStatistics) is True


@pytest.mark.search_sources
def test_list_sources(aurorax):
    # get sources
    sources = aurorax.search.sources.list()

    # check count and type
    assert len(sources) > 1
    for s in sources:
        assert isinstance(s, DataSource) is True


@pytest.mark.search_sources
def test_add_source_specific_identifier(aurorax):
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


@pytest.mark.search_sources
def test_add_source_arbitrary_identifier(aurorax):
    # set values
    identifier = 401
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


@pytest.mark.search_sources
def test_update_source(aurorax):
    # create the data source
    identifier = 402
    program = "test-program"
    platform = "test-platform"
    instrument_type = "testing::test_update_source"
    source_type = SOURCE_TYPE_GROUND
    display_name = instrument_type
    ds_to_create = DataSource(
        identifier=identifier,
        program=program,
        platform=platform,
        instrument_type=instrument_type,
        source_type=source_type,
        display_name=display_name,
    )
    _ = aurorax.search.sources.add(ds_to_create)

    # update the data source
    updated_ds = aurorax.search.sources.update(identifier,
                                               instrument_type="testing::test_update_source_partial",
                                               metadata={},
                                               ephemeris_metadata_schema=[])

    assert updated_ds.instrument_type == "testing::test_update_source_partial"
    assert updated_ds.metadata == {}
    assert updated_ds.ephemeris_metadata_schema == []

    # cleanup by deleting the source
    delete_result = aurorax.search.sources.delete(identifier)
    assert delete_result == 0


@pytest.mark.search_sources
def test_delete_source(aurorax):
    # set values
    idenifier = 403
    program = "test-program"
    platform = "test-platform"
    instrument_type = "testing::test_delete_source"
    source_type = SOURCE_TYPE_GROUND
    display_name = instrument_type

    # create the source
    ds_to_create = DataSource(
        identifier=idenifier,
        program=program,
        platform=platform,
        instrument_type=instrument_type,
        source_type=source_type,
        display_name=display_name,
    )
    ds_created = aurorax.search.sources.add(ds_to_create)

    # delete the source
    delete_result = aurorax.search.sources.delete(ds_created.identifier)

    # check it successfully deleted
    assert delete_result == 0
