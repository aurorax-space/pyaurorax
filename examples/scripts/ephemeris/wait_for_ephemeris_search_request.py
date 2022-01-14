import pyaurorax
import datetime
import pprint


def main():
    # start search
    print("Executing request ...")
    s = pyaurorax.ephemeris.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                   datetime.datetime(2020, 1, 2, 23, 59, 59),
                                   programs=["swarm"],
                                   platforms=["swarma"],
                                   instrument_types=["footprint"])
    s.execute()

    # wait for data
    print("Waiting for request to complete ...")
    s.wait()

    # get data
    print("Get data ...")
    s.get_data()

    # print data
    print()
    pprint.pprint(s.data[0:10])
    print("...")


# ----------
if (__name__ == "__main__"):
    main()
