import aurorax
from aurorax.sources import DataSource
import os

def test_get_single_source():
    source = aurorax.sources.get("swarm", "swarma", "footprint", format="full_record")

    assert type(source) is DataSource


def test_get_source_by_filter():
    source = aurorax.sources.get_using_filters(program="swarm", instrument_type="footprint", format="full_record")
    
    assert type(source) is list and len(source) > 0


def test_get_source_by_id():
    source = aurorax.sources.get("swarm", "swarma", "footprint", format="identifier_only")
    source_using_id = aurorax.sources.get_using_identifier(source.identifier, format="full_record")

    assert type(source_using_id) is DataSource


def test_get_source_stats():
    program = "themis"
    platform = "themise"
    instrument_type = "footprint"

    data_source = aurorax.sources.get_using_filters(program=program,
                                                    platform=platform,
                                                    instrument_type=instrument_type)

    stats = aurorax.sources.get_stats(data_source[0].identifier)

    assert type(stats) is dict


def test_list_sources():
    sources = aurorax.sources.list()

    assert type(sources) is list and len(sources) > 0


def test_add_source():
    # set values
    identifier = 400
    program = "test-program-new"
    platform = "test-platform-new"
    instrument_type = "test-instrument-new"
    source_type = "ground"
    display_name = "Test Instrument"
    metadata_schema_ephemeris = [
        {
            "field_name": "test_meta1",
            "description": "testing metadata field 1",
            "data_type": "string",
            "allowed_values": [],
        },
        {
            "field_name": "test_meta2",
            "description": "testing metadata field 2",
            "data_type": "string",
            "allowed_values": [],
        }
    ]
    metadata_schema_data_products = [
        {
            "field_name": "test_meta1",
            "description": "testing metadata field 1",
            "data_type": "string",
            "allowed_values": [],
        },
        {
            "field_name": "test_meta2",
            "description": "testing metadata field 2",
            "data_type": "string",
            "allowed_values": [],
        }
    ]

    # make request
    source = aurorax.sources.DataSource(identifier=identifier, program=program, platform=platform, instrument_type=instrument_type,
                                        source_type=source_type, display_name=display_name, ephemeris_metadata_schema=metadata_schema_ephemeris,
                                        data_product_metadata_schema=metadata_schema_data_products)

    r = aurorax.sources.add(source)

    assert r.identifier == 400


def test_update_source():
    # get the identifier
    try:
        ds = aurorax.sources.get("test-program-new", "test-platform-new", "test-instrument-new", format="full_record")
    except:
        assert False

    ds.program = "test-program-updated"
    ds.platform = "test-platform-updated"
    ds.instrument_type = "test-instrument-updated"
    ds.metadata = {
        "test-metadata-key": "test-metadata-value"
    }

    # update the data source
    updated_ds = aurorax.sources.update(ds)

    assert updated_ds.program == "test-program-updated"


def test_delete_source():
    # set values
    program = "test-program-updated"
    platform = "test-platform-updated"
    instrument_type = "test-instrument-updated"

    # get source record to pull out the identifier
    sources = aurorax.sources.get_using_filters(program=program,
                                                platform=platform,
                                                instrument_type=instrument_type)
    if (len(sources) == 0):
        assert False
    identifier = sources[0].identifier

    # remove source
    result = aurorax.sources.delete(identifier)

    assert result == 1