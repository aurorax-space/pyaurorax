import datetime
import pyaurorax


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # start search
    s = aurorax.search.EphemerisSearch(aurorax,
                                       datetime.datetime(2020, 1, 1, 0, 0, 0),
                                       datetime.datetime(2020, 1, 10, 0, 0, 0),
                                       programs=["swarm"],
                                       platforms=["swarma"],
                                       instrument_types=["footprint"])

    print()
    print(s.describe())
    print()


# ----------
if (__name__ == "__main__"):
    main()
