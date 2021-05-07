import aurorax
import os

aurorax.api.set_base_url("https://api.staging.aurorax.space")

def test_get_single_source():
    source = aurorax.sources.get("swarm", "swarma", "footprint", format="basic_info")

    assert type(source) is dict and source


def test_get_source_by_filter():
    source = aurorax.sources.get_using_filters(program="swarm", instrument_type="footprint", format="basic_info")
    
    assert type(source) is list and len(source) > 0


def test_get_source_by_id():
    source = aurorax.sources.get_using_identifier(10, format="basic_info")

    assert type(source) is dict and source


def test_get_source_stats():
    program = "themis"
    platform = "themise"
    instrument_type = "footprint"

    data_source = aurorax.sources.get_using_filters(program=program,
                                                    platform=platform,
                                                    instrument_type=instrument_type)

    stats = aurorax.sources.get_stats(data_source[0]["identifier"])

    assert type(stats) is dict and stats


def test_list_sources():
    sources = aurorax.sources.list()

    assert type(sources) is list and len(sources) > 0


def test_add_source():
    aurorax.api.authenticate(os.getenv("AURORAX_APIKEY_STAGING"))

    # set values
    identifier = 400
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument"
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
    r = aurorax.sources.add(program,
                            platform,
                            instrument_type,
                            source_type,
                            display_name,
                            ephemeris_metadata_schema=metadata_schema_ephemeris,
                            data_product_metadata_schema=metadata_schema_data_products,
                            identifier=identifier)

    assert r["identifier"] == 400


def test_update_source():
    aurorax.api.authenticate(os.getenv("AURORAX_APIKEY_STAGING"))

    # set values
    program = "test-program-updated"
    platform = "test-platform-updated"
    instrument_type = "test-instrument-type-updated"
    source_type = "leo"
    display_name = "Test Instrument Updated"
    metadata_schema_ephemeris = [
        {
            "field_name": "test_meta_updated",
            "description": "testing metadata field updated",
            "data_type": "string",
            "allowed_values": ["one", "two"],
        }
    ]
    metadata_schema_data_products = [
        {
            "field_name": "test_meta_updated_dataproducts",
            "description": "testing metadata field updated data products",
            "data_type": "string",
            "allowed_values": ["one", "two", "three"],
        }
    ]

    # get the identifier
    ds = aurorax.sources.get("test-program", "test-platform", "test-instrument")
    if (ds == {}):
        print("Could not find test-instrument, make sure you've added it already")
        return 1

    # update the data source
    updated_ds = aurorax.sources.update(identifier=ds["identifier"],
                                        program=program,
                                        platform=platform,
                                        instrument_type=instrument_type,
                                        source_type=source_type,
                                        display_name=display_name,
                                        ephemeris_metadata_schema=metadata_schema_ephemeris,
                                        data_product_metadata_schema=metadata_schema_data_products)

    assert updated_ds["program"] == "test-program-updated"


def test_delete_source():
    aurorax.api.authenticate(os.getenv("AURORAX_APIKEY_STAGING"))
    
    # set values
    program = "test-program-updated"
    platform = "test-platform-updated"
    instrument_type = "test-instrument-type-updated"

    # get source record to pull out the identifier
    sources = aurorax.sources.get_using_filters(program=program,
                                                platform=platform,
                                                instrument_type=instrument_type)
    if (len(sources) == 0):
        sources = aurorax.sources.get_using_filters(program=program,
                                                    platform=platform,
                                                    instrument_type="test-instrument-type-updated")
        if (len(sources) == 0):
            assert False
    identifier = sources[0]["identifier"]

    # remove source
    result = aurorax.sources.delete(identifier)

    assert result == 0