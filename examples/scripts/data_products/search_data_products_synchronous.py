import pyaurorax
import datetime
import pprint


def main():
    # do search
    s = pyaurorax.data_products.search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                       datetime.datetime(2020, 1, 1, 23, 59, 59),
                                       programs=["auroramax"],
                                       verbose=True)
    print()
    pprint.pprint(s.data)


# ----------
if (__name__ == "__main__"):
    main()
