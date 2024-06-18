import datetime
import pyaurorax
from pyaurorax.search import DataProductSearch


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # start search
    s = DataProductSearch(
        aurorax,
        datetime.datetime(2020, 1, 1, 0, 0, 0),
        datetime.datetime(2020, 1, 1, 23, 59, 59),
        programs=["auroramax"],
    )

    print()
    print(aurorax.search.data_products.describe(search_obj=s))
    print()


# ----------
if (__name__ == "__main__"):
    main()
