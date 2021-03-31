import aurorax
import datetime
import time
import pprint


def main():
    # set as staging API
    aurorax.api.set_base_url("https://api.staging.aurorax.space")

    # start search
    print("Executing search ...")
    s = aurorax.data_products.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
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
