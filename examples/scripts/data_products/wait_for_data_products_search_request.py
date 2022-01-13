import pyaurorax
import datetime
import pprint


def main():
    # set as staging API
    pyaurorax.api.set_base_url("https://api.staging.aurorax.space")

    # start search
    print("Executing request ...")
    s = pyaurorax.data_products.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                       datetime.datetime(
                                           2020, 1, 2, 23, 59, 59),
                                       programs=["auroramax"])
    s.execute()

    # wait for data
    print("Waiting for request to complete ...")
    s.wait()

    # get data
    print("Get data ...")
    s.get_data()

    # print data
    print()
    pprint.pprint(s.data[0:2])
    print("...")


# ----------
if (__name__ == "__main__"):
    main()
