import pytest
import pyaurorax


@pytest.mark.metadata
def test_validate_schema():
    source = pyaurorax.sources.get_using_filters(program="swarm",
                                                 platform="swarma",
                                                 instrument_type="footprint")
    schema = pyaurorax.metadata.get_ephemeris_schema(source[0].identifier)

    # create an example metadata dictionary
    metadata = {
        "nbtrace_region": "north cleft",
        "sbtrace_region": "south auroral oval",
        "radial_distance": 150.25,
        "radial_trace_region": "low latitude",
        "spacecraft_region": "nightside magnetosheath",
        "state": "definitive",
        "tii_on": True,
        "tii_quality_vixh": 0,
        "tii_quality_vixv": 1,
        "tii_quality_viy": 2,
        "tii_quality_viz": 3
    }

    # validate
    assert pyaurorax.metadata.validate(schema, metadata)


@pytest.mark.metadata
def test_get_ephemeris_metadata_schema():
    # set parameters
    program = "swarm"
    platform = "swarma"
    instrument_type = "footprint"

    # get idendifier
    data_source = pyaurorax.sources.get(program,
                                        platform,
                                        instrument_type,
                                        "identifier_only")

    # get schema
    schema = pyaurorax.metadata.get_ephemeris_schema(data_source.identifier)

    # check
    assert type(schema) is list


@pytest.mark.metadata
def test_get_data_product_metadata_schema():
    # set parameters
    program = "themis-asi"
    platform = "gillam"
    instrument_type = "panchromatic ASI"

    # get idendifier
    data_source = pyaurorax.sources.get(program,
                                        platform,
                                        instrument_type,
                                        format=pyaurorax.FORMAT_IDENTIFIER_ONLY)

    # get schema
    schema = pyaurorax.metadata.get_data_products_schema(data_source.identifier)

    # check
    assert type(schema) is list
