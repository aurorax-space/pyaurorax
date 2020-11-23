import aurorax
import datetime
import pprint


def main():
    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    start_dt = datetime.datetime(2020, 1, 1, 0, 0)
    end_dt = datetime.datetime(2020, 1, 1, 0, 59)
    data_product_type = "keogram"
    url = "http://data.aurorax.space/test_url.jpg"
    metadata = {}

    # get identifier
    data_source = aurorax.sources.get_using_filters(program=program,
                                                    platform=platform,
                                                    instrument_type=instrument_type)
    identifier = data_source["data"][0]["identifier"]

    # create DataProduct object
    e = aurorax.data_products.DataProduct(identifier,
                                          program,
                                          platform,
                                          instrument_type,
                                          start_dt,
                                          end_dt,
                                          url,
                                          data_product_type,
                                          metadata)

    # print
    print("__str__:\n----------")
    print(e)
    print()
    print("__repr__:\n----------")
    pprint.pprint(e)


# ----------
if (__name__ == "__main__"):
    main()
