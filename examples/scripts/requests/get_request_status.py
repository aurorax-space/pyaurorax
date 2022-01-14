#! /usr/bin/env python

import pyaurorax
import datetime
import time
import pprint


def main():
    # start search
    r = pyaurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                   datetime.datetime(2020, 1, 1, 1, 0, 0),
                                   programs=["swarm"],
                                   platforms=["swarma"],
                                   instrument_types=["footprint"])
    r.execute()

    # sleep briefly
    time.sleep(1.0)

    # get status
    status = pyaurorax.requests.get_status(r.request_url)

    # print status
    pprint.pprint(status)


# ----------
if (__name__ == "__main__"):
    main()
