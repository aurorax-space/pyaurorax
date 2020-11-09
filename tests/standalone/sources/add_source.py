import aurorax
import pprint
import os


def main():
    # read API key from environment vars
    api_key = os.environ["AURORAX_API_KEY"]

    # set values
    identifier = 400
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    source_type = "ground"
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
    r = aurorax.sources.add(api_key,
                            program,
                            platform,
                            instrument_type,
                            source_type,
                            ephemeris_metadata_schema=metadata_schema_ephemeris,
                            data_products_metadata_schema=metadata_schema_data_products,
                            identifier=identifier)

    # output results
    if (r["status_code"] == 200):
        print("Successfully added source\n")
    else:
        print("Error adding source\n")
    pprint.pprint(r)


# ----------
if (__name__ == "__main__"):
    main()
