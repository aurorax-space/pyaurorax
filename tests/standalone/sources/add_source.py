import pyaurorax
import pprint
import os


def main():
    # read API key from environment vars
    api_key = os.environ["AURORAX_API_KEY"]
    pyaurorax.api.set_base_url("https://api.staging.aurorax.space")
    pyaurorax.authenticate(api_key)

    # set values
    identifier = 400
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument"
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
    r = pyaurorax.sources.add(program,
                              platform,
                              instrument_type,
                              source_type,
                              display_name,
                              ephemeris_metadata_schema=metadata_schema_ephemeris,
                              data_product_metadata_schema=metadata_schema_data_products,
                              identifier=identifier)

    # output results
    print("Successfully added source\n")
    pprint.pprint(r)


# ----------
if (__name__ == "__main__"):
    main()
