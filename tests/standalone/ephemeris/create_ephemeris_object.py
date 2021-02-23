import aurorax
import datetime
import pprint


def main():
    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    epoch = datetime.datetime(2020, 1, 1, 0, 0)
    location_geo = aurorax.Location(lat=51.049999, lon=-114.066666)
    location_gsm = aurorax.Location(lat=150.25, lon=-10.75)
    nbtrace = aurorax.Location(lat=1.23, lon=45.6)
    sbtrace = aurorax.Location(lat=7.89, lon=101.23)
    metadata = {}

    # get identifier
    data_source = aurorax.sources.get_using_filters(program=program,
                                                    platform=platform,
                                                    instrument_type=instrument_type)
    identifier = data_source[0]["identifier"]

    # create Ephemeris object
    e = aurorax.ephemeris.Ephemeris(identifier=identifier,
                                    program=program,
                                    platform=platform,
                                    instrument_type=instrument_type,
                                    epoch=epoch,
                                    location_geo=location_geo,
                                    location_gsm=location_gsm,
                                    nbtrace=nbtrace,
                                    sbtrace=sbtrace,
                                    metadata=metadata)

    # print
    print("__str__:\n----------")
    print(e)
    print()
    print("__repr__:\n----------")
    pprint.pprint(e)


# ----------
if (__name__ == "__main__"):
    main()
