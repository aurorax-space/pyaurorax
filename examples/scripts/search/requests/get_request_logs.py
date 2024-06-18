import datetime
import time
import pprint
import pyaurorax


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # start search
    r = pyaurorax.search.EphemerisSearch(aurorax,
                                         datetime.datetime(2020, 1, 1, 0, 0, 0),
                                         datetime.datetime(2020, 1, 1, 1, 0, 0),
                                         programs=["swarm"],
                                         platforms=["swarma"],
                                         instrument_types=["footprint"])
    r.execute()

    # sleep briefly
    time.sleep(1.0)

    # wait for data
    logs = aurorax.search.requests.get_logs(r.request_url)

    # print logs
    pprint.pprint(logs)


# ----------
if (__name__ == "__main__"):
    main()
