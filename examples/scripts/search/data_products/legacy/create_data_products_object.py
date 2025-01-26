import datetime
import pyaurorax


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # set values
    program = "trex"
    platform = "gillam"
    instrument_type = "RGB ASI"
    start_dt = datetime.datetime(2020, 1, 1, 0, 0, 0)
    end_dt = start_dt.replace(hour=23, minute=59, second=59)
    data_product_type = "keogram"
    url = "testing_url.jpg"
    metadata = {}

    # get identifier
    ds = aurorax.search.sources.get(program, platform, instrument_type, format=aurorax.search.FORMAT_IDENTIFIER_ONLY)

    # create DataProduct object
    dp = aurorax.search.DataProductData(
        data_source=ds,
        start=start_dt,
        end=end_dt,
        data_product_type=data_product_type,
        url=url,
        metadata=metadata,
    )

    # print
    print()
    print(dp)
    print()


# ----------
if (__name__ == "__main__"):
    main()
