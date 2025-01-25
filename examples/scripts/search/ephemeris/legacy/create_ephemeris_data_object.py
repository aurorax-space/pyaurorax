import datetime
import pyaurorax
from pyaurorax.search import EphemerisData, Location


def main():
    # init
    aurorax = pyaurorax.PyAuroraX()

    # set values
    program = "themis"
    platform = "themisa"
    instrument_type = "footprint"
    epoch = datetime.datetime(2020, 1, 1, 0, 0)
    location_geo = Location(lat=51.049999, lon=-114.066666)
    location_gsm = Location(lat=150.25, lon=-10.75)
    nbtrace = Location(lat=1.23, lon=45.6)
    sbtrace = Location(lat=7.89, lon=101.23)
    metadata = {}

    # get identifier
    ds = aurorax.search.sources.get(program=program, platform=platform, instrument_type=instrument_type)

    # create Ephemeris object
    e = EphemerisData(data_source=ds,
                      epoch=epoch,
                      location_geo=location_geo,
                      location_gsm=location_gsm,
                      nbtrace=nbtrace,
                      sbtrace=sbtrace,
                      metadata=metadata)

    # print
    print()
    print(e)
    print()


# ----------
if (__name__ == "__main__"):
    main()
