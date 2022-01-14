import pyaurorax
import datetime


def main():
    # set values
    program = "themis"
    platform = "themisa"
    instrument_type = "footprint"
    epoch = datetime.datetime(2020, 1, 1, 0, 0)
    location_geo = pyaurorax.Location(lat=51.049999, lon=-114.066666)
    location_gsm = pyaurorax.Location(lat=150.25, lon=-10.75)
    nbtrace = pyaurorax.Location(lat=1.23, lon=45.6)
    sbtrace = pyaurorax.Location(lat=7.89, lon=101.23)
    metadata = {}

    # get identifier
    ds = pyaurorax.sources.get(program=program,
                               platform=platform,
                               instrument_type=instrument_type,
                               format=pyaurorax.FORMAT_IDENTIFIER_ONLY)

    # create Ephemeris object
    e = pyaurorax.ephemeris.Ephemeris(data_source=ds,
                                      epoch=epoch,
                                      location_geo=location_geo,
                                      location_gsm=location_gsm,
                                      nbtrace=nbtrace,
                                      sbtrace=sbtrace,
                                      metadata=metadata)

    # print
    print(e)


# ----------
if (__name__ == "__main__"):
    main()
