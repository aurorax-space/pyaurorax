#! /usr/bin/env python

import aurorax
import datetime
import pprint


def main():
    availability = aurorax.availability.get_ephemeris(datetime.datetime(2019, 1, 1),
                                                      datetime.datetime(2019, 1, 5),
                                                      program="swarm",
                                                      instrument_type="ssc-web")
    pprint.pprint(availability)


# ----------
if (__name__ == "__main__"):
    main()
