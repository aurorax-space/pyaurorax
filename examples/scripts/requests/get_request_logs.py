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

    # wait for data
    logs = pyaurorax.requests.get_logs(r.request_url)

    # print logs
    pprint.pprint(logs)


# ----------
if (__name__ == "__main__"):
    main()
