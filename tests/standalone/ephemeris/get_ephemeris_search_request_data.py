import aurorax
import datetime
import time
import pprint


def main():
    # start search
    print("Executing request ...")
    s = aurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                 datetime.datetime(2020, 1, 1, 0, 59, 59),
                                 programs=["swarm"],
                                 platforms=["swarma"],
                                 instrument_types=["footprint"])
    s.execute()

    # if the request isn't done, wait continuously
    print("Waiting for request to complete ...")
    status = aurorax.ephemeris.get_request_status(s.request_id)
    while (status["request_status"]["completed"] is False):
        time.sleep(1)
        status = aurorax.ephemeris.get_request_status(s.request_id)

    # get request data
    data = aurorax.ephemeris.get_request_data(s.request_id)

    # print data
    print("\nFound %s records" % (len(data["data"])))
    pprint.pprint(data["data"][0:2])
    print("...")


# ----------
if (__name__ == "__main__"):
    main()
