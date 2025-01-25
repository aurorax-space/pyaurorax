import datetime
import pyaurorax


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # start search
    s = pyaurorax.search.EphemerisSearch(aurorax,
                                         datetime.datetime(2020, 1, 1, 0, 0, 0),
                                         datetime.datetime(2020, 1, 10, 0, 0, 0),
                                         programs=["swarm"],
                                         platforms=["swarma"],
                                         instrument_types=["footprint"])

    print()
    print(aurorax.search.ephemeris.describe(search_obj=s))
    print()


# ----------
if (__name__ == "__main__"):
    main()
