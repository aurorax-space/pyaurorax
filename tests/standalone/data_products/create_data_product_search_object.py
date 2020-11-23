import aurorax
import datetime


def main():
    # start search
    s = aurorax.data_products.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                     datetime.datetime(2020, 1, 10, 0, 0, 0),
                                     programs=["themis-asi"],
                                     platforms=["gillam"],
                                     instrument_types=["panchromatic ASI"])
    print(s)


# ----------
if (__name__ == "__main__"):
    main()
