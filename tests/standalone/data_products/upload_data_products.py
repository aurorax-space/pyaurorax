import aurorax
import os
import datetime
import pprint


def main():
    # read API key from environment vars
    api_key = os.environ["AURORAX_API_KEY"]
    aurorax.authenticate(api_key)

    # set as staging API
    aurorax.api.set_base_url("https://api.staging.aurorax.space")

    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    url = "test.jpg"
    metadata = {
        "test_meta1": "testing1",
        "test_meta2": "testing2",
    }
    data_product_type = "keogram"
    start_dt = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end_dt = start_dt.replace(hour=23, minute=59, second=59)

    # get the data source ID
    ds = aurorax.sources.get(program, platform, instrument_type)
    identifier = ds["identifier"]

    # create DataProducts object
    e = aurorax.data_products.DataProduct(identifier=identifier,
                                          program=program,
                                          platform=platform,
                                          instrument_type=instrument_type,
                                          data_product_type=data_product_type,
                                          url=url,
                                          start=start_dt,
                                          end=end_dt,
                                          metadata=metadata)
    pprint.pprint(e)
    print("\nUploading record ...")

    # set records array
    records = []
    records.append(e)

    # upload record
    aurorax.data_products.upload(identifier, records=records)
    print("Successfully uploaded")


# ----------
if (__name__ == "__main__"):
    main()
