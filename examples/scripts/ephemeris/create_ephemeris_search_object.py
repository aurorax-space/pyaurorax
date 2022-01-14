import pyaurorax
import datetime


def main():
    s = pyaurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                   datetime.datetime(2020, 1, 10, 0, 0, 0),
                                   programs=["swarm"],
                                   platforms=["swarma"],
                                   instrument_types=["footprint"])
    print(s)


# ----------
if (__name__ == "__main__"):
    main()
