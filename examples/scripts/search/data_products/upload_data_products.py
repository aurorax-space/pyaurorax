import os
import datetime
import pprint
import pyaurorax
from dotenv import load_dotenv


def main():
    # read API key from environment vars
    aurorax = pyaurorax.PyAuroraX()
    load_dotenv("%s/../../../../tests/test_suite/.env" % (os.path.dirname(os.path.realpath(__file__))))
    aurorax.api_base_url = "https://api.staging.aurorax.space"
    aurorax.api_key = os.environ["AURORAX_API_KEY"]

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
    ds = aurorax.search.sources.get(program, platform, instrument_type)
    if (ds.identifier is None):
        print("Error retrieving valid data source, aborting")
        return 1

    # create DataProducts object
    e = pyaurorax.search.DataProductData(ds, data_product_type, start_dt, end_dt, url, metadata)
    pprint.pprint(e)
    print("\nUploading record ...")

    # set records array
    records = []
    records.append(e)

    # upload record
    aurorax.search.data_products.upload(ds.identifier, records=records)
    print("Successfully uploaded")


# ----------
if (__name__ == "__main__"):
    main()
