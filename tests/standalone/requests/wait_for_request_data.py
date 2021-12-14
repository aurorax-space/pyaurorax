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
                                   instrument_types=["ssc-web"])
    r.execute()

    # sleep briefly
    time.sleep(1.0)

    # wait for data
    status = pyaurorax.requests.wait_for_data(r.request_url)
    r.update_status(status=status)

    # get data
    r.get_data()

    # print data
    pprint.pprint(r.data[0:2])
    print("...")


# ----------
if (__name__ == "__main__"):
    main()
