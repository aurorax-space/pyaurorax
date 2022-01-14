import pyaurorax
import datetime


def main():
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
    ds = pyaurorax.sources.get(program, platform, instrument_type, format=pyaurorax.FORMAT_BASIC_INFO)

    # create DataProduct object
    dp = pyaurorax.data_products.DataProduct(data_source=ds,
                                             start=start_dt,
                                             end=end_dt,
                                             data_product_type=data_product_type,
                                             url=url,
                                             metadata=metadata)

    # print
    print(dp)


# ----------
if (__name__ == "__main__"):
    main()
