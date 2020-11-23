import aurorax
import datetime
import pprint


def main():
    s = aurorax.data_products.search(datetime.datetime(2019, 1, 1, 0, 0, 0),
                                     datetime.datetime(2019, 1, 1, 23, 59, 59),
                                     programs=["themis-asi"],
                                     platforms=["gillam"],
                                     instrument_types=["panchromatic ASI"],
                                     show_progress=True)
    pprint.pprint(s["data"][0:2])
    print("...")


# ----------
if (__name__ == "__main__"):
    main()
