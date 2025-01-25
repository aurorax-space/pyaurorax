import os
import datetime
import pprint
import pyaurorax
from pyaurorax.search import Location
from dotenv import load_dotenv


def main():
    # read API key from environment vars
    aurorax = pyaurorax.PyAuroraX()
    load_dotenv("%s/../../../../tests/test_suite/.env" % (os.path.dirname(os.path.realpath(__file__))))
    aurorax.api_base_url = "https://api.staging.aurorax.space"
    aurorax.api_key = os.environ["AURORAX_API_KEY"]

    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    metadata = {
        "test_meta1": "testing1",
        "test_meta2": "testing2",
    }
    epoch = datetime.datetime(2020, 1, 1, 0, 0)
    location_geo = Location(lat=51.049999, lon=-114.066666)
    location_gsm = Location(lat=150.25, lon=-10.75)
    nbtrace = Location(lat=1.23, lon=45.6)
    sbtrace = Location(lat=7.89, lon=101.23)

    # get the data source ID
    ds = aurorax.search.sources.get(program, platform, instrument_type)
    if (ds.identifier is None):
        print("Error retrieving valid data source, aborting")
        return 1

    # create Ephemeris object
    e = pyaurorax.search.EphemerisData(data_source=ds,
                                       epoch=epoch,
                                       location_geo=location_geo,
                                       location_gsm=location_gsm,
                                       nbtrace=nbtrace,
                                       sbtrace=sbtrace,
                                       metadata=metadata)
    pprint.pprint(e)
    print("\nUploading record ...")

    # set records array
    records = []
    records.append(e)

    # upload record
    aurorax.search.ephemeris.upload(ds.identifier, records)
    print("Successfully uploaded")


# ----------
if (__name__ == "__main__"):
    main()
