import pytest
import pyaurorax
from pyaurorax import AuroraXNotFoundException
from pyaurorax.sources import DataSource, DataSourceStatistics


@pytest.mark.sources
def test_get_single_source():
    source = pyaurorax.sources.get("swarm",
                                   "swarma",
                                   "footprint",
                                   format=pyaurorax.FORMAT_FULL_RECORD)
    assert type(source) is DataSource


def test_get_source_by_filter():
    source = pyaurorax.sources.get_using_filters(program="swarm",
                                                 instrument_type="footprint",
                                                 format=pyaurorax.FORMAT_FULL_RECORD)
    assert type(source) is list and len(source) > 0


@pytest.mark.sources
def test_get_source_by_id():
    source = pyaurorax.sources.get("swarm",
                                   "swarma",
                                   "footprint",
                                   format=pyaurorax.FORMAT_IDENTIFIER_ONLY)
    source_using_id = pyaurorax.sources.get_using_identifier(source.identifier,
                                                             format=pyaurorax.FORMAT_FULL_RECORD)
    assert type(source_using_id) is DataSource


@pytest.mark.sources
def test_get_source_not_found():
    with pytest.raises(AuroraXNotFoundException):
        pyaurorax.sources.get("space", "physics", "footprint")


@pytest.mark.sources
def test_get_source_using_filters_not_found():
    sources = pyaurorax.sources.get_using_filters("space",
                                                  "physics",
                                                  "footprint")
    assert len(sources) == 0


@pytest.mark.sources
def test_get_source_using_identifier_not_found():
    with pytest.raises(AuroraXNotFoundException):
        pyaurorax.sources.get_using_identifier(12345678)


@pytest.mark.sources
def test_get_source_stats():
    program = "themis"
    platform = "themise"
    instrument_type = "footprint"

    data_source = pyaurorax.sources.get_using_filters(program=program,
                                                      platform=platform,
                                                      instrument_type=instrument_type)

    stats = pyaurorax.sources.get_stats(data_source[0].identifier,
                                        "full_record")

    assert type(stats) is DataSourceStatistics


@pytest.mark.sources
def test_list_sources():
    sources = pyaurorax.sources.list()
    assert type(sources) is list and len(sources) > 0


@pytest.mark.sources
def test_add_source():
    # set values
    identifier = 400
    program = "test-program"
    platform = "test-platform-new"
    instrument_type = "test-instrument-new"
    source_type = pyaurorax.SOURCE_TYPE_GROUND
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
    source = pyaurorax.sources.DataSource(identifier=identifier,
                                          program=program,
                                          platform=platform,
                                          instrument_type=instrument_type,
                                          source_type=source_type,
                                          display_name=display_name,
                                          ephemeris_metadata_schema=metadata_schema_ephemeris,
                                          data_product_metadata_schema=metadata_schema_data_products)

    r = pyaurorax.sources.add(source)

    assert r.identifier == 400


@pytest.mark.sources
def test_update_source():
    # get the identifier
    try:
        ds = pyaurorax.sources.get("test-program",
                                   "test-platform-new",
                                   "test-instrument-new",
                                   format=pyaurorax.FORMAT_FULL_RECORD)
    except Exception:
        assert False

    ds.platform = "test-platform-updated"
    ds.instrument_type = "test-instrument-updated"
    ds.metadata = {
        "test-metadata-key": "test-metadata-value"
    }

    # update the data source
    updated_ds = pyaurorax.sources.update(ds)

    assert (updated_ds.platform == "test-platform-updated"
            and updated_ds.instrument_type == "test-instrument-updated"
            and "test-metadata-key" in updated_ds.metadata.keys())


@pytest.mark.sources
def test_update_source_partial():
    # get the identifier
    try:
        ds = pyaurorax.sources.get("test-program",
                                   "test-platform-updated",
                                   "test-instrument-updated",
                                   format=pyaurorax.FORMAT_FULL_RECORD)
    except Exception:
        assert False

    # partially update the data source
    updated_ds = pyaurorax.sources.partial_update(identifier=ds.identifier,
                                                  instrument_type="test-instrument-updated-partial",
                                                  metadata={},
                                                  ephemeris_metadata_schema=[])

    assert updated_ds.instrument_type == "test-instrument-updated-partial" \
        and updated_ds.metadata == {} \
        and updated_ds.ephemeris_metadata_schema == []


@pytest.mark.sources
def test_delete_source():
    # set values
    program = "test-program"
    platform = "test-platform-updated"
    instrument_type = "test-instrument-updated-partial"

    # get source record to pull out the identifier
    sources = pyaurorax.sources.get_using_filters(program=program,
                                                  platform=platform,
                                                  instrument_type=instrument_type)
    if (len(sources) == 0):
        assert False
    identifier = sources[0].identifier

    # remove source
    result = pyaurorax.sources.delete(identifier)

    assert result == 1
