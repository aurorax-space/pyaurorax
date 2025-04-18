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

    # if the request isn't done, wait continuously
    print("Waiting for request to complete ...")
    s.update_status()
    while (s.completed is False):
        time.sleep(1)
        s.update_status()

    # get request data
    s.get_data()

    # print data
    print("\nFound %d records" % (len(s.data)))
    pprint.pprint(s.data[0:10])
    print("...")


# ----------
if (__name__ == "__main__"):
    main()
