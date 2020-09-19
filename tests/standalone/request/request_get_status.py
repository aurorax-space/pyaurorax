#! /usr/bin/env python

import aurorax
import datetime
import time
import pprint


def main():
    # start search
    r = aurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                 datetime.datetime(2020, 1, 1, 1, 0, 0),
                                 programs=["swarm"],
                                 platforms=["swarma"],
                                 instrument_types=["ssc-web"])
    r.execute()

    # sleep briefly
    time.sleep(1.0)

    # get status
    status = aurorax.requests.get_status(r.request_url)

    # print status
    pprint.pprint(status)


# ----------
if (__name__ == "__main__"):
    main()
