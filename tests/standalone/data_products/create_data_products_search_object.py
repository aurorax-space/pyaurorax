import aurorax
import datetime


def main():
    # start search
    s = aurorax.data_products.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                     datetime.datetime(2020, 1, 1, 23, 59, 59),
                                     programs=["auroramax"])
    print(s)


# ----------
if (__name__ == "__main__"):
    main()
