import aurorax
import os
import datetime
import pprint


def main():
    # read API key from environment vars
    api_key = os.environ["AURORAX_API_KEY"]

    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    metadata = {}
    start_dt = datetime.datetime(2020, 1, 1, 0, 0)
    end_dt = datetime.datetime(2020, 1, 1, 0, 59)
    url = "http://data.aurorax.space/test-url.jpg"
    data_product_type = "summary_plot"

    # get the data source ID
    source = aurorax.sources.get_using_filters(program=[program],
                                               platform=[platform],
                                               instrument_type=[instrument_type])
    identifier = source["data"][0]["identifier"]

    # create Data Product object
    e = aurorax.data_products.DataProduct(identifier,
                                          program,
                                          platform,
                                          instrument_type,
                                          start_dt,
                                          end_dt,
                                          url,
                                          data_product_type,
                                          metadata)
    pprint.pprint(e)
    print("\nUploading record ...")

    # set records array
    records = []
    records.append(e)

    # upload record
    res = aurorax.data_products.upload(api_key, identifier, records=records)

    # print result
    if (res["status_code"] == 202):
        print("Successfully uploaded")
    else:
        print("Failed to upload")
        pprint.pprint(res)


# ----------
if (__name__ == "__main__"):
    main()
