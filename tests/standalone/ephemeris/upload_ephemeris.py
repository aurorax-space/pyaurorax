import aurorax
import os
import datetime
import pprint


def main():
    # read API key from environment vars
    api_key = os.environ["AURORAX_API_KEY"]

    # set values
    program = "test-program"
    platform = "test-platform"
    instrument_type = "test-instrument-type"
    metadata = {
        "test_meta1": "testing1",
        "test_meta2": "testing2",
    }
    epoch = datetime.datetime(2020, 1, 1, 0, 0)
    location_geo = aurorax.Location(51.049999, -114.066666)
    location_gsm = aurorax.Location(150.25, -10.75)
    nbtrace = aurorax.Location(1.23, 45.6)
    sbtrace = aurorax.Location(7.89, 101.23)

    # get the ephemeris source ID
    source = aurorax.sources.get_using_filters(program=[program],
                                               platform=[platform],
                                               instrument_type=[instrument_type])
    identifier = source["data"][0]["identifier"]

    # create Ephemeris object
    e = aurorax.ephemeris.Ephemeris(identifier,
                                    program,
                                    platform,
                                    instrument_type,
                                    epoch,
                                    location_geo,
                                    location_gsm,
                                    nbtrace,
                                    sbtrace,
                                    metadata)
    pprint.pprint(e)
    print("\nUploading record ...")

    # set records array
    records = []
    records.append(e)

    # upload record
    res = aurorax.ephemeris.upload(api_key, identifier, records=records)

    # print result
    if (res["status_code"] == 202):
        print("Successfully uploaded")
    else:
        print("Failed to upload")
        pprint.pprint(res)


# ----------
if (__name__ == "__main__"):
    main()
