#! /usr/bin/env python

import aurorax
import datetime
import pprint


def main():
    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    identifier = -999
    epoch = datetime.datetime(2020, 1, 1, 0, 0)
    location_geo = aurorax.Location(51.049999, -114.066666)
    location_gsm = aurorax.Location(150.25, -10.75)
    nbtrace = aurorax.Location(1.23, 45.6)
    sbtrace = aurorax.Location(7.89, 101.23)
    metadata = {}

    # create Ephemeris object
    e = aurorax.ephemeris.Ephemeris(identifier,
                                    program,
                                    platform,
                                    instrument_type,
                                    epoch,
                                    location_geo,
                                    location_gsm,
                                    nbtrace,
                                    sbtrace,
                                    metadata)

    # print
    print("__str__:\n----------")
    print(e)
    print()
    print("__repr__:\n----------")
    pprint.pprint(e)


# ----------
if (__name__ == "__main__"):
    main()
