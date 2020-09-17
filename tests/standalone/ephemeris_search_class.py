#! /usr/bin/env python

import aurorax
import datetime
import pprint


def main():
    # start search
    s = aurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                 datetime.datetime(2020, 1, 10, 0, 0, 0),
                                 programs=["swarm"],
                                 platforms=["swarma"],
                                 instrument_types=["ssc-web"])
    s.execute()

    # get status
    print("Getting status ...")
    s.update_status()

    # check for data
    print("Checking for data ...")
    s.check_for_data()

    # wait for data
    print("Waiting for data ...")
    s.wait_for_data()

    # get data
    print("Retrieving data ...")
    s.get_data()

    # print data
    pprint.pprint(s.data[0:2])
    print("...")


# ----------
if (__name__ == "__main__"):
    main()
