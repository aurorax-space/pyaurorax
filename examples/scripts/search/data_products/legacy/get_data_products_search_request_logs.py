import datetime
import time
import pprint
import pyaurorax


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # start search
    print("Executing search ...")
    s = pyaurorax.search.DataProductSearch(aurorax,
                                           datetime.datetime(2020, 1, 1, 0, 0, 0),
                                           datetime.datetime(2020, 1, 1, 23, 59, 59),
                                           programs=["auroramax"])
    s.execute()

    # if the request isn't done, wait continuously
    print("Waiting for request to complete ...")
    s.update_status()
    while (s.completed is False):
        time.sleep(1)
        s.update_status()

    # print logs
    print()
    pprint.pprint(s.logs)


# ----------
if (__name__ == "__main__"):
    main()
