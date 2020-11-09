import aurorax
import datetime
import time
import pprint


def main():
    # start search
    print("Executing request ...")
    s = aurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                 datetime.datetime(2020, 1, 1, 5, 59, 59),
                                 programs=["swarm"],
                                 platforms=["swarma"],
                                 instrument_types=["ssc-web"])
    s.execute()

    # get status
    print("Getting request status ...")
    status = aurorax.ephemeris.get_request_status(s.request_id)
    pprint.pprint(status)
    print("----------------------------\n")

    # if the request isn't done, wait continuously
    print("Waiting for request to complete ...")
    while (status["request_status"]["completed"] is False):
        time.sleep(1)
        status = aurorax.ephemeris.get_request_status(s.request_id)

    # print status
    pprint.pprint(status)


# ----------
if (__name__ == "__main__"):
    main()
