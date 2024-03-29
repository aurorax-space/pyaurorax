import pyaurorax
import os


def main():
    # read API key from environment vars
    api_key = os.environ["AURORAX_API_KEY"]
    pyaurorax.api.set_base_url("https://api.staging.aurorax.space")
    pyaurorax.authenticate(api_key)

    # set values
    program = "test-program-updated"
    platform = "test-platform-updated"
    instrument_type = "test-instrument-type-updated"
    source_type = pyaurorax.SOURCE_TYPE_HEO
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
    ds = pyaurorax.sources.get("test-program", "test-platform", "test-instrument")
    if (ds == {}):
        print("Could not find test-instrument, make sure you've added it already")
        return 1

    # update the data source
    updated_ds = pyaurorax.sources.update(identifier=ds.identifier,
                                          program=program,
                                          platform=platform,
                                          instrument_type=instrument_type,
                                          source_type=source_type,
                                          display_name=display_name,
                                          ephemeris_metadata_schema=metadata_schema_ephemeris,
                                          data_product_metadata_schema=metadata_schema_data_products)

    # output results
    print("Successfully updated source\n")
    print(updated_ds)


# ----------
if (__name__ == "__main__"):
    main()
