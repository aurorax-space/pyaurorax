#! /usr/bin/env python

import aurorax
import datetime
import time
import pprint


def main():
    # start search
    s = aurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                 datetime.datetime(2020, 1, 1, 1, 0, 0),
                                 programs=["swarm"],
                                 platforms=["swarma"],
                                 instrument_types=["ssc-web"])
    s.execute()

    # sleep briefly
    time.sleep(1)

    # get request logs
    logs = aurorax.ephemeris.get_request_logs(s.request_id)

    # print logs
    pprint.pprint(logs)


# ----------
if (__name__ == "__main__"):
    main()
