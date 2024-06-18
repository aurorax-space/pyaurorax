import datetime
import pprint
import pyaurorax


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # do search
    s = aurorax.search.data_products.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                            datetime.datetime(2020, 1, 1, 23, 59, 59),
                                            programs=["auroramax"],
                                            verbose=True)
    print()
    pprint.pprint(s.data)


# ----------
if (__name__ == "__main__"):
    main()
