import datetime
import time
import pprint
import pyaurorax


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # start search
    print("Executing request ...")
    s = aurorax.search.EphemerisSearch(aurorax,
                                       datetime.datetime(2020, 1, 1, 0, 0, 0),
                                       datetime.datetime(2020, 1, 1, 23, 59, 59),
                                       programs=["swarm"],
                                       platforms=["swarma"],
                                       instrument_types=["footprint"])
    s.execute()

    # get status
    print("Getting request status ...")
    s.update_status()
    pprint.pprint(s.status)
    print("----------------------------\n")

    # if the request isn't done, wait continuously
    print("Waiting for request to complete ...")
    while (s.completed is False):
        time.sleep(1)
        s.update_status()

    # print status
    pprint.pprint(s.status)


# ----------
if (__name__ == "__main__"):
    main()
