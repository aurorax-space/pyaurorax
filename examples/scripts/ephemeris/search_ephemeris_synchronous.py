import pyaurorax
import datetime
import pprint


def main():
    # do search
    s = pyaurorax.ephemeris.search(datetime.datetime(2019, 1, 1, 0, 0, 0),
                                   datetime.datetime(2019, 1, 10, 23, 59, 59),
                                   programs=["swarm"],
                                   platforms=["swarma"],
                                   instrument_types=["footprint"],
                                   verbose=True)
    print()
    pprint.pprint(s.data[0:10])
    print("...")


# ----------
if (__name__ == "__main__"):
    main()
