import aurorax
import datetime
import pprint


def main():
    # start search
    print("Executing request ...")
    r = aurorax.data_products.Search(datetime.datetime(2020, 1, 1, 0, 0, 0),
                                     datetime.datetime(2020, 1, 1, 23, 59, 59),
                                     programs=["themis-asi"],
                                     platforms=["gillam"],
                                     instrument_types=["panchromatic ASI"])
    r.execute()

    # wait for data
    print("Waiting for request to complete ...")
    status = aurorax.data_products.wait_for_data(r.request_id)

    # update status
    print("Request complete, update status variable ...")
    r.update_status(status=status)

    # get data
    print("Get data ...")
    r.get_data()

    # print data
    print()
    pprint.pprint(r.data[0:2])
    print("...")


# ----------
if (__name__ == "__main__"):
    main()
