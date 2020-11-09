import aurorax
import datetime
import pprint


def main():
    # get availability
    availability = aurorax.availability.ephemeris(datetime.datetime(2019, 1, 1),
                                                  datetime.datetime(2019, 1, 5),
                                                  program="swarm",
                                                  platform="swarma",
                                                  instrument_type="ssc-web")
    pprint.pprint(availability)


# ----------
if (__name__ == "__main__"):
    main()
