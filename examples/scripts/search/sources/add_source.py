import os
import pyaurorax
from dotenv import load_dotenv
from pyaurorax.search import DataSource, SOURCE_TYPE_GROUND


def main():
    # read API key from environment vars
    aurorax = pyaurorax.PyAuroraX()
    load_dotenv("%s/../../../../tests/test_suite/.env" % (os.path.dirname(os.path.realpath(__file__))))
    aurorax.api_base_url = "https://api.staging.aurorax.space"
    aurorax.api_key = os.environ["AURORAX_API_KEY"]

    # set values
    identifier = 400
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument"
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

    # create data source object
    data_source_to_create = DataSource(
        identifier=identifier,
        program=program,
        platform=platform,
        instrument_type=instrument_type,
        source_type=source_type,
        display_name=display_name,
        metadata={},
        ephemeris_metadata_schema=metadata_schema_ephemeris,
        data_product_metadata_schema=metadata_schema_data_products,
    )

    # make request
    created_ds = aurorax.search.sources.add(data_source_to_create)

    # output results
    print("Successfully added source\n")
    print(created_ds)


# ----------
if (__name__ == "__main__"):
    main()
