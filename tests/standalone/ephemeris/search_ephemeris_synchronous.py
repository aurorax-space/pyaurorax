import aurorax
import datetime
import pprint


def main():
    s = aurorax.ephemeris.search(datetime.datetime(2019, 1, 1, 0, 0, 0),
                                 datetime.datetime(2019, 1, 1, 23, 59, 59),
                                 programs=["swarm"],
                                 platforms=["swarma"],
                                 instrument_types=["ssc-web"],
                                 show_progress=True)
    pprint.pprint(s["data"][0:2])
    print("...")


# ----------
if (__name__ == "__main__"):
    main()
