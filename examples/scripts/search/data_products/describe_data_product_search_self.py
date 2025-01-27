import datetime
import pyaurorax


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # start search
    s = pyaurorax.search.DataProductSearch(
        aurorax,
        datetime.datetime(2020, 1, 1, 0, 0, 0),
        datetime.datetime(2020, 1, 1, 23, 59, 59),
        programs=["auroramax"],
    )

    print()
    print(s.describe())
    print()


# ----------
if (__name__ == "__main__"):
    main()
