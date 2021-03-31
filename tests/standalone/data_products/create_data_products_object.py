import aurorax
import datetime
import pprint


def main():
    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    start_dt = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end_dt = start_dt.replace(hour=23, minute=59, second=59)
    data_product_type = "keogram"
    url = "testing_url.jpg"
    metadata = {}

    # set as staging API
    aurorax.api.set_base_url("https://api.staging.aurorax.space")

    # get identifier
    data_source = aurorax.sources.get(program, platform, instrument_type)
    identifier = data_source["identifier"]

    # create DataProduct object
    e = aurorax.data_products.DataProduct(identifier=identifier,
                                          program=program,
                                          platform=platform,
                                          instrument_type=instrument_type,
                                          data_product_type=data_product_type,
                                          url=url,
                                          start=start_dt,
                                          end=end_dt,
                                          metadata=metadata)

    # print
    print("__str__:\n----------")
    print(e)
    print()
    print("__repr__:\n----------")
    pprint.pprint(e)


# ----------
if (__name__ == "__main__"):
    main()
